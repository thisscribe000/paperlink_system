# Phase 4: Production

**Goal**: Deploy to Cloudflare and integrate R2 storage.

## Tasks

### Infrastructure
- [ ] Set up Cloudflare R2 bucket
- [ ] Configure wrangler.toml
- [ ] Deploy to Cloudflare Workers

### Storage
- [ ] Replace local storage with R2
- [ ] Implement signed URLs for private files
- [ ] CDN for file serving

### Monitoring
- [ ] Analytics dashboard
- [ ] Usage alerts
- [ ] Error logging

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

- [ ] App runs on Cloudflare Workers
- [ ] Files stored in R2
- [ ] CDN serving files globally
- [ ] Zero cold start errors