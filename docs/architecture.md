# Architecture

This project uses a simple host-native execution model with no long-running daemon.

## Execution Model

`systemd timer -> oneshot service -> Python script -> yt-dlp -> /srv/media/YouTube -> Jellyfin`

Current unit names:

- `yt-email-ingestion.timer`
- `yt-email-ingestion.service`

Current script path:

- `scripts/mail_fetch.py`

Current config path:

- `config/config.py`

## What The Script Does

On each service run, the script:

1. Loads environment-backed settings through `config/config.py`
2. Connects to IMAP over SSL
3. Searches the configured mailbox for `UNSEEN` messages
4. Reads message content and extracts supported URLs
5. Calls `yt-dlp` once per supported URL
6. Leaves the message unread if any download fails
7. Marks the message seen if all downloads for that message succeed

## Media Output

Downloads are written under:

- `/srv/media/YouTube`

Jellyfin is expected to watch that directory and pick up new files after they land.

## Operational Notes

- The service is `Type=oneshot`
- There is no database, queue worker, or dedupe layer
- The timer provides repeated polling
- Retry is only the next timer run reprocessing messages that were left unread
