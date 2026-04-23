import os
import ssl
from pathlib import Path
from aiohttp import web
import sys

sys.path.insert(0, str(Path(__file__).parent))

SITES_DIR = Path("sites")
CERTS_DIR = Path("certs")
SITES_DIR.mkdir(exist_ok=True)

async def serve_site(request):
    slug = request.match_info.get('slug')
    
    if not slug:
        host = request.headers.get('Host', '').split(':')[0].lower()
        if host not in ('localhost', '127.0.0.1') and not host.replace('.', '').isdigit():
            from database import get_site_by_domain
            site = get_site_by_domain(host)
            if site:
                slug = site[3]
    
    if not slug:
        return web.Response(
            text="<h1>Telegram Land</h1><p>Plot not found. Claim one with @YourBot</p>",
            content_type='text/html',
            status=404
        )
    
    file_path = SITES_DIR / slug / 'index.html'
    
    if file_path.exists():
        content = file_path.read_text()
        
        base_url = os.getenv("BASE_URL", "http://localhost:8080")
        tracking_script = f'''
<script>
(function() {{
    const data = {{
        slug: '{slug}',
        ref: document.referrer,
        ua: navigator.userAgent,
        path: window.location.pathname
    }};
    fetch('{base_url}/api/track', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify(data)
    }}).catch(() => {{}});
    
    document.addEventListener('click', function(e) {{
        if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') {{
            fetch('{base_url}/api/track/event', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    slug: '{slug}',
                    type: 'button_click',
                    element: e.target.innerText.substring(0, 50)
                }})
            }}).catch(() => {{}});
        }}
    }});
}})();
</script>
</body>'''
        
        content = content.replace('</body>', tracking_script)
        
        return web.Response(
            text=content,
            content_type='text/html'
        )
    
    from database import get_site
    from builder import generate_site
    
    site = get_site(slug)
    if site:
        import json
        content = json.loads(site[5])
        generate_site(slug, site[4], content)
        if file_path.exists():
            content = file_path.read_text()
            return web.Response(text=content, content_type='text/html')
    
    return web.Response(
        text="<h1>Plot Under Construction</h1>",
        content_type='text/html',
        status=404
    )

async def serve_image(request):
    slug = request.match_info['slug']
    filename = request.match_info['filename']
    file_path = SITES_DIR / slug / "images" / filename
    if file_path.exists():
        return web.FileResponse(file_path)
    return web.Response(status=404)

async def index(request):
    return web.Response(
        text="""<!DOCTYPE html>
<html><head><title>Telegram Land</title><style>
body{font-family:system-ui;background:#0a0a0a;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center;}
h1{font-size:48px;margin-bottom:16px;}p{color:#666;font-size:18px;}
</style></head>
<body><div><h1>Telegram Land</h1><p>Infrastructure for the Telegram ecosystem</p></div></body>
</html>""",
        content_type='text/html'
    )

async def serve_editor(request):
    editor_path = Path(__file__).parent / 'editor.html'
    if editor_path.exists():
        return web.FileResponse(editor_path)
    return web.Response(text="Editor not found", status=404)

def create_app():
    from api import setup_api_routes
    
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/editor.html', serve_editor)
    app.router.add_get('/sites/{slug}', serve_site)
    app.router.add_get('/sites/{slug}/images/{filename}', serve_image)
    app.router.add_static('/sites/', path=SITES_DIR, show_index=False)
    
    setup_api_routes(app)
    
    return app

if __name__ == '__main__':
    from api import setup_api_routes
    
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/editor.html', serve_editor)
    app.router.add_get('/sites/{slug}', serve_site)
    app.router.add_get('/sites/{slug}/images/{filename}', serve_image)
    app.router.add_static('/sites/', path=SITES_DIR, show_index=False)
    
    setup_api_routes(app)
    
    port = int(os.getenv('PORT', 8080))
    web.run_app(app, host='0.0.0.0', port=port)