# Email Media Ingestion Pipeline

Automated system that ingests media links sent via email and downloads them into a local media library for playback in Jellyfin.

This project demonstrates practical infrastructure automation, safe secret handling, systemd scheduling, and real-world media ingestion workflows.

---

## Overview

The system monitors an email inbox via IMAP.  
Unread messages are scanned for supported media URLs (YouTube, TikTok, etc).  

Valid links are downloaded using `yt-dlp` and stored in a structured media library folder which is indexed by Jellyfin.

Execution is automated via a `systemd` timer.

---

## Architecture

Email inbox (IMAP) -> Python ingestion script -> yt-dlp media extraction -> Local media library (srv/media/YouTube) -> Jellyfin indexing + playback

---

## Features

- Inbox-driven ingestion workflow
- Unread-only trigger behavior
- Automatic retry of failed downloads
- Multi-site support via yt-dlp
- Local-only execution (no inbound ports)
- systemd timer automation
- Secret isolation via `.env`
- Git-safe project structure

---

## Technology Stack

- Python 3
- yt-dlp
- ffmpeg
- Gmail IMAP
- systemd timers
- Jellyfin

---

## Current Status

Stable baseline implementation.

- Manual execution validated
- Automated polling validated
- Successful media ingestion verified
- Jellyfin playback verified

---

## Known Limitations

- Some YouTube formats may require PO-token support
- Extractor reliability depends on upstream yt-dlp changes
- Inbox scanning assumes reasonable unread-mail hygiene
- No deduplication or database state tracking yet

---

## Future Improvements

- Message labeling / queue isolation
- Download state database
- Containerized deployment option
- Notification system
- Multi-library routing
- Parallel ingestion workers
