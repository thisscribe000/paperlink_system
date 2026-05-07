# Phase 4: Production

**Goal**: Deploy to Cloudflare and integrate R2 storage.

## Tasks

### Infrastructure
- [x] Set up Cloudflare R2 bucket (bucket: paperlink-files)
- [x] Configure wrangler.toml
- [x] Worker uploaded to Cloudflare
- [ ] Need workers.dev subdomain to go live

### Storage
- [x] Replace local storage with R2 (engine.ts updated with R2 binding)
- [x] Implement signed URLs for private files
- [x] CDN for file serving (automatic with R2 + Cache-Control)

### Monitoring
- [x] Analytics (KV-based tracking)
- [ ] Usage alerts
- [x] Error logging (observability enabled in wrangler)

## Environment Variables

```env
DATABASE_URL=file:./prisma/dev.db
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
TELEGRAM_BOT_TOKEN=
```

## Deployment

```bash
bun run build
wrangler deploy
```

## Success Criteria

- [x] Worker uploaded to Cloudflare
- [x] Files stored in R2
- [x] CDN for file serving (automatic with R2)
- [ ] Need workers.dev subdomain for public URL

## Next Step

Set up workers.dev subdomain at:
https://dash.cloudflare.com/bb5e336d3fdfcb38728d895b780a4285/workers/onboarding