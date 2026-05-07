# Deployment Guide

## Current Status

✅ Worker uploaded to Cloudflare  
⏳ Need workers.dev subdomain to go live

## Prerequisites

1. **Enable R2**: Already done - bucket `paperlink-files` created
2. **KV Namespace**: Already done - `ANALYTICS` created
3. **Workers.dev Subdomain**: Need to set up at https://dash.cloudflare.com/bb5e336d3fdfcb38728d895b780a4285/workers/onboarding

## Setup Steps

### 1. Get Workers.dev Subdomain
Go to: https://dash.cloudflare.com/bb5e336d3fdfcb38728d895b780a4285/workers/onboarding

- Click "Start building"
- Choose a subdomain name (e.g., `abujazone1`)
- Complete the setup (free)

### 2. Update BASE_URL
After getting subdomain, add it as a secret:
```bash
export CLOUDFLARE_API_TOKEN="your_token_here"
echo "https://your-subdomain.workers.dev" | wrangler secret put BASE_URL
```

### 3. Deploy
```bash
npm run deploy
```

## Environment Variables

Already set via wrangler secrets:
- `SIGNING_KEY`: For signed URLs
- `BASE_URL`: Your workers URL (after subdomain setup)

## Local Development

```bash
npm run dev  # Runs on localhost:3000
```

## Files Structure

```
src/
├── index.ts          # Local Node entry
├── cloudflare.ts    # Cloudflare Workers entry
├── api/             # API routes
├── bot/             # Telegram bot
├── storage/         # R2 + local fallback
├── utils/           # Helpers (signed URLs, analytics)
└── workers/         # Background jobs
```

## Cost (Free Tier)

| Service | Limit | Notes |
|---------|-------|-------|
| Workers | 100k req/day | |
| R2 | 1GB storage, 1M Class A, 10M Class B | |
| KV | 1GB | Analytics |
| CDN | Free | With R2 |

## Troubleshooting

- **R2 not enabled**: "Please enable R2 through the Cloudflare Dashboard"
- **Missing subdomain**: "You need to register a workers.dev subdomain"
- **Permission errors**: Ensure API token has all required permissions