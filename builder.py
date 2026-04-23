import json
from pathlib import Path
from jinja2 import Template

TEMPLATES_DIR = Path("templates")
SITES_DIR = Path("sites")

TEMPLATES_DIR.mkdir(exist_ok=True)
SITES_DIR.mkdir(exist_ok=True)

LANDING_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | {{ site_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0a0a; color: #fff; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
        
        nav { padding: 24px 0; position: fixed; width: 100%; top: 0; background: rgba(10,10,10,0.9); backdrop-filter: blur(20px); z-index: 100; border-bottom: 1px solid #222; }
        .nav-content { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 24px; font-weight: 800; color: {{ brand_color }}; display: flex; align-items: center; gap: 12px; }
        .logo img { height: 40px; width: 40px; object-fit: cover; border-radius: 8px; }
        .nav-links { display: flex; gap: 32px; }
        .nav-links a { color: #888; text-decoration: none; font-weight: 500; transition: color 0.3s; }
        .nav-links a:hover { color: #fff; }
        
        .hero { padding: 160px 0 100px; text-align: center; background: radial-gradient(ellipse at top, #1a1a2e 0%, #0a0a0a 70%); }
        .hero h1 { font-size: 72px; font-weight: 800; line-height: 1.1; margin-bottom: 24px; background: linear-gradient(135deg, #fff 0%, #888 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 22px; color: #666; max-width: 600px; margin: 0 auto 40px; line-height: 1.6; }
        .cta-group { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
        .btn-primary { padding: 16px 36px; background: {{ brand_color }}; color: #fff; text-decoration: none; border-radius: 12px; font-weight: 600; font-size: 16px; transition: all 0.3s; border: none; cursor: pointer; display: inline-block; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 20px 40px rgba(0,136,204,0.3); }
        .btn-secondary { padding: 16px 36px; background: transparent; color: #fff; text-decoration: none; border-radius: 12px; font-weight: 600; font-size: 16px; border: 1px solid #333; transition: all 0.3s; display: inline-block; }
        .btn-secondary:hover { border-color: {{ brand_color }}; }
        
        .features { padding: 100px 0; }
        .section-header { text-align: center; margin-bottom: 64px; }
        .section-header h2 { font-size: 40px; margin-bottom: 16px; }
        .section-header p { color: #666; font-size: 18px; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 24px; }
        .feature-card { background: #111; border: 1px solid #222; border-radius: 16px; padding: 40px; transition: all 0.3s; }
        .feature-card:hover { border-color: {{ brand_color }}; transform: translateY(-4px); }
        .feature-icon { width: 48px; height: 48px; background: {{ brand_color }}20; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; font-size: 24px; }
        .feature-card h3 { font-size: 20px; margin-bottom: 12px; }
        .feature-card p { color: #666; line-height: 1.6; }
        
        {% if images %}
        .gallery { padding: 100px 0; background: #111; }
        .gallery-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 40px; }
        .gallery-item { border-radius: 16px; overflow: hidden; aspect-ratio: 16/10; }
        .gallery-item img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
        .gallery-item:hover img { transform: scale(1.05); }
        {% endif %}
        
        footer { padding: 60px 0 40px; border-top: 1px solid #222; text-align: center; }
        footer p { color: #555; margin-bottom: 16px; }
        .socials { display: flex; gap: 20px; justify-content: center; margin-top: 20px; }
        .socials a { color: #666; text-decoration: none; font-size: 20px; transition: color 0.3s; }
        .socials a:hover { color: {{ brand_color }}; }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 40px; }
            .hero { padding: 120px 0 60px; }
            .nav-links { display: none; }
            .feature-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <nav>
        <div class="container nav-content">
            <div class="logo">
                {% if logo_url %}<img src="{{ logo_url }}" alt="logo">{% endif %}
                {{ site_name }}
            </div>
            <div class="nav-links">
                <a href="#features">Features</a>
                <a href="#gallery">Gallery</a>
                <a href="#contact">Contact</a>
            </div>
        </div>
    </nav>

    <section class="hero">
        <div class="container">
            <h1>{{ hero_text or title }}</h1>
            <p>{{ hero_subtext or description }}</p>
            <div class="cta-group">
                <a href="{{ cta_link }}" class="btn-primary">{{ cta_text }}</a>
                <a href="#features" class="btn-secondary">Learn More</a>
            </div>
        </div>
    </section>

    <section class="features" id="features">
        <div class="container">
            <div class="section-header">
                <h2>Why Choose Us</h2>
                <p>Built with precision and care</p>
            </div>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Lightning Fast</h3>
                    <p>Optimized for speed and performance across all devices and networks.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Secure by Default</h3>
                    <p>Enterprise-grade security with SSL encryption and DDoS protection.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎨</div>
                    <h3>Beautiful Design</h3>
                    <p>Pixel-perfect interfaces crafted with modern design principles.</p>
                </div>
            </div>
        </div>
    </section>

    {% if images %}
    <section class="gallery" id="gallery">
        <div class="container">
            <div class="section-header">
                <h2>Gallery</h2>
                <p>See what we've built</p>
            </div>
            <div class="gallery-grid">
                {% for img in images %}
                <div class="gallery-item">
                    <img src="{{ img }}" alt="Gallery image" loading="lazy">
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    <footer id="contact">
        <div class="container">
            <p>&copy; {{ year }} {{ site_name }}. Built on Telegram Land</p>
            {% if contact_email %}
            <p><a href="mailto:{{ contact_email }}" style="color: #666; text-decoration: none;">{{ contact_email }}</a></p>
            {% endif %}
            <div class="socials">
                <a href="#">X</a>
                <a href="#">Instagram</a>
                <a href="#">WhatsApp</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""

SHOP_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ site_name }} — Shop</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: #fafafa; color: #111; }
        .container { max-width: 1400px; margin: 0 auto; padding: 0 24px; }
        
        .top-bar { background: {{ brand_color }}; color: #fff; padding: 12px 0; text-align: center; font-size: 14px; font-weight: 500; }
        header { padding: 20px 0; background: #fff; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 100; }
        .header-content { display: flex; justify-content: space-between; align-items: center; }
        .brand { font-size: 28px; font-weight: 800; color: #111; display: flex; align-items: center; gap: 12px; }
        .brand img { height: 40px; border-radius: 8px; }
        .cart-btn { background: #111; color: #fff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 14px; }
        
        .shop-hero { padding: 80px 0; text-align: center; background: linear-gradient(180deg, #fff 0%, #f5f5f5 100%); }
        .shop-hero h1 { font-size: 56px; font-weight: 800; margin-bottom: 16px; }
        .shop-hero p { font-size: 20px; color: #666; max-width: 500px; margin: 0 auto; }
        
        .products { padding: 60px 0 100px; }
        .products-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
        .products-header h2 { font-size: 32px; }
        
        .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 32px; }
        .product-card { background: #fff; border-radius: 16px; overflow: hidden; border: 1px solid #eee; transition: all 0.3s; }
        .product-card:hover { box-shadow: 0 20px 40px rgba(0,0,0,0.08); transform: translateY(-4px); }
        .product-image { aspect-ratio: 4/3; background: #f5f5f5; display: flex; align-items: center; justify-content: center; font-size: 48px; overflow: hidden; }
        .product-image img { width: 100%; height: 100%; object-fit: cover; }
        .product-info { padding: 24px; }
        .product-info h3 { font-size: 18px; margin-bottom: 8px; }
        .product-info p { color: #666; font-size: 14px; line-height: 1.5; margin-bottom: 16px; }
        .product-footer { display: flex; justify-content: space-between; align-items: center; }
        .price { font-size: 24px; font-weight: 700; color: {{ brand_color }}; }
        .add-to-cart { background: #111; color: #fff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
        .add-to-cart:hover { background: {{ brand_color }}; }
        
        footer { background: #111; color: #888; padding: 60px 0 40px; }
        .footer-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; margin-bottom: 40px; }
        .footer-col h4 { color: #fff; margin-bottom: 20px; font-size: 16px; }
        .footer-col a { display: block; color: #666; text-decoration: none; margin-bottom: 12px; transition: color 0.3s; }
        .footer-col a:hover { color: #fff; }
        .footer-bottom { border-top: 1px solid #333; padding-top: 24px; text-align: center; font-size: 14px; }
        
        @media (max-width: 768px) {
            .shop-hero h1 { font-size: 36px; }
            .products-header { flex-direction: column; gap: 16px; align-items: flex-start; }
        }
    </style>
</head>
<body>
    <div class="top-bar">Free shipping on orders over $50</div>
    
    <header>
        <div class="container header-content">
            <div class="brand">
                {% if logo_url %}<img src="{{ logo_url }}" alt="logo">{% endif %}
                {{ site_name }}
            </div>
            <a href="#" class="cart-btn">Cart (0)</a>
        </div>
    </header>

    <section class="shop-hero">
        <div class="container">
            <h1>{{ hero_text or title }}</h1>
            <p>{{ hero_subtext or description }}</p>
        </div>
    </section>

    <section class="products">
        <div class="container">
            <div class="products-header">
                <h2>All Products</h2>
            </div>
            <div class="product-grid">
                {% for product in products %}
                <div class="product-card">
                    <div class="product-image">
                        {% if product.image %}
                        <img src="{{ product.image }}" alt="{{ product.name }}">
                        {% else %}
                        📦
                        {% endif %}
                    </div>
                    <div class="product-info">
                        <h3>{{ product.name }}</h3>
                        <p>{{ product.description }}</p>
                        <div class="product-footer">
                            <span class="price">${{ product.price }}</span>
                            <button class="add-to-cart">Add to Cart</button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4>Shop</h4>
                    <a href="#">All Products</a>
                    <a href="#">New Arrivals</a>
                    <a href="#">Best Sellers</a>
                </div>
                <div class="footer-col">
                    <h4>Support</h4>
                    <a href="#">FAQ</a>
                    <a href="#">Shipping</a>
                    <a href="#">Returns</a>
                </div>
                <div class="footer-col">
                    <h4>Company</h4>
                    <a href="#">About</a>
                    <a href="#">Contact</a>
                    <a href="#">Blog</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {{ year }} {{ site_name }}. Built on Telegram Land</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

IGLINK_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ site_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        :root {
            --accent: {{ brand_color }};
            --bg: #000;
            --card: #111;
            --text: #fff;
            --muted: #888;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding-bottom: 40px;
        }
        
        .profile {
            text-align: center;
            padding: 40px 24px 24px;
        }
        
        .avatar {
            width: 96px;
            height: 96px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--accent);
            margin-bottom: 16px;
        }
        
        .avatar-placeholder {
            width: 96px;
            height: 96px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), #333);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            font-weight: 700;
            margin: 0 auto 16px;
        }
        
        .profile h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .profile p {
            color: var(--muted);
            font-size: 15px;
            line-height: 1.5;
            max-width: 300px;
            margin: 0 auto;
        }
        
        .verified {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: var(--accent);
            color: #fff;
            font-size: 11px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
            margin-top: 12px;
        }
        
        .socials {
            display: flex;
            justify-content: center;
            gap: 16px;
            padding: 0 24px 24px;
        }
        
        .social-btn {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--card);
            border: 1px solid #222;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text);
            text-decoration: none;
            font-size: 20px;
            transition: all 0.2s;
        }
        
        .social-btn:hover {
            background: var(--accent);
            border-color: var(--accent);
            transform: scale(1.1);
        }
        
        .links {
            padding: 0 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .link-btn {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 16px 20px;
            background: var(--card);
            border: 1px solid #222;
            border-radius: 14px;
            color: var(--text);
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.2s;
            position: relative;
            overflow: hidden;
        }
        
        .link-btn::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: var(--accent);
            opacity: 0;
            transition: opacity 0.2s;
        }
        
        .link-btn:hover::before {
            opacity: 1;
        }
        
        .link-btn:hover {
            background: #1a1a1a;
            transform: translateX(4px);
        }
        
        .link-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: #1a1a1a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }
        
        .link-text {
            flex: 1;
        }
        
        .link-arrow {
            color: var(--muted);
            font-size: 18px;
        }
        
        {% if products %}
        .section {
            padding: 32px 20px 0;
        }
        
        .section-title {
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--muted);
            margin-bottom: 16px;
            padding: 0 4px;
        }
        
        .product-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        
        .product-card {
            background: var(--card);
            border: 1px solid #222;
            border-radius: 14px;
            overflow: hidden;
            transition: all 0.2s;
        }
        
        .product-card:hover {
            border-color: #333;
            transform: translateY(-2px);
        }
        
        .product-img {
            aspect-ratio: 1;
            background: #1a1a1a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            overflow: hidden;
        }
        
        .product-img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .product-info {
            padding: 12px;
        }
        
        .product-name {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .product-price {
            color: var(--accent);
            font-weight: 700;
            font-size: 16px;
        }
        {% endif %}
        
        .footer {
            text-align: center;
            padding: 40px 24px 20px;
        }
        
        .footer p {
            font-size: 12px;
            color: #333;
        }
        
        .footer a {
            color: #444;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="profile">
        {% if logo_url %}
        <img src="{{ logo_url }}" alt="{{ site_name }}" class="avatar">
        {% else %}
        <div class="avatar-placeholder">{{ site_name[0] }}</div>
        {% endif %}
        <h1>{{ site_name }}</h1>
        <p>{{ hero_subtext or description }}</p>
        <div class="verified">
            <span>✓</span> Verified Shop
        </div>
    </div>
    
    <div class="socials">
        {% if social_links.instagram %}
        <a href="{{ social_links.instagram }}" class="social-btn" target="_blank">📸</a>
        {% endif %}
        {% if social_links.whatsapp %}
        <a href="{{ social_links.whatsapp }}" class="social-btn" target="_blank">💬</a>
        {% endif %}
        {% if social_links.tiktok %}
        <a href="{{ social_links.tiktok }}" class="social-btn" target="_blank">🎵</a>
        {% endif %}
        {% if social_links.twitter %}
        <a href="{{ social_links.twitter }}" class="social-btn" target="_blank">𝕏</a>
        {% endif %}
    </div>
    
    <div class="links">
        {% for link in links %}
        <a href="{{ link.url }}" class="link-btn" target="_blank" data-track="link_{{ loop.index }}">
            <div class="link-icon">{{ link.icon or '🔗' }}</div>
            <span class="link-text">{{ link.title }}</span>
            <span class="link-arrow">›</span>
        </a>
        {% endfor %}
        
        {% if not links %}
        <a href="#" class="link-btn">
            <div class="link-icon">🛍️</div>
            <span class="link-text">Shop All Products</span>
            <span class="link-arrow">›</span>
        </a>
        <a href="#" class="link-btn">
            <div class="link-icon">💬</div>
            <span class="link-text">Chat on WhatsApp</span>
            <span class="link-arrow">›</span>
        </a>
        <a href="#" class="link-btn">
            <div class="link-icon">📍</div>
            <span class="link-text">Store Location</span>
            <span class="link-arrow">›</span>
        </a>
        {% endif %}
    </div>
    
    {% if products %}
    <div class="section">
        <div class="section-title">Featured Products</div>
        <div class="product-grid">
            {% for product in products %}
            <div class="product-card">
                <div class="product-img">
                    {% if product.image %}
                    <img src="{{ product.image }}" alt="{{ product.name }}">
                    {% else %}
                    📦
                    {% endif %}
                </div>
                <div class="product-info">
                    <div class="product-name">{{ product.name }}</div>
                    <div class="product-price">${{ product.price }}</div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    <div class="footer">
        <p>Built with <a href="https://t.me/YourBot">Telegram Land</a></p>
    </div>
    
    <script>
    (function() {
        const data = { slug: '{{ slug }}', ref: document.referrer, ua: navigator.userAgent };
        fetch('/api/track', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data) }).catch(()=>{});
        
        document.querySelectorAll('[data-track]').forEach(el => {
            el.addEventListener('click', () => {
                fetch('/api/track/event', { 
                    method: 'POST', 
                    headers: {'Content-Type':'application/json'}, 
                    body: JSON.stringify({ slug: '{{ slug }}', type: 'link_click', element: el.dataset.track })
                }).catch(()=>{});
            });
        });
    })();
    </script>
</body>
</html>
"""

def load_template(template_name: str) -> Template:
    template_path = TEMPLATES_DIR / f"{template_name}.html"
    if not template_path.exists():
        if template_name == "shop":
            return Template(SHOP_TEMPLATE)
        elif template_name == "blog":
            return Template(BLOG_TEMPLATE)
        elif template_name == "iglink":
            return Template(IGLINK_TEMPLATE)
        return Template(LANDING_TEMPLATE)
    return Template(template_path.read_text())

def generate_site(slug: str, site_type: str, content: dict):
    template = load_template(site_type)
    
    context = {
        "site_name": content.get("name", "My Site"),
        "title": content.get("title", "Welcome"),
        "description": content.get("description", ""),
        "hero_text": content.get("hero_text", ""),
        "hero_subtext": content.get("hero_subtext", ""),
        "cta_text": content.get("cta_text", "Get Started"),
        "cta_link": content.get("cta_link", "#"),
        "products": content.get("products", []),
        "posts": content.get("posts", []),
        "links": content.get("links", []),
        "stories": content.get("stories", []),
        "brand_color": content.get("brand_color", "#0088cc"),
        "logo_url": content.get("logo_url", ""),
        "contact_email": content.get("contact_email", ""),
        "social_links": content.get("social_links", {}),
        "images": content.get("images", []),
        "year": 2026,
        "slug": slug
    }
    
    html = template.render(**context)
    
    site_dir = SITES_DIR / slug
    site_dir.mkdir(exist_ok=True)
    
    index_path = site_dir / "index.html"
    index_path.write_text(html, encoding='utf-8')
    
    return str(index_path)