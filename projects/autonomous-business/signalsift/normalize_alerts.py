#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ALERTS = BASE / 'alerts.json'

alerts = json.loads(ALERTS.read_text()) if ALERTS.exists() else []
normalized = []
seen = set()
for alert in alerts:
    alert.setdefault('severity', 'low')
    key = (alert.get('company'), alert.get('url'), tuple(alert.get('signals', [])), alert.get('createdAt'))
    if key in seen:
        continue
    seen.add(key)
    normalized.append(alert)
ALERTS.write_text(json.dumps(normalized[-300:], indent=2))
print(f'Normalized {ALERTS}')
