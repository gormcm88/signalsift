#!/usr/bin/env python3
import json
import hashlib
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html import unescape

BASE = Path(__file__).resolve().parent
WATCHLIST = BASE / 'watchlist.json'
SNAPSHOTS = BASE / 'snapshots.json'
ALERTS = BASE / 'alerts.json'
USER_AGENT = 'SignalSiftBot/0.3 (+local prototype)'


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


def clean_text(text):
    return re.sub(r'\s+', ' ', unescape(text or '')).strip()


def extract_many(pattern, html, flags=0, limit=8):
    matches = re.findall(pattern, html, flags)
    out = []
    for match in matches:
        if isinstance(match, tuple):
            cleaned = tuple(clean_text(x) for x in match)
            if any(cleaned):
                out.append(cleaned)
        else:
            cleaned = clean_text(match)
            if cleaned:
                out.append(cleaned)
    return out[:limit]


def extract_text(html):
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    title = clean_text(title_match.group(1)) if title_match else ''

    meta_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
    meta = clean_text(meta_match.group(1)) if meta_match else ''

    headings = extract_many(r'<h[1-3][^>]*>(.*?)</h[1-3]>', html, re.I | re.S, limit=12)
    links = extract_many(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.I | re.S, limit=40)
    normalized_links = []
    for href, text in links:
        text = clean_text(text)
        href = clean_text(href)
        if text and href and not href.startswith('#'):
            normalized_links.append({'href': href, 'text': text})

    body = re.sub(r'<script.*?</script>', ' ', html, flags=re.I | re.S)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.I | re.S)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = clean_text(body)
    excerpt = body[:1200]
    return title, meta, excerpt, headings, normalized_links[:20]


def fingerprint(*parts):
    payload = '\n'.join(parts).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def added_items(previous_list, current_list, key):
    prev = {item[key] for item in previous_list if item.get(key)}
    return [item for item in current_list if item.get(key) and item[key] not in prev]


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

    new_headings = [h for h in current.get('headings', []) if h not in previous.get('headings', [])]
    if new_headings:
        signals.append(f"new headings added: {', '.join(new_headings[:3])}")

    added_links = added_items(previous.get('links', []), current.get('links', []), 'href')
    if added_links:
        interesting = [x for x in added_links if any(term in x['href'].lower() for term in ['locations', 'location', 'services', 'pricing', 'careers', 'jobs'])]
        if interesting:
            labels = ', '.join(x['href'] for x in interesting[:3])
            signals.append(f'new interesting links detected: {labels}')
    return signals


def score_severity(signals):
    score = 0
    for signal in signals:
        lower = signal.lower()
        if 'new interesting links detected' in lower:
            score += 3
        elif 'new headings added' in lower:
            score += 2
        elif 'title changed' in lower or 'meta description changed' in lower:
            score += 2
        elif 'page content changed' in lower:
            score += 1
        elif 'fetch failed' in lower:
            score += 1
    if score >= 5:
        return 'high'
    if score >= 3:
        return 'medium'
    return 'low'


def sales_angle(company, category, signals, severity):
    text = ' | '.join(signals)
    prefix = {'high': 'High-signal change:', 'medium': 'Meaningful change:', 'low': 'Minor change:'}[severity]
    if 'meta description changed' in text or 'title changed' in text:
        return f'{prefix} {company} changed site messaging. That often means a new offer, repositioning, or active growth push — strong timing for outreach.'
    if 'new interesting links detected' in text:
        return f'{prefix} {company} appears to have added new service/location/careers pages. That can indicate expansion or a change in go-to-market priorities.'
    if 'new headings added' in text:
        return f'{prefix} {company} added new on-page themes or service language. Useful signal for agencies, recruiters, or SDR teams that sell around business change.'
    if 'page content changed' in text:
        return f'{prefix} {company} updated site content recently. Good time to pitch SEO, CRO, recruiting, or demand generation help while priorities are moving.'
    return f'{prefix} {company} was added to monitoring. Wait for the next change before outreach.'


def run():
    watchlist = load_json(WATCHLIST, [])
    snapshots = load_json(SNAPSHOTS, [])
    alerts = load_json(ALERTS, [])
    latest_by_url = {item['url']: item for item in snapshots}

    for target in watchlist:
        url = target['url']
        try:
            html = fetch_page(url)
            title, meta, excerpt, headings, links = extract_text(html)
            current = {
                'company': target['company'],
                'url': url,
                'category': target.get('category', ''),
                'title': title,
                'meta': meta,
                'excerpt': excerpt,
                'headings': headings,
                'links': links,
                'fingerprint': fingerprint(title, meta, excerpt, json.dumps(headings), json.dumps(links)),
                'checkedAt': datetime.now(timezone.utc).isoformat()
            }
            previous = latest_by_url.get(url)
            signals = summarize_changes(previous, current)
            latest_by_url[url] = current
            if signals:
                severity = score_severity(signals)
                alerts.append({
                    'company': target['company'],
                    'url': url,
                    'category': target.get('category', ''),
                    'severity': severity,
                    'signals': signals,
                    'angle': sales_angle(target['company'], target.get('category', ''), signals, severity),
                    'createdAt': current['checkedAt']
                })
        except Exception as exc:
            alerts.append({
                'company': target['company'],
                'url': url,
                'category': target.get('category', ''),
                'severity': 'low',
                'signals': ['fetch failed'],
                'angle': f'Could not fetch {url}: {exc}',
                'createdAt': datetime.now(timezone.utc).isoformat()
            })

    save_json(SNAPSHOTS, list(latest_by_url.values()))
    save_json(ALERTS, alerts[-300:])


if __name__ == '__main__':
    run()
