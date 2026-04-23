# Telegram Land — Project Context

## What is Telegram Land?

Telegram Land is a hosting platform built entirely on Telegram. Users create websites, blogs, shops, and Link-in-Bio pages through chat commands — no coding required. The vision is to become a Telegram-native alternative to Namecheap + Vercel + Gmail.

## Why Telegram First?

1. **Mobile-first audience**: IG sellers live on their phones
2. **No dashboard needed**: Everything happens in chat
3. **Instant notifications**: New orders, analytics alerts — all in Telegram
4. **Viral potential**: Every user shares their site link = free marketing

## Target Audience

### Primary: IG Sellers
- Instagram merchants selling products (clothes, food, services)
- Need: Link in bio, product showcase, WhatsApp ordering
- Pain point: Current options linktree, Carrd — no customization

### Secondary: Small Businesses
- Local shops, freelancers, consultants
- Need: Professional presence, custom domain, email
- Pain point: WordPress/Wix are "too much"

### Tertiary: Developers (Future)
- Want: Code control, custom deployments
- Need: API, CLI, custom domains

## Current Status

The platform is fully functional with:
- ✅ Multi-step site creation via chat
- ✅ 3 templates (Landing, Shop, Blog)
- ✅ IG Link-in-Bio template
- ✅ Image uploads from chat
- ✅ Brand color customization
- ✅ Custom domains + SSL
- ✅ Visual + Code editor (Mini App)
- ✅ Analytics tracking
- ✅ Domain availability checker

What's missing before public launch:
- Domain purchase flow (needs reseller API)
- Email hosting (needs Mailu)
- Payment processing

## Key Decisions

### Own the Stack
- WHOIS queries built from scratch (no third-party API for availability)
- All user-facing code is ours
- Only the actual domain registration goes through reseller

### Concierge First
- Instead of perfect self-service onboarding
- You DM users "Send photos + prices, I'll build it"
- They watch their site get created in real-time
- They share = viral loop starts

### Build Fast, Ship Faster
- Iterate publicly with real users
- Fix bugs in production if needed
- Don't over-engineer before demand is proven

## Technical Decisions

### SQLite over PostgreSQL
- Simplicity for now
- Can migrate to Supabase/Neon at 1000 users
- No managed database cost initially

### Self-hosted over Serverless
- Egress fees kill you at scale on Vercel/AWS
- $10/mo Hetzner beats $100+/mo AWS
- Need root anyway for email hosting later

### Python over Node
- Easier async with aiogram
- Strong template handling (Jinja2)
- Existing libraries for everything

## Competition

| Platform | What They Do | Our Advantage |
|----------|-------------|---------------|
| Carrd | One-page sites | Telegram-native, chat management |
| Linktree | Link in bio | Full site, products, ordering |
| Shopify | E-commerce | Simpler, chat-only |
| WordPress | Blog/website | No "CMS", just chat |
| Namecheap | Domains | Integrated with hosting |

## Terminology

| Term | Meaning |
|------|---------|
| Plot / Site | A user's website |
| Tenant | A user account |
| Blueprint | Template |
| Land Registry | Database |
| Builder Engine | Site generator |
| The Land | The platform itself |

## User Journey

1. **Discovery**: See friend's shop link in IG bio
2. **Interest**: "How did you make this?"
3. **Onboarding**: /start → choose type → answer questions
4. **Creation**: Bot builds site, generates URL
5. **Sharing**: Post link in bio, stories
6. **Growth**: Upgrade to custom domain, add email
7. **Referral**: Tell friends → they become users

## Financial Goals ($)

### Month 1-3: Validation
- Get 50 users (free tier)
- 5 paying for custom domain
- Revenue: $75-125/mo

### Month 4-6: Traction
- 200 users, 20 paying
- Domain sales + premium tiers
- Revenue: $500-1000/mo

### Month 7-12: Scale
- 1000 users, 100 paying
- Email hosting + payments
- Revenue: $3000-5000/mo

## Important Files

| File | Purpose |
|------|---------|
| `bot.py` | Main Telegram bot, all commands |
| `database.py` | SQLite schema and queries |
| `builder.py` | HTML generation from templates |
| `domain_checker.py` | WHOIS availability queries |
| `api.py` | REST endpoints for builder |
| `server.py` | aiohttp web server |
| `templates/*.html` | Site templates |

## Commands to Remember

```bash
# Start bot
python bot.py

# Start web server
python server.py

# Check domain
python -c "from domain_checker import check_domain; print(check_domain('example.com'))"
```

## Contact

This is a private project built by the team.
For questions, refer to the project lead.