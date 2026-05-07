CREATE TABLE IF NOT EXISTS "User" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "telegram_id" INTEGER NOT NULL UNIQUE,
    "username" TEXT,
    "storage_used" INTEGER NOT NULL DEFAULT 0,
    "storage_limit" INTEGER NOT NULL DEFAULT 1073741824,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "File" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "storage_key" TEXT NOT NULL UNIQUE,
    "filename" TEXT NOT NULL,
    "mime_type" TEXT NOT NULL,
    "size" INTEGER NOT NULL,
    "hash" TEXT,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expires_at" DATETIME,
    "is_public" BOOLEAN NOT NULL DEFAULT true,
    "owner_id" TEXT
);

CREATE TABLE IF NOT EXISTS "Link" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "file_id" TEXT NOT NULL,
    "url_slug" TEXT NOT NULL UNIQUE,
    "password" TEXT,
    "expires_at" DATETIME,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "click_count" INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS "User_telegram_id_key" ON "User"("telegram_id");
CREATE INDEX IF NOT EXISTS "File_storage_key_key" ON "File"("storage_key");
CREATE INDEX IF NOT EXISTS "Link_url_slug_key" ON "Link"("url_slug");
