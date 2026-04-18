# yt-email-ingestion Rebuild Runbook

## Purpose
This runbook explains how to rebuild the yt-email-ingestion system on a new Linux host from scratch in the event of migration to a new server, OS reinstall, or host failure.

It assumes the Jellyfin server and media directory already exist and focuses only on restoring the email triggered media ingestion pipeline.

---

## 1. System Overview

This repository implements a host-native email ingestion flow for a Jellyfin library.

The path is:

`Email -> IMAP -> Python script -> yt-dlp -> Jellyfin media library`

The execution chain on the host is:

`systemd timer -> oneshot service -> Python script -> yt-dlp -> /srv/media/YouTube -> Jellyfin`

`scripts/mail_fetch.py` logs into IMAP, searches for unread messages, extracts supported media URLs from message bodies, runs `yt-dlp` for each URL, and marks the message seen only if all downloads for that message succeed.

## 2. Host Requirements

Required host components:

- Linux host with `systemd`
- Python 3
- `python3-venv`
- `ffmpeg`
- `yt-dlp`
- `nodejs` (recommended)
- Network access
- Writable Jellyfin media directory

Notes:

- The expected media destination is `/srv/media/YouTube`.
- Jellyfin should already be configured to watch that directory.
- No inbound ports are required for this ingestion system itself.

## 3. Install System Dependencies

On Debian or Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg nodejs npm curl
```

Install `yt-dlp` from the upstream GitHub release into a known path:

```bash
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

Optional verification:

```bash
/usr/local/bin/yt-dlp --version
ffmpeg -version
node --version
```

## 4. Clone the Repository

Clone the repository to the location you want to keep as the long-term project root:

```bash
git clone <repo-url>
cd yt-email-ingestion
```

## 5. Python Environment Setup

From `<repo-root>`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p logs
```

This creates the virtual environment expected by the repo `systemd` service and creates the repo-local log directory.

## 6. Configure Environment Variables

Create the runtime environment file:

```bash
cp .env.example .env
```

Edit `.env` and set the real host credentials and paths.

Minimum required variables:

- `EMAIL_ACCOUNT`
- `EMAIL_PASSWORD`

Recommended values:

- `LOG_FILE=logs/yt-inbox.log`
- `DOWNLOAD_ROOT=/srv/media/YouTube`
- `YT_DLP_PATH=/usr/local/bin/yt-dlp`

The repo supports these common settings:

```dotenv
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
MAILBOX=Inbox
DOWNLOAD_ROOT=/srv/media/YouTube
LOG_FILE=logs/yt-inbox.log
YT_DLP_PATH=/usr/local/bin/yt-dlp
```

Operational notes:

- `config/config.py` defaults `LOG_FILE` to `/tmp/yt-inbox.log` if it is not set, but the current repo documentation expects `logs/yt-inbox.log`.
- `.env` contains credentials and should remain local to the host.

## 7. Verify Manual Execution

Run one ingestion cycle directly before installing `systemd` units:

```bash
source .venv/bin/activate
python scripts/mail_fetch.py
```

This confirms:

- IMAP login works
- URL extraction works
- `yt-dlp` works
- Files appear in `/srv/media/YouTube`

If the script fails immediately, check `.env`, network access, the `yt-dlp` path, and write permissions on `/srv/media/YouTube`.

If you want to watch the repo-local log during testing:

```bash
tail -f logs/yt-inbox.log
```

## 8. Install systemd Units

The repository includes these unit files:

- `systemd/yt-email-ingestion.service`
- `systemd/yt-email-ingestion.timer`

Copy them into `/etc/systemd/system/`:

```bash
sudo cp systemd/yt-email-ingestion.service /etc/systemd/system/
sudo cp systemd/yt-email-ingestion.timer /etc/systemd/system/
```

Important: the checked-in service file uses YOUR_USERNAME as a placeholder. Before enabling the timer, edit /etc/systemd/system/yt-email-ingestion.service and replace YOUR_USERNAME with your actual account name and adjust paths to match your <repo-root>.

- `User`
- `Group`
- `WorkingDirectory`
- `ExecStart`

Before enabling the timer on a new host, edit `/etc/systemd/system/yt-email-ingestion.service` so those values match the new operator account and `<repo-root>`.

The installed service should point to:

- `<repo-root>/.venv/bin/python`
- `<repo-root>/scripts/mail_fetch.py`

After copying and adjusting the service file:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now yt-email-ingestion.timer
```

## 9. Verify Timer Operation

Check the timer:

```bash
sudo systemctl status yt-email-ingestion.timer
```

Check recent service logs:

```bash
sudo journalctl -u yt-email-ingestion.service -n 50
```

The timer in this repo is configured with:

- `OnBootSec=2min`
- `OnUnitActiveSec=2min`

That means it should trigger roughly every 2 minutes after boot and every 2 minutes after the last completed run.

If needed, inspect the installed unit definition:

```bash
sudo systemctl cat yt-email-ingestion.service
```

## 10. Confirm End-to-End Function

Run a final live test.

1. Send an email to the configured mailbox containing a supported YouTube link.
2. Wait for the next timer run, or manually start the service:

```bash
sudo systemctl start yt-email-ingestion.service
```

3. Confirm the result:

- File downloaded to `/srv/media/YouTube`
- Jellyfin detects the file

If Jellyfin does not pick up the file, verify Jellyfin library configuration and filesystem permissions on the media directory.

## 11. Operational Notes

- The service is `Type=oneshot`. There is no long-running daemon.
- Retry is simple: if any download for a message fails, that message remains unread and will be retried on a later timer run.
- Messages with no supported URLs are marked seen and will not be retried.
- HTML-only emails may not be parsed correctly because the current script extracts URLs from `text/plain` parts.
- Logs are normally written to `logs/yt-inbox.log` when `LOG_FILE` is set that way in `.env`.
- `yt-dlp` behavior depends on upstream extractor changes. If downloads start failing for a site that used to work, update `yt-dlp` first.
- Supported host patterns in the current script include YouTube, Vimeo, TikTok, Instagram, X, and Twitter URLs.
- No database, queue, or dedupe layer exists in this design. Recovery is based on the mailbox state plus repeated timer runs.
