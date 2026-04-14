# Operations

All commands below use the current unit names:

- `yt-email-ingestion.service`
- `yt-email-ingestion.timer`

Current project log path:

- `logs/yt-inbox.log`

## Timer Control

Check timer state:

```bash
sudo systemctl status yt-email-ingestion.timer
```

Restart the timer after unit or schedule changes:

```bash
sudo systemctl restart yt-email-ingestion.timer
```

Enable the timer at boot:

```bash
sudo systemctl enable --now yt-email-ingestion.timer
```

## Manual Service Trigger

Run one ingestion cycle through `systemd`:

```bash
sudo systemctl start yt-email-ingestion.service
```

Check the last service result:

```bash
sudo systemctl status yt-email-ingestion.service
```

## Direct Script Execution

Run the script directly from the project virtualenv:

```bash
cd <repo-root>
source .venv/bin/activate
python scripts/mail_fetch.py
```

This bypasses the timer and service wrapper and is the fastest way to test config changes.

## Log Viewing

Follow the project log file:

```bash
tail -f logs/yt-inbox.log
```

## Journal Viewing

Check recent `systemd` journal lines for the service:

```bash
sudo journalctl -u yt-email-ingestion.service -n 50
```

Follow the journal live during a manual run:

```bash
sudo journalctl -u yt-email-ingestion.service -f
```

## Service Definition Inspection

Show the installed service definition that `systemd` is actually using:

```bash
sudo systemctl cat yt-email-ingestion.service
```

If needed, compare that output with the repo copy at:

- `systemd/yt-email-ingestion.service`
