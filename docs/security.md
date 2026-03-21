# Security Model

## Network Exposure

No inbound ports required.

System performs outbound IMAP + HTTPS only.

## Secrets Handling

Credentials stored in `.env`
File excluded from Git
Permissions restricted to owner

## Execution Isolation

Script runs as non-root user.
systemd oneshot prevents long-running attack surface.

## Risk Considerations

- Email account compromise could trigger unwanted downloads
- yt-dlp processes remote content
- Library path permissions must be controlled
