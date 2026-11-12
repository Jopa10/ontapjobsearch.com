#!/usr/bin/env python3
"""Package only Thursday production-selected and automated-review adverts."""
import argparse, csv, hashlib, json, re, sys
from pathlib import Path

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def review_ids(root, day):
    found = {}
    for path in sorted(root.rglob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "job_id" not in reader.fieldnames or "decision" not in reader.fieldnames:
                continue
            for row in reader:
                if row.get("feed_date") != day:
                    continue
                decision = (row.get("decision") or "").strip()
                if decision.startswith(("POSS", "REVIEW")):
                    jid = (row.get("job_id") or "").strip()
                    if jid: found[jid] = decision
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8-sig")
        for block in re.split(r"(?m)^---\s*$", text):
            match = re.search(r"(?m)^\s*(POSS(?:\s*-[^|\n]+)?|REVIEW(?:\s*-[^|\n]+)?)\s*(?:\||$)", block)
            id_match = re.search(r"(?m)^job_id:\s*(\S+)\s*$", block)
            if match and id_match and re.search(r"(?m)^feed_date:\s*"+re.escape(day)+r"\s*$", text[:min(len(text), 256)]):
                found[id_match.group(1)] = match.group(1).strip()
    return found

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive", required=True); p.add_argument("--outputs", required=True)
    p.add_argument("--reviews", required=True); p.add_argument("--date", required=True)
    p.add_argument("--production-run-id", type=int, required=True)
    p.add_argument("--production-run-commit", required=True)
    p.add_argument("--app-commit", required=True); p.add_argument("--output", required=True)
    a=p.parse_args()
    if not re.fullmatch(r"20\d\d-\d\d-\d\d",a.date): raise SystemExit("Invalid feed date")
    for value in (a.production_run_commit,a.app_commit):
        if not re.fullmatch(r"[a-f0-9]{40}",value): raise SystemExit("Invalid provenance commit")
    # Reuse the production-tested XML flattening and duplicate quarantine rules.
    sys.path.insert(0,str(Path(__file__).parent))
    from prepare_raw_stage import load_archive
    archive=Path(a.archive)
    raw_rows, receipt=load_archive(archive)
    feed={}
    for row in raw_rows:
        jid=row.get("/Job/DisplayReference","").strip()
        if jid: feed[jid]=row
    selected=set()
    for file in Path(a.outputs).rglob("*.json"):
        try: values=json.loads(file.read_text(encoding="utf-8-sig"))
        except Exception as e: raise SystemExit(f"Bad output artifact file {file.name}: {e}")
        if not isinstance(values,list): continue
        for row in values:
            if isinstance(row,dict) and row.get("source")=="JobG8":
                jid=str(row.get("job_id","")).strip()
                if jid: selected.add(jid)
    if not selected: raise SystemExit("No selected JobG8 IDs found in production output artifacts")
    reviews=review_ids(Path(a.reviews),a.date)
    candidate_ids=selected|set(reviews)
    missing=sorted(candidate_ids-set(feed))
    if missing: raise SystemExit(f"{len(missing)} selected/review IDs are missing from the dated raw feed; first: {missing[:10]}")
    records=[]
    for jid in sorted(candidate_ids):
        payload=feed[jid]
        decision="SELECTED" if jid in selected else "REVIEW"
        reason="present in final production output" if decision=="SELECTED" else reviews[jid]
        raw_hash=hashlib.sha256(canonical(payload).encode()).hexdigest()
        records.append({"public_id":jid,"decision":decision,"decision_reason":reason,
          "selector_revision":a.production_run_commit,"raw_payload":payload,"payload_sha256":raw_hash})
    archive_sha=hashlib.sha256(archive.read_bytes()).hexdigest()
    result={"schemaVersion":1,"feedDate":a.date,"productionWorkflowRunId":a.production_run_id,
      "productionRunCommit":a.production_run_commit,"productionAppCommit":a.app_commit,
      "archiveKey":"jobg8/raw/"+a.date+".zip","archiveSha256":archive_sha,
      "rawFeedDiagnostics":receipt,"selectedIds":len(selected),"reviewIds":len(reviews),
      "uniqueSelectedOrReviewIds":len(records),"payloadBytes":sum(len(canonical(r["raw_payload"]).encode()) for r in records),
      "records":records}
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="records"},sort_keys=True))
if __name__=="__main__": main()
