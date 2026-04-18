# Setup Guide

## Paths Used In This Repo

- Project root: `<repo-root>`
- Script: `scripts/mail_fetch.py`
- Config loader: `config/config.py`
- Project log file: `logs/yt-inbox.log`

## Host Requirements

- Linux host with `systemd`
- Python 3
- `python3-venv`
- `ffmpeg`
- `yt-dlp`
- IMAP account credentials
- Write access to `/srv/media/YouTube`

Recommended for current `yt-dlp` reliability:

- Node.js installed on the host for sites and extractors that need JavaScript runtime support

## Package Install

Example Debian/Ubuntu package install:

```bash
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg nodejs npm curl
```

Install `yt-dlp` in a known system path:

```bash
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

## Virtualenv Setup

From the project root:

```bash
cd <repo-root>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p logs
```

## `.env` Setup

Copy the example file and edit it for the host:

```bash
cd <repo-root>
cp .env.example .env
nano .env
```

At minimum, set:

- `EMAIL_ACCOUNT`
- `EMAIL_PASSWORD`

For the expected repo-local logging layout, set:

- `LOG_FILE=logs/yt-inbox.log`

For this host deployment, an absolute path is also valid if preferred:

- `LOG_FILE=/home/YOUR_USERNAME/projects/yt-email-ingestion/logs/yt-inbox.log`

Other values commonly kept as-is unless your host differs:

- `IMAP_SERVER=imap.gmail.com`
- `IMAP_PORT=993`
- `MAILBOX=Inbox`
- `DOWNLOAD_ROOT=/srv/media/YouTube`
- `YT_DLP_PATH=/usr/local/bin/yt-dlp`

`config/config.py` loads `.env` and uses defaults when values are not set, but the current working setup expects the `.env` file to define the real host-specific values.

## Manual Test

Run the script directly from the virtualenv:

```bash
cd <repo-root>
source .venv/bin/activate
python scripts/mail_fetch.py
```

If you want logs in the project log file instead of the config default fallback, make sure `LOG_FILE` is set in `.env` before testing.

## Systemd Units

Repo copies of the units are:

- `systemd/yt-email-ingestion.service`
- `systemd/yt-email-ingestion.timer`

The service in this repo runs:

- `.venv/bin/python scripts/mail_fetch.py`
