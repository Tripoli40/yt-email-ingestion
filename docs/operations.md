# Operations

## Timer Control

sudo systemctl status yt-email-ingestion.timer
sudo systemctl restart yt-email-ingestion.timer

## Manual Run

sudo systemctl start yt-email-ingestion.service

## Logs

tail -f ~/projects/yt-email-ingestion/logs/yt-inbox.log

## Troubleshooting

Check systemd journal:

sudo journalctl -u yt-email-ingestion.service -n 50
