#!/usr/bin/env python3
import json
import hashlib
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
WATCHLIST = BASE / 'watchlist.json'
SNAPSHOTS = BASE / 'snapshots.json'
ALERTS = BASE / 'alerts.json'
USER_AGENT = 'SignalSiftBot/0.1 (+local prototype)'


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def fetch_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    return html


def extract_text(html):
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    title = re.sub(r'\s+', ' ', title_match.group(1)).strip() if title_match else ''

    meta_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
    meta = re.sub(r'\s+', ' ', meta_match.group(1)).strip() if meta_match else ''

    body = re.sub(r'<script.*?</script>', ' ', html, flags=re.I | re.S)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.I | re.S)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    excerpt = body[:800]
    return title, meta, excerpt


def fingerprint(title, meta, excerpt):
    payload = f'{title}\n{meta}\n{excerpt}'.encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def summarize_changes(previous, current):
    signals = []
    if not previous:
        signals.append('initial snapshot created')
        return signals
    if previous['title'] != current['title']:
        signals.append('title changed')
    if previous['meta'] != current['meta']:
        signals.append('meta description changed')
    if previous['fingerprint'] != current['fingerprint']:
        signals.append('page content changed')
    return signals


def sales_angle(company, signals):
    if 'title changed' in signals or 'meta description changed' in signals:
        return f'{company} changed site messaging. This can indicate a new offer, repositioning, or active growth initiative worth contacting them about.'
    if 'page content changed' in signals:
        return f'{company} updated site content recently. Good time to pitch SEO, CRO, or demand generation help while priorities are in motion.'
    return f'{company} was added to monitoring. Wait for the next change before outreach.'


def run():
    watchlist = load_json(WATCHLIST, [])
    snapshots = load_json(SNAPSHOTS, [])
    alerts = load_json(ALERTS, [])
    latest_by_url = {item['url']: item for item in snapshots}

    for target in watchlist:
        url = target['url']
        try:
            html = fetch_page(url)
            title, meta, excerpt = extract_text(html)
            current = {
                'company': target['company'],
                'url': url,
                'category': target.get('category', ''),
                'title': title,
                'meta': meta,
                'excerpt': excerpt,
                'fingerprint': fingerprint(title, meta, excerpt),
                'checkedAt': datetime.now(timezone.utc).isoformat()
            }
            previous = latest_by_url.get(url)
            signals = summarize_changes(previous, current)
            latest_by_url[url] = current
            if signals:
                alerts.append({
                    'company': target['company'],
                    'url': url,
                    'signals': signals,
                    'angle': sales_angle(target['company'], signals),
                    'createdAt': current['checkedAt']
                })
        except Exception as exc:
            alerts.append({
                'company': target['company'],
                'url': url,
                'signals': ['fetch failed'],
                'angle': f'Could not fetch {url}: {exc}',
                'createdAt': datetime.now(timezone.utc).isoformat()
            })

    save_json(SNAPSHOTS, list(latest_by_url.values()))
    save_json(ALERTS, alerts[-200:])


if __name__ == '__main__':
    run()
