# Database Schema

## Entities

### File
Stores file metadata and location.

| Field | Type | Description |
|-------|------|-------------|
| id | String (cuid) | Primary key |
| storage_key | String | R2/S3 object key |
| filename | String | Original filename |
| mime_type | String | MIME type |
| size | Int | File size in bytes |
| hash | String? | Content hash for deduplication |
| created_at | DateTime | Upload timestamp |
| expires_at | DateTime? | Auto-delete time |
| is_public | Boolean | Public access flag |
| owner_id | String | Telegram user ID |

### Link
Shareable short URLs.

| Field | Type | Description |
|-------|------|-------------|
| id | String (cuid) | Primary key |
| file_id | String | Foreign key to File |
| url_slug | String | Short URL slug (unique) |
| password | String? | Hashed password |
| expires_at | DateTime? | Expiration time |
| created_at | DateTime | Creation timestamp |
| click_count | Int | Access counter |

### User
PaperLink user tracking.

| Field | Type | Description |
|-------|------|-------------|
| id | String (cuid) | Primary key |
| telegram_id | BigInt | Telegram user ID (unique) |
| username | String? | Telegram username |
| storage_used | Int | Bytes used |
| storage_limit | Int | Bytes allowed |
| created_at | DateTime | Registration time |

## Indexes

- `File.owner_id` — For listing user's files
- `Link.url_slug` — For fast link lookup
- `Link.file_id` — For file's links
- `User.telegram_id` — For auth lookup

## Migrations

```bash
bunx prisma migrate dev
```