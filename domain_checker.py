import socket
import re
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, List

WHOIS_SERVERS = {
    'com': 'whois.verisign-grs.com',
    'net': 'whois.verisign-grs.com',
    'org': 'whois.pir.org',
    'io': 'whois.nic.io',
    'co': 'whois.nic.co',
    'app': 'whois.nic.google',
    'dev': 'whois.nic.google',
    'xyz': 'whois.nic.xyz',
    'shop': 'whois.nic.shop',
    'store': 'whois.nic.store',
    'online': 'whois.nic.online',
    'site': 'whois.nic.site',
    'me': 'whois.nic.me',
    'biz': 'whois.nic.biz',
    'info': 'whois.nic.info',
    'ng': 'whois.nic.net.ng',
    'za': 'whois.co.za',
}

DOMAIN_PRICING = {
    'com': {'register': 12.99, 'renew': 12.99, 'transfer': 12.99},
    'net': {'register': 11.99, 'renew': 11.99, 'transfer': 11.99},
    'org': {'register': 13.99, 'renew': 13.99, 'transfer': 13.99},
    'io': {'register': 34.99, 'renew': 34.99, 'transfer': 34.99},
    'co': {'register': 24.99, 'renew': 24.99, 'transfer': 24.99},
    'app': {'register': 14.99, 'renew': 14.99, 'transfer': 14.99},
    'dev': {'register': 14.99, 'renew': 14.99, 'transfer': 14.99},
    'xyz': {'register': 9.99, 'renew': 9.99, 'transfer': 9.99},
    'shop': {'register': 29.99, 'renew': 29.99, 'transfer': 29.99},
    'store': {'register': 39.99, 'renew': 39.99, 'transfer': 39.99},
    'online': {'register': 29.99, 'renew': 29.99, 'transfer': 29.99},
    'site': {'register': 24.99, 'renew': 24.99, 'transfer': 24.99},
    'me': {'register': 17.99, 'renew': 17.99, 'transfer': 17.99},
    'ng': {'register': 8.99, 'renew': 8.99, 'transfer': 8.99},
    'za': {'register': 6.99, 'renew': 6.99, 'transfer': 6.99},
}

CACHE_DB = "domain_cache.db"

def init_cache():
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS whois_cache (
            domain TEXT PRIMARY KEY,
            available BOOLEAN,
            raw_response TEXT,
            checked_at TIMESTAMP,
            expires_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_cached(domain: str) -> Optional[Dict]:
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    c.execute(
        "SELECT available, raw_response, checked_at FROM whois_cache WHERE domain = ? AND expires_at > ?",
        (domain.lower(), datetime.now())
    )
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'available': bool(row[0]),
            'raw': row[1],
            'cached': True,
            'checked_at': row[2]
        }
    return None

def set_cached(domain: str, available: bool, raw: str):
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    expires = datetime.now() + timedelta(hours=1)
    c.execute('''
        INSERT OR REPLACE INTO whois_cache (domain, available, raw_response, checked_at, expires_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (domain.lower(), available, raw[:5000], datetime.now(), expires))
    conn.commit()
    conn.close()

def whois_query(domain: str, server: str, timeout: int = 10) -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((server, 43))
        
        query = f"{domain}\r\n"
        sock.send(query.encode())
        
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        
        sock.close()
        return response.decode('utf-8', errors='ignore')
        
    except socket.timeout:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def parse_whois_response(raw: str, tld: str) -> Dict:
    raw_lower = raw.lower()
    
    available_patterns = [
        'no match',
        'not found',
        'no entries found',
        'domain not found',
        'status: free',
        'is available',
        'does not exist',
        'no data found',
        'not been registered',
    ]
    
    taken_patterns = [
        'domain name:',
        'registrant',
        'creation date:',
        'updated date:',
        'registrar:',
        'name server:',
        'status:',
    ]
    
    for pattern in available_patterns:
        if pattern in raw_lower:
            return {'available': True, 'reason': pattern}
    
    for pattern in taken_patterns:
        if pattern in raw_lower:
            return {'available': False, 'reason': pattern}
    
    if len(raw.strip()) < 100:
        return {'available': True, 'reason': 'short_response'}
    
    return {'available': False, 'reason': 'uncertain_default'}

def check_domain(domain: str) -> Dict:
    domain = domain.lower().strip()
    
    if not re.match(r'^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]\.[a-z]{2,}$', domain):
        return {'error': 'Invalid domain format. Use: name.com'}
    
    parts = domain.split('.')
    tld = parts[-1]
    
    cached = get_cached(domain)
    if cached:
        return {
            'domain': domain,
            'tld': tld,
            'available': cached['available'],
            'price': DOMAIN_PRICING.get(tld),
            'raw': cached['raw'],
            'cached': True,
            'checked_at': cached['checked_at']
        }
    
    whois_server = WHOIS_SERVERS.get(tld)
    if not whois_server:
        return {
            'domain': domain,
            'tld': tld,
            'error': f'TLD .{tld} not supported yet. Supported: {", ".join(WHOIS_SERVERS.keys())}'
        }
    
    raw = whois_query(domain, whois_server)
    
    if raw.startswith('ERROR') or raw == 'TIMEOUT':
        return {
            'domain': domain,
            'tld': tld,
            'error': f'WHOIS query failed: {raw}'
        }
    
    parsed = parse_whois_response(raw, tld)
    set_cached(domain, parsed['available'], raw)
    
    return {
        'domain': domain,
        'tld': tld,
        'available': parsed['available'],
        'price': DOMAIN_PRICING.get(tld),
        'raw': raw[:200] + '...' if len(raw) > 200 else raw,
        'cached': False,
        'checked_at': datetime.now().isoformat(),
        'parse_reason': parsed['reason']
    }

def suggest_domains(base_name: str) -> List[Dict]:
    tlds = ['com', 'net', 'org', 'co', 'io', 'app', 'xyz', 'shop', 'me']
    suggestions = []
    
    for tld in tlds:
        domain = f"{base_name}.{tld}"
        result = check_domain(domain)
        if 'error' not in result:
            suggestions.append(result)
    
    return suggestions

init_cache()