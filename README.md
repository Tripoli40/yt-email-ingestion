# yt-email-ingestion

Email-driven media ingestion pipeline for a self-hosted Jellyfin library.

## Background:

This was built as a part of a broader offline resilience setup. The goal is a local media library that remains accessible without the internet. It would provide reference videos on water purification, food preservation, first aid, and similar practical skills that are worth having locally rather than depending on a streaming service.

Email was chosen as the trigger interface because it works from any device without requiring a dedicated app, open inbound ports, or additional attack surface on the host. You send a supported URL to a designated inbox and the pipeline handles the rest.

## How It Works:

'systemd timer -> oneshot service -> python script -> yt-dlp -> local media storage -> Jellyfin library'

The main script is `scripts/mail_fetch.py`, configuration is loaded through `config/config.py`, and the default project log file is `logs/yt-inbox.log`.

Deployment-specific paths are documented in `docs/setup.md`.

## What it does:

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
