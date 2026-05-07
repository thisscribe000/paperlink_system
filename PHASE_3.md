# Phase 3: Access Control

**Goal**: Add expiring links, password protection, and usage tracking.

## Features

1. **Expiring Links** — Links that auto-expire
2. **Password Protection** — Secure links with password
3. **Usage Tracking** — Track downloads, views, storage

## API Additions

```
POST /api/links
Body: { file_id, expires_in?, password? }

GET /f/{slug}?password=xxx
→ 401 if wrong password
→ 410 if expired
```

## Database Additions

```prisma
model Link {
  password   String?
  expires_at DateTime?
}

model User {
  storage_used   Int @default(0)
  storage_limit  Int @default(1073741824)  // 1GB
}
```

## Cleanup Worker

Background job to:
- Delete expired files
- Clean up expired links
- Update user storage usage

## Success Criteria

- [x] Can create expiring link
- [x] Expired links return 410
- [x] Password-protected links work
- [x] Storage usage tracked per user
- [x] Cleanup worker runs daily