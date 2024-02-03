#!/bin/bash

source env/bin/activate

pip install -U pip
pip install -r requirements.txt
spotdl --download-ffmpeg

echo ""
echo "Helper links:"
echo "1. https://core.telegram.org/bots/features#creating-a-new-bot"
echo "2. https://developer.spotify.com/documentation/web-api/concepts/apps"
echo ""

read -p "Enter Telegram bot API-Token: " API_TOKEN
read -p "Enter Spotify client id: " SPOTIFY_CLIENT_ID
read -p "Enter Spotify client secret: " SPOTIFY_CLIENT_SECRET

cd spotify_music_downloader_telegram_bot

cat << EOF > .env
API_TOKEN=$API_TOKEN

SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET
EOF
