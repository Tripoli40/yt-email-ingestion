# Architecture

This project uses a simple host-native ingestion model.

## Design Principles

- Known-working operational pattern first
- Minimal moving parts
- No persistent daemon required
- Fail-safe retry behavior
- Human-driven ingestion trigger

## Execution Model

systemd timer → oneshot service → Python script

The script performs:

1. IMAP login
2. Search for UNSEEN messages
3. Extract supported URLs
4. Execute yt-dlp
5. Mark successful messages as seen

## Media Flow

yt-dlp writes directly to:

/srv/media/YouTube

Jellyfin monitors this directory and indexes new content automatically.
