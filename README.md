# yt-email-ingestion

Host-native email-driven media ingestion for a homelab Jellyfin library.

The main script is `scripts/mail_fetch.py`, configuration is loaded through `config/config.py`, and the default project log file is `logs/yt-inbox.log`.

Deployment-specific paths are documented in `docs/setup.md`.

The service flow is simple:

`systemd timer -> oneshot service -> Python script -> yt-dlp -> /srv/media/YouTube -> Jellyfin`

What it does:

- Logs into IMAP
- Checks for unread messages
- Extracts supported media URLs from message content
- Runs `yt-dlp` for each supported URL
- Marks the message seen only if all downloads for that message succeed

Retry behavior is conditional. There is no separate retry queue or backoff system. If a download fails, the message is left unread, so `yt-email-ingestion.timer` can pick it up again on a later run. Messages with no supported URLs are marked seen and will not be retried.

Systemd units in this repo:

- `yt-email-ingestion.service`
- `yt-email-ingestion.timer`

More detail:

- [docs/setup.md](docs/setup.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/operations.md](docs/operations.md)
- [docs/known_issues.md](docs/known_issues.md)
- [docs/security.md](docs/security.md)
