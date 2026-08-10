#!/usr/bin/env python3
"""
V1 updater:
- 自动更新 FRED 免费公开数据（无需 API Key）：
  * DFII10: 美国10年期实际利率
  * DTWEXBGS: Fed广义美元指数（DXY免费代理）
  * UNRATE: 美国失业率
  * FEDFUNDS: 有效联邦基金利率（月度）
- 中国国家统计局、全球PMI、央行购金等月/季数据：
  V1 先保留 latest.json 中最近一期值；可继续增加 scraper。
"""
from pathlib import Path
import csv, io, json, urllib.request
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "latest.json"

def fred_csv(series):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 macro-dashboard/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text)))
    vals=[]
    for row in rows:
        v=row.get(series)
        if v and v != ".":
            try: vals.append((row["DATE"], float(v)))
            except: pass
    return vals[-2:] if len(vals)>=2 else vals

def update_metric(metrics, mid, value, period, previous=None, direction=None, source=None):
    m=next((x for x in metrics if x["id"]==mid),None)
    if not m:return
    m["value"]=round(value,2) if isinstance(value,(int,float)) else value
    m["period"]=period
    if previous is not None:m["previous"]=round(previous,2)
    if direction is None and previous is not None:
        direction="↑" if value>previous else "↓" if value<previous else "→"
    if direction is not None:m["direction"]=direction
    if source:m["source"]=source

data=json.loads(PATH.read_text(encoding="utf-8"))
metrics=data["metrics"]

series_map={
    "real_yield":("DFII10","FRED / Federal Reserve DFII10"),
    "dxy":("DTWEXBGS","FRED / Federal Reserve：Nominal Broad U.S. Dollar Index（DXY免费代理）"),
    "us_unemployment":("UNRATE","FRED / BLS"),
}
for mid,(sid,src) in series_map.items():
    try:
        vals=fred_csv(sid)
        if vals:
            (date,val)=vals[-1]; prev=vals[-2][1] if len(vals)>1 else None
            update_metric(metrics,mid,val,date,prev,source=src)
    except Exception as e:
        print(f"{sid} update failed: {e}")

# FEDFUNDS 是月度有效联邦基金利率；网页原先的目标区间仍可手工维护。
try:
    vals=fred_csv("FEDFUNDS")
    if vals:
        date,val=vals[-1]; prev=vals[-2][1] if len(vals)>1 else None
        # 另附到 impact 里，不覆盖目标区间
        m=next(x for x in metrics if x["id"]=="fed_rate")
        m["impact"]=f"FRED 最新有效联邦基金利率约 {val:.2f}%；目标区间仍以美联储会议声明为准。"
except Exception as e:
    print("FEDFUNDS update failed:",e)

cn=timezone(timedelta(hours=8))
data["updated_at"]=datetime.now(cn).strftime("%Y-%m-%d %H:%M +08:00")
PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print("updated",PATH)
