import os
import json
import hmac
import hashlib
from datetime import datetime
from pathlib import Path
from aiohttp import web
import sys

sys.path.insert(0, str(Path(__file__).parent))

from database import get_site, get_user_sites, update_site_content, get_or_create_tenant
from builder import generate_site
from analytics import track_view, track_event

BUILDER_SECRET = os.getenv("BUILDER_SECRET", "your-secret-key-change-this")
SITES_DIR = Path("sites")

def verify_telegram_init_data(init_data: str) -> dict:
    try:
        parsed = dict(x.split('=') for x in init_data.split('&') if '=' in x)
        hash_received = parsed.pop('hash', '')
        
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(
            b"WebAppData",
            BUILDER_SECRET.encode(),
            hashlib.sha256
        ).digest()
        
        hash_calculated = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if hash_calculated != hash_received:
            return None
        
        auth_date = int(parsed.get('auth_date', 0))
        if datetime.now().timestamp() - auth_date > 86400:
            return None
            
        return parsed
    except Exception:
        return None

async def get_site_api(request):
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    verified = verify_telegram_init_data(init_data)
    
    if not verified:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    
    slug = request.match_info['slug']
    site = get_site(slug)
    
    if not site:
        return web.json_response({'error': 'Site not found'}, status=404)
    
    user = json.loads(verified.get('user', '{}'))
    telegram_id = user.get('id')
    tenant = get_or_create_tenant(telegram_id, user.get('username'))
    
    if site[1] != tenant[0]:
        return web.json_response({'error': 'Forbidden'}, status=403)
    
    content = json.loads(site[5])
    
    return web.json_response({
        'slug': site[3],
        'name': site[4],
        'type': site[4],
        'content': content,
        'custom_domain': site[8],
        'is_published': bool(site[7]),
        'created_at': site[9],
        'updated_at': site[10]
    })

async def save_site_api(request):
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    verified = verify_telegram_init_data(init_data)
    
    if not verified:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    
    slug = request.match_info['slug']
    site = get_site(slug)
    
    if not site:
        return web.json_response({'error': 'Site not found'}, status=404)
    
    user = json.loads(verified.get('user', '{}'))
    telegram_id = user.get('id')
    tenant = get_or_create_tenant(telegram_id, user.get('username'))
    
    if site[1] != tenant[0]:
        return web.json_response({'error': 'Forbidden'}, status=403)
    
    try:
        data = await request.json()
        content = data.get('content', {})
        code_mode = data.get('codeMode', False)
        custom_html = data.get('customHtml', None)
        
        existing = json.loads(site[5])
        
        if code_mode and custom_html:
            existing['custom_html'] = custom_html
            existing['code_mode'] = True
        else:
            existing.update(content)
            existing.pop('custom_html', None)
            existing.pop('code_mode', None)
        
        update_site_content(slug, existing)
        
        site_type = site[4]
        generate_site(slug, site_type, existing)
        
        base_url = os.getenv("BASE_URL", "http://localhost:8080")
        site_url = f"{base_url}/sites/{slug}"
        
        return web.json_response({
            'success': True,
            'url': site_url,
            'message': 'Site updated successfully'
        })
        
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def upload_image_api(request):
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    verified = verify_telegram_init_data(init_data)
    
    if not verified:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    
    slug = request.match_info['slug']
    reader = await request.multipart()
    
    field = await reader.next()
    if field.name != 'image':
        return web.json_response({'error': 'No image field'}, status=400)
    
    filename = field.filename or 'upload.jpg'
    site_images_dir = SITES_DIR / slug / "images"
    site_images_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{timestamp}_{filename}"
    file_path = site_images_dir / safe_name
    
    with open(file_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    
    relative_path = f"images/{safe_name}"
    
    return web.json_response({
        'success': True,
        'url': relative_path,
        'filename': safe_name
    })

async def track_view_api(request):
    try:
        data = await request.json()
        ip = request.headers.get('X-Forwarded-For', request.remote) or 'unknown'
        track_view(
            data.get('slug'),
            ip.split(',')[0].strip(),
            data.get('ua', ''),
            data.get('ref', ''),
            data.get('path', '/')
        )
        return web.Response(status=204)
    except:
        return web.Response(status=200)

async def track_event_api(request):
    try:
        data = await request.json()
        track_event(
            data.get('slug'),
            'anonymous',
            data.get('type'),
            {'element': data.get('element')}
        )
        return web.Response(status=204)
    except:
        return web.Response(status=200)

async def builder_config(request):
    return web.json_response({
        'apiBase': os.getenv('BASE_URL', 'http://localhost:8080'),
        'botUsername': os.getenv('BOT_USERNAME', 'YourBot')
    })

def setup_api_routes(app):
    app.router.add_get('/api/config', builder_config)
    app.router.add_get('/api/site/{slug}', get_site_api)
    app.router.add_post('/api/site/{slug}/save', save_site_api)
    app.router.add_post('/api/site/{slug}/upload', upload_image_api)
    app.router.add_post('/api/track', track_view_api)
    app.router.add_post('/api/track/event', track_event_api)