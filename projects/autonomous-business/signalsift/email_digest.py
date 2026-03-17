#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
ALERTS = BASE / 'alerts.json'
OUT = BASE / 'daily-digest.md'

alerts = json.loads(ALERTS.read_text()) if ALERTS.exists() else []
recent = alerts[-20:]
lines = [f'# SignalSift Daily Digest ({datetime.now().strftime("%Y-%m-%d")})', '']
if not recent:
    lines.append('No alerts yet.')
else:
    for alert in reversed(recent):
        lines.append(f"## {alert.get('company', 'Unknown')} — {alert.get('severity', 'low').upper()}")
        lines.append(f"- URL: {alert.get('url', '')}")
        lines.append(f"- Signals: {'; '.join(alert.get('signals', []))}")
        lines.append(f"- Angle: {alert.get('angle', '')}")
        lines.append(f"- Created: {alert.get('createdAt', '')}")
        lines.append('')
OUT.write_text('\n'.join(lines))
print(f'Wrote {OUT}')
