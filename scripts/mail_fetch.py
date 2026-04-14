import imaplib
import email
import re
import subprocess
import logging
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "config"))

from config import (
    IMAP_SERVER,
    IMAP_PORT,
    EMAIL_ACCOUNT,
    EMAIL_PASSWORD,
    MAILBOX,
    DOWNLOAD_ROOT,
    LOG_FILE,
    YT_DLP_PATH,
)

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

URL_REGEX = re.compile(r"https?://[^\s<>\"]+")

ALLOWED_HOST_PATTERNS = (
    "youtube.com",
    "youtu.be",
    "m.youtube.com",
    "music.youtube.com",
    "vimeo.com",
    "tiktok.com",
    "instagram.com",
    "x.com",
    "twitter.com",
)


def connect_mail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select(MAILBOX)
    return mail


def fetch_unread(mail):
    status, messages = mail.search(None, "UNSEEN")
    if status != "OK":
        logging.error("Failed to search mailbox.")
        return []
    if not messages or not messages[0]:
        return []
    return messages[0].split()


def extract_urls(msg):
    urls = []

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ("text/plain", "text/html"):
                payload = part.get_payload(decode=True)
                if payload:
                    text = payload.decode(errors="ignore")
                    urls.extend(URL_REGEX.findall(text))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text = payload.decode(errors="ignore")
            urls.extend(URL_REGEX.findall(text))

    cleaned = []
    for url in urls:
        url = url.rstrip('>)]}.,;\'"')
        lowered = url.lower()
        if any(host in lowered for host in ALLOWED_HOST_PATTERNS):
            cleaned.append(url)

    return list(dict.fromkeys(cleaned))


def download(url):
    logging.info(f"Downloading: {url}")
    result = subprocess.run(
        [
            YT_DLP_PATH,
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", f"{DOWNLOAD_ROOT}/%(title)s (%(upload_date)s) [YouTube - %(uploader)s].%(ext)s",
            url
        ],
        capture_output=True,
        text=True
    )
    logging.info(f"yt-dlp return code: {result.returncode}")
    if result.stdout:
        logging.info(result.stdout)
    if result.stderr:
        logging.error(result.stderr)

    return result.returncode == 0


def main():
    if not EMAIL_ACCOUNT or not EMAIL_PASSWORD:
        raise RuntimeError("EMAIL_ACCOUNT and EMAIL_PASSWORD must be set in .env")

    mail = connect_mail()

    for msg_id in fetch_unread(mail):
        status, data = mail.fetch(msg_id, "(RFC822)")
        if status != "OK":
            logging.error(f"Failed to fetch message id {msg_id!r}")
            continue

        msg = email.message_from_bytes(data[0][1])
        urls = extract_urls(msg)
        logging.info(f"Extracted URLs: {urls}")

        if not urls:
            logging.info(f"No supported URLs found in message id {msg_id!r}")
            mail.store(msg_id, "+FLAGS", "\\Seen")
            continue

        all_ok = True

        for url in urls:
            ok = download(url)
            if not ok:
                all_ok = False

        if all_ok:
            mail.store(msg_id, "+FLAGS", "\\Seen")
        else:
            logging.warning(f"Leaving message unread due to failed download: {msg_id!r}")

    mail.logout()


if __name__ == "__main__":
    main()
