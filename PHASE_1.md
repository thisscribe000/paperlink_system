# Phase 1: Core Storage

**Goal**: Build the fundamental storage engine with local storage.

## Deliverables

1. Hono + Bun project setup
2. Prisma + SQLite database
3. File upload endpoint (`POST /upload`)
4. File retrieval endpoint (`GET /f/{slug}`)
5. Public link generation
6. File metadata storage

## Files to Create

### Core
- `package.json`
- `tsconfig.json`
- `src/index.ts` — Main entry point
- `prisma/schema.prisma` — Database schema

### Storage Engine
- `src/storage/engine.ts` — Core storage logic
- `src/storage/uploader.ts` — Upload handling
- `src/storage/links.ts` — Link generation

### API Routes
- `src/api/files.ts` — File CRUD endpoints
- `src/api/links.ts` — Link endpoints

### Utilities
- `src/db/index.ts` — Prisma client
- `src/utils/id.ts` — ID generation

## Database Schema

```prisma
model File {
  id          String   @id @default(cuid())
  storage_key String   @unique
  filename    String
  mime_type   String
  size        Int
  hash        String?
  created_at  DateTime @default(now())
  expires_at  DateTime?
  is_public   Boolean  @default(true)
  owner_id    String
}

model Link {
  id        String   @id @default(cuid())
  file_id   String
  url_slug  String   @unique
  expires_at DateTime?
  created_at DateTime @default(now())
  click_count Int    @default(0)
}
```

## API Design

### Upload
```
POST /upload
Content-Type: multipart/form-data

Response: { id, url_slug, url }
```

### Access
```
GET /f/{url_slug}
→ Redirects to file or serves directly
```

### Manage
```
GET /api/files          → List files
DELETE /api/files/{id}  → Delete file
```

## Success Criteria

- [ ] Can upload file via POST
- [ ] File saved to local storage
- [ ] Can retrieve file via short URL
- [ ] Metadata stored in SQLite
- [ ] Clean 404 for missing files