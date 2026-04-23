import sqlite3
import json
from datetime import datetime, timedelta

DB_PATH = "telegram_land.db"

def init_analytics():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY,
            site_slug TEXT,
            visitor_id TEXT,
            ip_hash TEXT,
            user_agent TEXT,
            referrer TEXT,
            country TEXT,
            device_type TEXT,
            path TEXT DEFAULT '/',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            site_slug TEXT,
            visitor_id TEXT,
            event_type TEXT,
            event_data TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def track_view(site_slug: str, ip: str, user_agent: str, referrer: str, path: str = '/'):
    import hashlib
    
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]
    visitor_id = hashlib.sha256(f"{ip}:{user_agent}".encode()).hexdigest()[:16]
    
    ua = user_agent.lower()
    if 'mobile' in ua:
        device = 'mobile'
    elif 'tablet' in ua:
        device = 'tablet'
    else:
        device = 'desktop'
    
    country = 'Unknown'
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO page_views (site_slug, visitor_id, ip_hash, user_agent, referrer, country, device_type, path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (site_slug, visitor_id, ip_hash, user_agent[:200], referrer[:200], country, device, path))
    
    c.execute('''
        UPDATE sites 
        SET total_views = total_views + 1,
            unique_visitors = (SELECT COUNT(DISTINCT visitor_id) FROM page_views WHERE site_slug = ?)
        WHERE slug = ?
    ''', (site_slug, site_slug))
    
    conn.commit()
    conn.close()

def track_event(site_slug: str, visitor_id: str, event_type: str, event_data: dict = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (site_slug, visitor_id, event_type, event_data)
        VALUES (?, ?, ?, ?)
    ''', (site_slug, visitor_id, event_type, json.dumps(event_data) if event_data else None))
    conn.commit()
    conn.close()

def get_analytics(site_slug: str, days: int = 30):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    since = datetime.now() - timedelta(days=days)
    
    c.execute('''
        SELECT COUNT(*), COUNT(DISTINCT visitor_id) 
        FROM page_views 
        WHERE site_slug = ? AND timestamp > ?
    ''', (site_slug, since))
    total, unique = c.fetchone()
    
    c.execute('''
        SELECT date(timestamp), COUNT(*) 
        FROM page_views 
        WHERE site_slug = ? AND timestamp > ?
        GROUP BY date(timestamp)
        ORDER BY date(timestamp)
    ''', (site_slug, since))
    daily = c.fetchall()
    
    c.execute('''
        SELECT device_type, COUNT(*) 
        FROM page_views 
        WHERE site_slug = ? AND timestamp > ?
        GROUP BY device_type
    ''', (site_slug, since))
    devices = dict(c.fetchall())
    
    c.execute('''
        SELECT referrer, COUNT(*) 
        FROM page_views 
        WHERE site_slug = ? AND timestamp > ? AND referrer != ''
        GROUP BY referrer
        ORDER BY COUNT(*) DESC
        LIMIT 10
    ''', (site_slug, since))
    referrers = c.fetchall()
    
    c.execute('''
        SELECT event_type, COUNT(*) 
        FROM events 
        WHERE site_slug = ? AND timestamp > ?
        GROUP BY event_type
    ''', (site_slug, since))
    events = dict(c.fetchall())
    
    conn.close()
    
    return {
        'period_days': days,
        'total_views': total or 0,
        'unique_visitors': unique or 0,
        'daily_views': daily,
        'devices': devices,
        'referrers': referrers,
        'events': events,
        'ctr': round((events.get('button_click', 0) / max(total, 1)) * 100, 2)
    }

init_analytics()