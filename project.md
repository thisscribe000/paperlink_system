# Telegram Land — Project Roadmap

## Vision
Build a Telegram-native hosting platform where users can create websites, blogs, shops, and Link-in-Bio pages entirely through Telegram chat. Eventually expand to domain registration and email hosting.

## Core Concept
- **Role**: Infrastructure provider (like Namecheap + Vercel + Gmail)
- **Target Audience**: IG sellers, entrepreneurs, small businesses
- **Platform**: Telegram as the management interface
- **Hosting**: Self-hosted with Cloudflare edge

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TELEGRAM CLIENT LAYER                     │
│  (User chats with Bot, Inline queries, Web App opens)       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 YOUR ORCHESTRATION LAYER                     │
│  Telegram Bot API ←→ Your Backend (Python)                 │
│  Webhook handling, command parsing, state management       │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│   BUILDER    │ │  DEPLOY  │ │   MANAGE     │
│   ENGINE     │ │  ENGINE  │ │   DASHBOARD  │
│(Visual editor│ │(CDN/SSL/ │ │(Analytics,   │
│/CLI/Templates│ │  Domain) │ │  Billing)    │
└──────┬───────┘ └────┬─────┘ └──────┬───────┘
       │              │              │
       └──────────────┼──────────────┘
                      ▼
        ┌─────────────────────────┐
        │    HOSTING LAYER        │
        │  (Cloudflare + Local)   │
        └─────────────────────────┘
```

## Features (Phase by Phase)

### Phase 1: Foundation ✅ (COMPLETE)
- [x] Bot scaffolding with conversation FSM
- [x] Basic template engine (Landing, Blog, Shop)
- [x] Static site deployment
- [x] Subdomain auto-provisioning
- [x] SQLite database (tenants, sites)

### Phase 2: Builder Tools ✅ (COMPLETE)
- [x] Mini App visual editor (React-based)
- [x] Component library (20+ blocks)
- [x] Media manager (Telegram file integration)
- [x] Preview system
- [x] Code editor (Monaco)

### Phase 3: Domain Layer ✅ (COMPLETE)
- [x] WHOIS availability checker (self-owned)
- [x] Response parser
- [x] Caching layer
- [x] Suggestion algorithm
- [ ] Reseller bridge (for actual purchases)
- [ ] PowerDNS integration

### Phase 4: Analytics ✅ (COMPLETE)
- [x] Page view tracking
- [x] Device breakdown
- [x] Referrer tracking
- [x] Event tracking
- [x] /stats command

### Phase 5: IG Link-in-Bio ✅ (COMPLETE)
- [x] Mobile-first template
- [x] Social links (IG, WhatsApp, TikTok)
- [x] Product grid
- [x] Multiple link buttons
- [x] Click tracking

### Phase 6: Email Hosting (PENDING)
- [ ] Mailu Docker deployment
- [ ] Email account API
- [ ] Webmail interface
- [ ] SMTP/IMAP access
- [ ] Catch-all, aliases

### Phase 7: Domain Marketplace (PENDING)
- [ ] Reseller API integration
- [ ] Shopping cart flow
- [ ] Payment processing
- [ ] Domain provisioning

### Phase 8: Payments (PENDING)
- [ ] Telegram Stars integration
- [ ] Stripe checkout
- [ ] Order management
- [ ] Subscription billing

## Tech Stack

### Backend
- **Language**: Python 3.10+
- **Bot Framework**: python-telegram-bot 21.x
- **Web Framework**: aiohttp
- **Database**: SQLite (migrate to PostgreSQL later)
- **Templates**: Jinja2

### Frontend (Builder)
- **Framework**: React 18 + Vite
- **Telegram SDK**: @vkruglikov/react-telegram-web-app
- **Code Editor**: Monaco Editor
- **Icons**: Lucide React

### Infrastructure
- **Edge/CDN**: Cloudflare (free tier)
- **App Server**: Hetzner/Vultr ($5-10/mo)
- **File Storage**: Cloudflare R2 or local
- **DNS**: PowerDNS (self-hosted) or Cloudflare API

## Revenue Model

| Tier | Features | Price |
|------|----------|-------|
| Free | Subdomain only, 3 projects, Tland branding | $0 |
| Developer | Custom domain, 10 projects, API access | $9/mo |
| Merchant | Shop features, payments, analytics | $29/mo |
| Enterprise | White-label, dedicated IP, SLA | Custom |

### Domain Sales
- Cost: ~$9 wholesale (various TLDs)
- Sell: $15-25 (depends on TLD)
- Margin: $6-16 per domain

### Email Hosting
- Free with domain purchase
- Or $2/user/month for standalone

## File Structure

```
telegram-land/
├── bot.py                      # Main Telegram bot
├── database.py                  # SQLite models
├── builder.py                  # HTML generator
├── image_handler.py            # Image upload/download
├── domain_manager.py            # Custom domain + SSL
├── domain_checker.py            # WHOIS availability
├── analytics.py                # Page view tracking
├── server.py                   # aiohttp web server
├── api.py                      # REST API endpoints
├── dns_manager.py              # PowerDNS wrapper
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables
├── templates/                  # HTML templates
│   ├── landing.html
│   ├── shop.html
│   ├── blog.html
│   └── iglink.html
├── builder/                    # React builder app
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       └── components/
│           ├── VisualBuilder.jsx
│           ├── CodeEditor.jsx
│           └── LivePreview.jsx
├── sites/                      # Generated websites (auto-created)
├── certs/                      # SSL certificates (auto-created)
└── telegram_land.db           # Database (auto-created)
```

## Deployment

### Development (Local)
```bash
# Terminal 1 — Run the bot
cd telegram-land
python bot.py

# Terminal 2 — Run the server
python server.py
```

### Production (VPS)
```bash
# Install dependencies
apt update && apt install python3 python3-pip certbot
pip install -r requirements.txt

# Run behind nginx (recommended)
python server.py --port 8080

# Nginx config for SSL termination
```

## Commands Reference

### User Commands
- `/start` — Main menu
- `/new` — Create new project
- `/sites` — List your projects
- `/edit <slug>` — Edit site
- `/stats <slug>` — View analytics
- `/check <domain>` — Check domain availability
- `/connect <slug> <domain>` — Connect custom domain
- `/status <slug>` — Domain health

### Bot Father Commands
```
start - Main menu
new - Create new project
sites - List your projects
edit - Edit site (opens builder)
stats - View analytics
check - Check domain availability
connect - Link custom domain
status - Domain health help - Show all commands
cancel - Cancel operation
```

## Development Roadmap

### Immediate (Week 1-2)
- [ ] Deploy locally, test all features
- [ ] Get 5 IG sellers to test
- [ ] Fix any bugs found

### Short-term (Month 1)
- [ ] Add more templates
- [ ] Polish the builder UI
- [ ] Implement domain purchase flow

### Medium-term (Month 2-3)
- [ ] Deploy to production VPS
- [ ] Add email hosting
- [ ] Add payment processing

### Long-term (Month 4-6)
- [ ] Apply for ICANN accreditation (if revenue justifies)
- [ ] Migrate to managed PostgreSQL
- [ ] Scale to 1000+ users

## Contributing

This is a private project. Development happens locally with the team.

## License

Proprietary — All rights reserved