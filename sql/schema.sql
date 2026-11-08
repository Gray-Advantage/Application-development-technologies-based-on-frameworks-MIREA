PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    registered_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS links (
    code TEXT PRIMARY KEY NOT NULL,
    url TEXT NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    CHECK (expires_at > created_at)
);
CREATE TABLE IF NOT EXISTS clicks (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL REFERENCES links(code) ON DELETE RESTRICT,
    clicked_at TEXT NOT NULL,
    source TEXT DEFAULT NULL
);
CREATE INDEX IF NOT EXISTS clicks_code_idx ON clicks(code);
CREATE INDEX IF NOT EXISTS links_owner_idx ON links(owner_id);
