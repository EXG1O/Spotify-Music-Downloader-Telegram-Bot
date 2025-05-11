#!/bin/bash

source env/bin/activate

pip install -U pip
pip install poetry
poetry install
spotdl --download-ffmpeg

read -p "Enter Telegram bot API-Token: " API_TOKEN
read -p "Enter Spotify client id: " SPOTIFY_CLIENT_ID
read -p "Enter Spotify client secret: " SPOTIFY_CLIENT_SECRET
read -p "Enter PostgreSQL database host: " POSTGRESQL_DATABASE_HOST
read -p "Enter PostgreSQL database name: " POSTGRESQL_DATABASE_NAME
read -p "Enter PostgreSQL database user: " POSTGRESQL_DATABASE_USER
read -p "Enter PostgreSQL database password: " POSTGRESQL_DATABASE_PASSWORD

cat << EOF > .env
BOT_TOKEN=$BOT_TOKEN

SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET

POSTGRESQL_DATABASE_HOST=$POSTGRESQL_DATABASE_HOST
POSTGRESQL_DATABASE_NAME=$POSTGRESQL_DATABASE_NAME
POSTGRESQL_DATABASE_USER=$POSTGRESQL_DATABASE_USER
POSTGRESQL_DATABASE_PASSWORD=$POSTGRESQL_DATABASE_PASSWORD
EOF

alembic upgrade head
