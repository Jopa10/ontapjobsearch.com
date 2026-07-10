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

CSV_COLUMNS = ['decision', 'region', 'title', 'town', 'salary_text', 'manual_override', 'manual_select', 'job_id', 'geo_lookup_source']


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


def resolve_cluster(town, location, geo_map):
    """Resolve geography using the established rule: /Job/Area is the town key, /Job/Location is fallback."""
    town_key = low(town)
    location_key = low(location)
    if town_key and town_key in geo_map:
        return geo_map[town_key], 'area_town'
    if location_key and location_key in geo_map:
        return geo_map[location_key], 'location_fallback'
    return '', 'unmapped'


def build(kind, slices, jobs, geo_map):
    rows = []
    for _, row in jobs.iterrows():
        town = clean(row['/Job/Area'])
        job_location = clean(row['/Job/Location'])
        cluster, geo_source = resolve_cluster(town, job_location, geo_map)
        title = clean(row['/Job/Position'])
        desc = clean(row.get('/Job/Description', ''))
        cls = classify(title, desc, kind)
        if cls != 'HIGH_CONFIDENCE':
            continue
        if has_any(f'{town} {job_location} {cluster}', NI_TERMS) and cluster == 'London':
            continue
        for target in slices:
            if cluster != target:
                continue
            rows.append({
                'decision': 'review',
                'region': target,
                'title': title,
                'town': town,
                'salary_text': salary(row),
                'manual_override': '',
                'manual_select': '',
                'job_id': clean(row.get('/Job/DisplayReference', '')),
                'geo_lookup_source': geo_source,
            })
    return pd.DataFrame(rows, columns=CSV_COLUMNS)


def write_md(df, path, heading):
    lines = [f'# {heading}', '', 'Generated on test branch only. No live JSONs or daily manual review files are changed.', '']
    if df.empty:
        lines.append('_No rows found._')
    else:
        for region, group in df.groupby('region', sort=False):
            lines += [f'## {region}', '', f'Rows: {len(group)}', '']
            lines.append('| ' + ' | '.join(CSV_COLUMNS) + ' |')
            lines.append('| ' + ' | '.join(['---'] * len(CSV_COLUMNS)) + ' |')
            for _, r in group[CSV_COLUMNS].head(200).fillna('').iterrows():
                vals = [str(r[c]).replace('|', '\\|').replace('\n', ' ') for c in CSV_COLUMNS]
                lines.append('| ' + ' | '.join(vals) + ' |')
            lines.append('')
    path.write_text('\n'.join(lines) + '\n')


def write_outputs(admin, support):
    admin.to_csv(OUT / 'service-admin-expansion-review.csv', index=False)
    support.to_csv(OUT / 'support-worker-expansion-review.csv', index=False)
    write_md(admin, OUT / 'service-admin-expansion-review.md', 'Admin/service expansion review')
    write_md(support, OUT / 'support-worker-expansion-review.md', 'Support-worker expansion review')


def log_summary(admin, support):
    log = [
        'Expansion manual review run',
        'Geo rule: /Job/Area primary town key, /Job/Location fallback.',
        'CSV format: decision, region, title, town, salary_text, manual_override, manual_select, job_id, geo_lookup_source.',
        'Outputs written only under pipeline/manual-expansion/',
        'No live JSONs changed.',
        'No daily manual review CSV/MD files changed.',
        'No merge to main performed.',
    ]
    for name, df in [('admin/service', admin), ('support-worker', support)]:
        log.append(f'{name} total rows: {len(df)}')
        if not df.empty:
            for region, group in df.groupby('region', sort=False):
                area_town = int((group['geo_lookup_source'] == 'area_town').sum())
                fallback = int((group['geo_lookup_source'] == 'location_fallback').sum())
                log.append(f'{name} {region}: rows={len(group)}, area_town_lookup={area_town}, location_fallback={fallback}')
    ni_london = 0
    if not admin.empty:
        london = admin[admin['region'] == 'London']
        if not london.empty:
            ni_london = int(london.apply(lambda r: has_any(f"{r.get('town','')} {r.get('region','')}", NI_TERMS), axis=1).sum())
    log.append(f'London admin/service NI/Derry/Belfast wrong-region rows: {ni_london}')
    (OUT / 'expansion-review-run-log.txt').write_text('\n'.join(log) + '\n')


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
    write_outputs(admin, support)
    log_summary(admin, support)


if __name__ == '__main__':
    main()
