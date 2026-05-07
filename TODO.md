# Current Tasks

## Phase 1: Core Storage ✅ COMPLETE

- [x] Upload endpoint
- [x] File retrieval
- [x] List files
- [x] Delete files

## Phase 2: Telegram Bot ✅ IN PROGRESS

- [x] Bot setup with grammy
- [x] /start, /files, /share, /delete commands
- [x] Photo upload handler
- [x] Document upload handler
- [ ] Test with real bot token

## Phase 3: Access Control (TODO)
- Expiring links
- Password protection
- Usage tracking

## Phase 4: Production (TODO)
- Cloudflare R2
- Workers deployment

## Run Commands

```bash
# Start server only
bun run src/index.ts

# Requires TELEGRAM_BOT_TOKEN in .env
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | Health | Server status |
| `POST /upload` | Upload | Multipart file upload |
| `GET /f/:slug` | Serve | Serve file by slug |
| `GET /api/files` | List | List all files |
| `DELETE /api/files/:id` | Delete | Delete a file |