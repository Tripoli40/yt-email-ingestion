# Security Model

## Network Exposure

- No inbound ports are required for normal operation
- The script makes outbound connections for IMAP and site downloads through `yt-dlp`

## Secrets Handling

- Credentials are stored in `.env`
- `.env` is excluded from Git
- `config/config.py` loads values from `.env` into the script at runtime

This is simple secret handling for a homelab host, not a hardened secret-management system.

## Execution Model

- The service is a non-root `systemd` `oneshot` unit
- The repo unit file runs from the repository root
- The script path is `scripts/mail_fetch.py`

## Data And Host Risks

- An exposed or reused mail credential can let unwanted messages trigger downloads
- `yt-dlp` processes remote content and depends on upstream extractor behavior
- The media library path and the project log path should stay writable only to the intended local user
- Security still depends on normal host hygiene around file permissions, package updates, and account access
