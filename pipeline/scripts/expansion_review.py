from pathlib import Path
import pandas as pd

OUT = Path('pipeline/manual-expansion')
JOB_PATH = Path('pipeline/input/jobg8.xlsx')
GEO_PATH = Path('pipeline/geo/geo_lookup.xlsx')

ADMIN_SLICES = ['London', 'Northern Ireland - East', 'Hampshire', 'Surrey']
SUPPORT_SLICES = ['Sussex', 'Hampshire', 'Cumbria - South', 'Lancashire - North', 'Cumbria - North']

ADMIN_INCLUDE = ['admin','administrator','administration','administrative','customer service','receptionist','office','service advisor','service administrator','service coordinator','business support','data entry','call handler','contact centre','scheduler','planner','booking','bookings']
ADMIN_EXCLUDE = ['support worker','care assistant','care worker','healthcare assistant','nurse','teacher','driver','engineer','warehouse','operative','labourer','manager','senior manager','sales executive','field sales','business development','account manager']
SUPPORT_INCLUDE = ['support worker','support workers','care assistant','care worker','healthcare assistant','health care assistant','healthcare support worker','homecare assistant','home care assistant','personal assistant','community care assistant','community care worker','residential support worker','mental health support worker','learning disability support worker']
SUPPORT_EXCLUDE = ['senior','lead','team leader','deputy','manager','coordinator','officer','housing','homeless','tenancy','driver','transport','school','sen ','send','semh','teacher','teaching','nurse','therapist','social worker','counsellor','admin','administrator','administration','business support','sales support','it support','project support']
NI_TERMS = ['belfast', 'londonderry', 'derry', 'county londonderry', 'northern ireland']


def clean(v):
    if pd.isna(v):
        return ''
    return str(v).strip()


def low(v):
    return clean(v).casefold()


def has_any(text, terms):
    t = low(text)
    return any(term in t for term in terms)


def salary(row):
    parts = []
    for col in ['/Job/SalaryMinimum','/Job/SalaryMaximum','/Job/SalaryPeriod','/Job/SalaryAdditional']:
        val = clean(row.get(col, ''))
        if val:
            parts.append(val)
    return ' | '.join(parts)


def classify(title, desc, kind):
    text = f'{title} {desc}'
    if kind == 'admin':
        if has_any(text, ADMIN_EXCLUDE):
            return 'HARD_PASS'
        if has_any(text, ADMIN_INCLUDE):
            return 'HIGH_CONFIDENCE'
    else:
        if has_any(text, SUPPORT_EXCLUDE):
            return 'HARD_PASS'
        if has_any(text, SUPPORT_INCLUDE):
            return 'HIGH_CONFIDENCE'
    return 'OUT_OF_SCOPE'


def load_geo():
    geo = pd.read_excel(GEO_PATH)
    geo.columns = [str(c).strip() for c in geo.columns]
    if 'Area' not in geo.columns or 'Cluster' not in geo.columns:
        raise SystemExit('geo_lookup.xlsx must contain Area and Cluster columns')
    geo['Area'] = geo['Area'].map(clean)
    geo['Cluster'] = geo['Cluster'].map(clean)
    return dict(zip(geo['Area'].map(low), geo['Cluster']))


def resolve_cluster(town, area, geo_map):
    """Resolve geography using the normal rule: town/location first, then area fallback."""
    town_key = low(town)
    area_key = low(area)
    if town_key and town_key in geo_map:
        return geo_map[town_key], 'location'
    if area_key and area_key in geo_map:
        return geo_map[area_key], 'area'
    return '', 'unmapped'


def decision(target, cluster, area, town, classification, kind):
    hay = f'{area} {town} {cluster}'
    if target == 'London' and has_any(hay, NI_TERMS):
        return 'EXCLUDE_WRONG_REGION', 'NI/Derry/Belfast safety exclusion from London'
    if cluster != target:
        return 'EXCLUDE_WRONG_REGION', f'Cluster does not match {target}'
    if classification == 'HIGH_CONFIDENCE':
        return 'REVIEW_CANDIDATE', f'{kind} high-confidence title'
    return 'EXCLUDE_TITLE', f'{kind} title not accepted'


