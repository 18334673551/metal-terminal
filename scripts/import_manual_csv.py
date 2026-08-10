
"""
Import a manually downloaded/licensed CSV into data/history/<indicator>.json.

CSV format:
date,value
2026-08-01,123.4
2026-08-08,125.1
"""
from pathlib import Path
import argparse, csv, json

ROOT = Path(__file__).resolve().parents[1]

p = argparse.ArgumentParser()
p.add_argument("--indicator", required=True)
p.add_argument("--file", required=True)
p.add_argument("--name", required=True)
p.add_argument("--unit", required=True)
p.add_argument("--frequency", required=True)
p.add_argument("--source", required=True)
args = p.parse_args()

rows=[]
with open(args.file, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        if not r.get("date") or not r.get("value"):
            continue
        rows.append([r["date"].strip(), float(r["value"])])
rows.sort(key=lambda x:x[0])

obj={
    "id":args.indicator,"name":args.name,"unit":args.unit,
    "frequency":args.frequency,"source":args.source,
    "provider":"manual","is_demo":False,
    "updated":rows[-1][0],"data":rows
}
out=ROOT/"data/history"/f"{args.indicator}.json"
out.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
print(out)
