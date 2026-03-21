# Setup Guide

## Requirements

- Linux host (Ubuntu / Mint recommended)
- Python 3
- ffmpeg
- yt-dlp
- Gmail account with App Password enabled
- Jellyfin library folder

## Install Dependencies

sudo apt install python3 python3-venv ffmpeg curl

Install yt-dlp:

sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

## Project Setup

git clone <repo>
cd yt-email-ingestion

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Configure Environment

cp .env.example .env
nano .env

## Test Manually

python scripts/mail_fetch.py
