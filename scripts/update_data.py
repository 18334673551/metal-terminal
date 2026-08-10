from pathlib import Path
import json
from datetime import date
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'data/history';L=ROOT/'data/latest.json'
latest={'updated':date.today().isoformat(),'is_demo':False,'items':{}}
demo=False
for fp in H.glob('*.json'):
    o=json.loads(fp.read_text(encoding='utf-8'))
    if not o.get('data'): continue
    cur=o['data'][-1][1]; prev=o['data'][-2][1] if len(o['data'])>1 else cur
    ch=((cur-prev)/abs(prev)*100) if prev not in (0,None) else 0
    d=bool(o.get('is_demo',False)); demo|=d
    latest['items'][o['id']]={'value':cur,'change_pct':round(ch,2),'unit':o.get('unit'),'updated':o.get('updated'),'is_demo':d}
latest['is_demo']=demo
L.write_text(json.dumps(latest,ensure_ascii=False,indent=2),encoding='utf-8')
print('rebuilt',L)
