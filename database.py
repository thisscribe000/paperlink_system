import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "telegram_land.db"
SITES_DIR = Path("sites")
SITES_DIR.mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS tenants (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            plan TEXT DEFAULT 'free',
            sites_count INTEGER DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY,
            tenant_id INTEGER,
            slug TEXT UNIQUE,
            name TEXT,
            site_type TEXT,
            content TEXT,
            custom_domain TEXT,
            is_published BOOLEAN DEFAULT 0,
            total_views INTEGER DEFAULT 0,
            unique_visitors INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_or_create_tenant(telegram_id: int, username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT * FROM tenants WHERE telegram_id = ?", (telegram_id,))
    tenant = c.fetchone()
    
    if not tenant:
        c.execute(
            "INSERT INTO tenants (telegram_id, username) VALUES (?, ?)",
            (telegram_id, username or f"user_{telegram_id}")
        )
        conn.commit()
        c.execute("SELECT * FROM tenants WHERE telegram_id = ?", (telegram_id,))
        tenant = c.fetchone()
    
    conn.close()
    return tenant

def create_site(tenant_id: int, slug: str, name: str, site_type: str, content: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute(
        "INSERT INTO sites (tenant_id, slug, name, site_type, content) VALUES (?, ?, ?, ?, ?)",
        (tenant_id, slug, name, site_type, json.dumps(content))
    )
    
    c.execute(
        "UPDATE tenants SET sites_count = sites_count + 1 WHERE id = ?",
        (tenant_id,)
    )
    
    conn.commit()
    conn.close()
    return True

def get_site(slug: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM sites WHERE slug = ?", (slug,))
    site = c.fetchone()
    conn.close()
    return site

def get_site_by_domain(domain: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM sites WHERE custom_domain = ?", (domain,))
    site = c.fetchone()
    conn.close()
    return site

def get_user_sites(tenant_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM sites WHERE tenant_id = ?", (tenant_id,))
    sites = c.fetchall()
    conn.close()
    return sites

def update_site_content(slug: str, content: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE sites SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE slug = ?",
        (json.dumps(content), slug)
    )
    conn.commit()
    conn.close()

def publish_site(slug: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE sites SET is_published = 1 WHERE slug = ?",
        (slug,)
    )
    conn.commit()
    conn.close()

def set_custom_domain(slug: str, domain: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE sites SET custom_domain = NULL WHERE custom_domain = ?", (domain,))
    c.execute("UPDATE sites SET custom_domain = ? WHERE slug = ?", (domain, slug))
    conn.commit()
    conn.close()

init_db()