#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ALERTS = BASE / 'alerts.json'
CSV_OUT = BASE / 'alerts.csv'

alerts = json.loads(ALERTS.read_text()) if ALERTS.exists() else []
with CSV_OUT.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['company', 'url', 'category', 'severity', 'signals', 'angle', 'createdAt'])
    writer.writeheader()
    for a in alerts:
        writer.writerow({
            'company': a.get('company', ''),
            'url': a.get('url', ''),
            'category': a.get('category', ''),
            'severity': a.get('severity', 'low'),
            'signals': ' | '.join(a.get('signals', [])),
            'angle': a.get('angle', ''),
            'createdAt': a.get('createdAt', '')
        })
print(f'Wrote {CSV_OUT}')
