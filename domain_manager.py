import os
import re
import asyncio
from pathlib import Path
from database import get_site, set_custom_domain, get_site_by_domain

SITES_DIR = Path("sites")
CERTS_DIR = Path("certs")
CERTS_DIR.mkdir(exist_ok=True)

def is_valid_domain(domain: str) -> bool:
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

async def verify_dns(domain: str, expected_target: str) -> bool:
    try:
        proc = await asyncio.create_subprocess_exec(
            'dig', '+short', domain,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        records = stdout.decode().strip().split('\n')
        
        for record in records:
            record = record.strip()
            if record and (expected_target in record or record in expected_target):
                return True
        return False
    except Exception:
        return False

async def generate_ssl(domain: str) -> bool:
    cert_path = CERTS_DIR / domain
    cert_path.mkdir(exist_ok=True)
    
    key_file = cert_path / 'privkey.pem'
    cert_file = cert_path / 'fullchain.pem'
    
    if key_file.exists() and cert_file.exists():
        return True
    
    try:
        proc = await asyncio.create_subprocess_exec(
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
            '-keyout', str(key_file),
            '-out', str(cert_file),
            '-days', '365',
            '-nodes',
            '-subj', f'/CN={domain}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        return proc.returncode == 0
    except FileNotFoundError:
        return False

def get_ssl_paths(domain: str):
    cert_path = CERTS_DIR / domain
    key = cert_path / 'privkey.pem'
    cert = cert_path / 'fullchain.pem'
    
    if key.exists() and cert.exists():
        return str(key), str(cert)
    return None, None

def get_expected_dns_target() -> str:
    return os.getenv('SERVER_IP', os.getenv('BASE_URL', 'your-server-ip'))