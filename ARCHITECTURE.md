# PaperLink Storage

Telegram-native file storage infrastructure for the PaperLink ecosystem.

## Mission

Be the **central file layer** for all PaperLink services — Mail, bots, and future products. Files exist ONCE; everything else references them.

## Principles

- **Link-first**: Everything is a URL reference
- **Lightweight**: No Google Drive clones
- **Telegram-native**: Bot-first, mobile-first
- **Modular**: Storage scales independently from other services
- **Cost-conscious**: Deduplication, expiring files, lazy loading

## Stack

| Component | Technology |
|-----------|------------|
| Runtime | Bun |
| Framework | Hono (TypeScript) |
| Database | SQLite + Prisma |
| Storage | Local (dev) / Cloudflare R2 (prod) |
| Deployment | Cloudflare Workers |

## Project Structure

```
paperlink-storage/
├── src/
│   ├── bot/           # Telegram bot handlers
│   ├── api/            # REST API endpoints
│   ├── storage/        # Storage engine
│   ├── db/             # Prisma & queries
│   └── workers/        # Background jobs
├── prisma/
│   └── schema.prisma   # Database schema
└── storage/            # Local file storage
```

## Current Status

- [ ] Phase 1: Core Storage
  - [ ] Project scaffolding
  - [ ] Database setup
  - [ ] File upload handler
  - [ ] Public links

- [ ] Phase 2: Telegram Bot
- [ ] Phase 3: Access Control
- [ ] Phase 4: Production