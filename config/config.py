import os
from dotenv import load_dotenv

load_dotenv()

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
MAILBOX = os.getenv("MAILBOX", "Inbox")
DOWNLOAD_ROOT = os.getenv("DOWNLOAD_ROOT", "/srv/media/YouTube")
LOG_FILE = os.getenv("LOG_FILE", "/tmp/yt-inbox.log")
YT_DLP_PATH = os.getenv("YT_DLP_PATH", "/usr/local/bin/yt-dlp")