def build(kind, slices, jobs, geo_map):
    rows = []
    for _, row in jobs.iterrows():
        area = clean(row['/Job/Area'])
        town = clean(row['/Job/Location'])
        cluster, geo_source = resolve_cluster(town, area, geo_map)
        title = clean(row['/Job/Position'])
        desc = clean(row.get('/Job/Description', ''))
        cls = classify(title, desc, kind)
        if cls == 'OUT_OF_SCOPE':
            continue
        for target in slices:
            if cluster != target:
                continue
            dec, reason = decision(target, cluster, area, town, cls, kind)
            if dec != 'REVIEW_CANDIDATE':
                continue
            rows.append({
                'decision': dec,
                'target_slice': target,
                'region_cluster': cluster,
                'geo_lookup_source': geo_source,
                'title': title,
                'town_location': town,
                'area': area,
                'advertiser': clean(row.get('/Job/AdvertiserName', '')),
                'salary_text': salary(row),
                'job_id': clean(row.get('/Job/DisplayReference', '')),
                'apply_url': clean(row.get('/Job/ApplicationURL', '')),
                'reason_classification': reason,
                'title_classification': cls,
            })
    return pd.DataFrame(rows)


def write_md(df, path, heading):
    lines = [f'# {heading}', '', 'Generated on test branch only. No live JSONs or daily manual review files are changed.', '']
    if df.empty:
        lines.append('_No rows found._')
    else:
        for target, group in df.groupby('target_slice', sort=False):
            lines += [f'## {target}', '', f'Rows: {len(group)}', '']
            cols = ['decision','title','town_location','area','geo_lookup_source','advertiser','salary_text','job_id','reason_classification']
            lines.append('| ' + ' | '.join(cols) + ' |')
            lines.append('| ' + ' | '.join(['---'] * len(cols)) + ' |')
            for _, r in group[cols].head(200).fillna('').iterrows():
                vals = [str(r[c]).replace('|', '\\|').replace('\n', ' ') for c in cols]
                lines.append('| ' + ' | '.join(vals) + ' |')
            lines.append('')
    path.write_text('\n'.join(lines) + '\n')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = pd.read_excel(JOB_PATH)
    jobs.columns = [str(c).strip() for c in jobs.columns]
    required = ['/Job/DisplayReference','/Job/Position','/Job/AdvertiserName','/Job/Area','/Job/Location','/Job/ApplicationURL','/Job/Description']
    missing = [c for c in required if c not in jobs.columns]
    if missing:
        raise SystemExit(f'Missing JobG8 columns: {missing}')
    geo_map = load_geo()
    admin = build('admin', ADMIN_SLICES, jobs, geo_map)
    support = build('support', SUPPORT_SLICES, jobs, geo_map)
    admin.to_csv(OUT / 'service-admin-expansion-review.csv', index=False)
    support.to_csv(OUT / 'support-worker-expansion-review.csv', index=False)
    write_md(admin, OUT / 'service-admin-expansion-review.md', 'Admin/service expansion review')
    write_md(support, OUT / 'support-worker-expansion-review.md', 'Support-worker expansion review')
    log = ['Expansion manual review run', 'Geo rule: /Job/Location first, /Job/Area fallback.', 'Outputs written only under pipeline/manual-expansion/', 'No live JSONs changed.', 'No daily manual review CSV/MD files changed.', 'No merge to main performed.']
    for name, df in [('admin/service', admin), ('support-worker', support)]:
        log.append(f'{name} total rows: {len(df)}')
        if not df.empty:
            for target, group in df.groupby('target_slice', sort=False):
                cand = int((group['decision'] == 'REVIEW_CANDIDATE').sum())
                loc = int((group['geo_lookup_source'] == 'location').sum())
                area = int((group['geo_lookup_source'] == 'area').sum())
                log.append(f'{name} {target}: rows={len(group)}, candidates={cand}, location_lookup={loc}, area_fallback={area}')
    ni_london = 0
    if not admin.empty:
        london = admin[admin['target_slice'] == 'London']
        if not london.empty:
            ni_london = int(london.apply(lambda r: has_any(f"{r.get('area','')} {r.get('town_location','')} {r.get('region_cluster','')}", NI_TERMS), axis=1).sum())
    log.append(f'London admin/service NI/Derry/Belfast wrong-region rows: {ni_london}')
    (OUT / 'expansion-review-run-log.txt').write_text('\n'.join(log) + '\n')


if __name__ == '__main__':
    main()
