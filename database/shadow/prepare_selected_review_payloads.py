#!/usr/bin/env python3
"""Package only Thursday production-selected and automated-review adverts."""
import argparse, csv, hashlib, json, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

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
        if not re.search(r"(?m)^feed_date:\s*"+re.escape(day)+r"\s*$", text[:512]):
            continue
        for block in re.split(r"(?m)^---\s*$", text):
            match = re.search(r"(?m)^\s*(POSS(?:\s*-[^|\n]+)?|REVIEW(?:\s*-[^|\n]+)?)\s*(?:\||$)", block)
            id_match = re.search(r"(?m)^job_id:\s*(\S+)\s*$", block)
            if match and id_match:
                found[id_match.group(1)] = match.group(1).strip()
    return found

def load_candidate_payloads(archive_path, candidate_ids):
    # Parse all Job nodes, but validate and retain only selected/review IDs.
    # This keeps malformed, non-candidate feed rows out of the test scope.
    sys.path.insert(0,str(Path(__file__).parent))
    from prepare_raw_stage import flatten
    with zipfile.ZipFile(archive_path) as archive:
        names=[n for n in archive.namelist() if Path(n).name.lower()=="jobs.xml"]
        if len(names)!=1: raise SystemExit("Expected exactly one Jobs.xml in dated archive")
        with archive.open(names[0]) as handle: root=ET.parse(handle).getroot()
    payloads, conflicts={},set()
    job_nodes=0
    for node in root.iter():
        if node.tag.rsplit("}",1)[-1].lower()!="job": continue
        job_nodes+=1
        row={}; flatten(node,["Job"],row)
        jid=row.get("/Job/DisplayReference","").strip()
        if jid not in candidate_ids: continue
        if not row.get("/Job/Position") or not row.get("/Job/ApplicationURL"):
            raise SystemExit("A selected/review candidate lacks its title or apply URL in the raw payload: "+jid)
        if jid in payloads and payloads[jid]!=row: conflicts.add(jid)
        else: payloads[jid]=row
    if conflicts: raise SystemExit("Conflicting duplicate raw records for selected/review IDs: "+", ".join(sorted(conflicts)[:10]))
    missing=sorted(candidate_ids-set(payloads))
    if missing: raise SystemExit(f"{len(missing)} selected/review IDs are absent from the dated raw feed; first: {missing[:10]}")
    return payloads,job_nodes

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True); p.add_argument("--outputs",required=True)
    p.add_argument("--reviews",required=True); p.add_argument("--date",required=True)
    p.add_argument("--production-run-id",type=int,required=True)
    p.add_argument("--production-run-commit",required=True)
    p.add_argument("--app-commit",required=True); p.add_argument("--output",required=True)
    a=p.parse_args()
    if not re.fullmatch(r"20\d\d-\d\d-\d\d",a.date): raise SystemExit("Invalid feed date")
    for value in (a.production_run_commit,a.app_commit):
        if not re.fullmatch(r"[a-f0-9]{40}",value): raise SystemExit("Invalid provenance commit")
    selected=set()
    for file in Path(a.outputs).rglob("*.json"):
        try: values=json.loads(file.read_text(encoding="utf-8-sig"))
        except Exception as e: raise SystemExit(f"Bad production output file {file.name}: {e}")
        if not isinstance(values,list): continue
        for row in values:
            if isinstance(row,dict) and row.get("source")=="JobG8":
                jid=str(row.get("job_id","")).strip()
                if jid: selected.add(jid)
    if not selected: raise SystemExit("No selected JobG8 IDs found in production output artifacts")
    reviews=review_ids(Path(a.reviews),a.date)
    candidate_ids=selected|set(reviews)
    payloads,job_nodes=load_candidate_payloads(a.archive,candidate_ids)
    records=[]
    for jid in sorted(candidate_ids):
        payload=payloads[jid]
        decision="SELECTED" if jid in selected else "REVIEW"
        reason="present in final production output" if decision=="SELECTED" else reviews[jid]
        records.append({"public_id":jid,"decision":decision,"decision_reason":reason,
          "selector_revision":a.production_run_commit,"raw_payload":payload,
          "payload_sha256":hashlib.sha256(canonical(payload).encode()).hexdigest()})
    archive=Path(a.archive)
    result={"schemaVersion":1,"feedDate":a.date,"productionWorkflowRunId":a.production_run_id,
      "productionRunCommit":a.production_run_commit,"productionAppCommit":a.app_commit,
      "archiveKey":"jobg8/raw/"+a.date+".zip","archiveSha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
      "rawFeedJobNodes":job_nodes,"selectedIds":len(selected),"reviewIds":len(reviews),
      "uniqueSelectedOrReviewIds":len(records),
      "payloadBytes":sum(len(canonical(r["raw_payload"]).encode()) for r in records),"records":records}
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="records"},sort_keys=True))
if __name__=="__main__": main()
