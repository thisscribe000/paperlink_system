# Phase 2: Telegram Bot

**Goal**: Add Telegram bot for file uploads and management.

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome + help |
| `/upload` | Upload a file |
| `/files` | List your files |
| `/delete <id>` | Delete a file |
| `/share <id>` | Get share link |

## Features

- Receive files via Telegram message
- Upload to storage engine
- Generate share links
- Inline keyboard menus

## Files to Create

- `src/bot/index.ts` — Bot entry point
- `src/bot/handlers/upload.ts` — Upload handler
- `src/bot/handlers/files.ts` — List/delete handlers
- `src/bot/handlers/share.ts` — Share link handler

## Bot Flow

```
User sends file → Bot receives → Upload to storage → Generate link → Send to user
```

## Success Criteria

- [ ] Bot receives files via Telegram
- [ ] Files uploaded to storage
- [ ] User can list their files
- [ ] User can delete files
- [ ] Share links work in Telegram