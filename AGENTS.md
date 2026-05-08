# PaperLink System - Agent Context

## What is this?
A file storage system integrated with Telegram. Users upload files via Telegram bot, get shareable links.

## Current Stack
- **Runtime:** Bun
- **Framework:** Hono (works on Node.js and Cloudflare Workers)
- **Database:** SQLite with Prisma
- **Storage:** Local filesystem (./storage folder)
- **Tunnel:** Cloudflare Tunnel (named tunnel "paperlink")
- **Domain:** usepaperlink.site

## Key Files
- `src/index.ts` - Main server entry point
- `src/bot/index.ts` - Telegram bot
- `src/api/` - API routes (upload, files, links, serve)
- `src/storage/` - Storage abstraction (local + Cloudflare R2)
- `.env` - Environment variables

## Important Notes
1. Cloudflare Tunnel is connected but DNS propagation may take time
2. Bot handles files up to 20MB (Telegram API limit)
3. For larger files (20MB+), need to implement Cloudflare R2 storage

## To Run
```bash
# Terminal 1 - Server
bun run dev

# Terminal 2 - Tunnel
cloudflared tunnel run paperlink
```

## Future Work
- Add password-protected links
- Add expiring links
- Add usage tracking/analytics
- Implement R2 storage for large files