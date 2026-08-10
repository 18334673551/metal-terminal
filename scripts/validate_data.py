from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];c=json.loads((R/'data/catalog.json').read_text(encoding='utf-8'));e=[]
for s in c['sectors']:
  for i in s['indicators']:
    p=R/'data/history'/f"{i['id']}.json"
    if not p.exists(): e.append('missing '+p.name)
    else:
      o=json.loads(p.read_text(encoding='utf-8'))
      if not o.get('data'): e.append('bad '+p.name)
print('\n'.join(e) if e else 'OK');sys.exit(1 if e else 0)
