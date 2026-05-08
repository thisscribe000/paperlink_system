# Current Tasks

## Phase 1: Core Storage ✅ COMPLETE

- [x] Upload endpoint
- [x] File retrieval
- [x] List files
- [x] Delete files

## Phase 2: Telegram Bot ✅ COMPLETE

- [x] Bot setup with grammy
- [x] /start, /files, /share, /delete commands
- [x] Photo upload handler
- [x] Document upload handler
- [x] Error handling for large files (20MB limit)
- [x] Bot connected to main server
- [x] Tested with real bot token

## Phase 3: Access Control (TODO)
- Expiring links
- Password protection
- Usage tracking

## Phase 4: Production ✅ IN PROGRESS
- [x] Cloudflare Tunnel setup
- [x] Domain usepaperlink.site connected
- [ ] Cloudflare R2 for large files (over 20MB)

## Run Commands

```bash
# Start server
bun run dev

# Start tunnel (in separate terminal)
cloudflared tunnel run paperlink
```

## Current Setup

- **Domain:** usepaperlink.site (pointing to local dev via Cloudflare Tunnel)
- **Tunnel:** Named tunnel "paperlink"
- **Bot Token:** Configured in .env

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | Health | Server status |
| `POST /upload` | Upload | Multipart file upload |
| `GET /f/:slug` | Serve | Serve file by slug |
| `GET /api/files` | List | List all files |
| `DELETE /api/files/:id` | Delete | Delete a file |

## Telegram Bot Commands

- `/start` - Welcome message
- `/files` - List your uploaded files
- `/share <id>` - Get share link for a file
- `/delete <id>` - Delete a file
- Just send a file to upload it

## Known Limitations

- Telegram Bot API has 20MB file download limit
- Files over 20MB cannot be downloaded by the bot
- Solution: Use Cloudflare R2 for large files (future)