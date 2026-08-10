
from pathlib import Path
from datetime import date
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from providers.fred import fetch_series

SOURCES = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
HIST = ROOT / "data" / "history"
LATEST = ROOT / "data" / "latest.json"

def update_fred():
    done, failed = [], []
    for indicator_id, cfg in SOURCES["providers"]["fred"]["series"].items():
        try:
            data = fetch_series(cfg["series_id"])
            obj = {
                "id": indicator_id,
                "name": cfg["name"],
                "unit": cfg["unit"],
                "frequency": cfg["frequency"],
                "source": cfg["source_label"],
                "source_id": cfg["series_id"],
                "provider": "fred",
                "is_demo": False,
                "updated": data[-1][0],
                "data": data,
            }
            (HIST / f"{indicator_id}.json").write_text(
                json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            done.append(indicator_id)
        except Exception as e:
            failed.append((indicator_id, str(e)))
    return done, failed

def rebuild_latest():
    latest = {
        "updated": date.today().isoformat(),
        "is_demo": False,
        "mode": "hybrid",
        "items": {},
    }
    any_demo = False
    for fp in HIST.glob("*.json"):
        obj = json.loads(fp.read_text(encoding="utf-8"))
        data = obj.get("data") or []
        if not data:
            continue
        cur = data[-1][1]
        prev = data[-2][1] if len(data) > 1 else cur
        pct = ((cur - prev) / abs(prev) * 100) if prev not in (0, None) else 0
        is_demo = bool(obj.get("is_demo", True))
        any_demo |= is_demo
        latest["items"][obj["id"]] = {
            "value": cur,
            "change_pct": round(pct, 2),
            "updated": obj.get("updated"),
            "unit": obj.get("unit"),
            "is_demo": is_demo,
            "source": obj.get("source", ""),
            "provider": obj.get("provider", "demo"),
        }
    latest["is_demo"] = any_demo
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    done, failed = update_fred()
    rebuild_latest()
    print("UPDATED:", ", ".join(done) if done else "(none)")
    if failed:
        print("FAILED:")
        for iid, err in failed:
            print(" -", iid, "=>", err)
        # Fail workflow only if every live source failed.
        if not done:
            raise SystemExit(1)
