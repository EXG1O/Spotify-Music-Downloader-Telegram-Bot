# Spotify Music Downloader Telegram Bot
**Spotify Music Downloader Telegram Bot** - Telegram Bot для скачивания музыки с Spotify.

# Требование
- Python 3.10.10

# Установка проекта
1. Устанавливаем проекта:
```sh
git clone https://github.com/EXG1O/Spotify-Music-Downloader-Telegram-Bot.git
cd Spotify-Music-Downloader-Telegram-Bot
python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
spotdl --download-ffmpeg
cd spotify_music_downloader_telegram_bot
```
2. Запускаем главный файл:
```sh
python main.py
```
3. Если вы всё правильно сделали, то у вас будет такой вывод:
```
Enter the Constructor Telegram bot token in the file ./data/api.token!
```
4. Теперь нам нужно создать своего Telegram бота через [BotFather Telegram бота](https://t.me/BotFather);
5. После создание Telegram бота получаем его API-токен и добавляем его в файл ./data/api.token;
6. Запускаем ещё раз главный файл:
```sh
python main.py
```
7. Теперь в файл ./data/spotify_settings.json нам нужно ввести "client_id" и "client_secret", которые можно получить на сайте [Spotify for Developers](https://developer.spotify.com/dashboard);
8. Запускаем ещё раз главный файл:
```sh
python main.py
```
7. Если вы всё правильно сделали, то в консоли будут такие сообщения:
```log
[ДАТА И ВРЕМЯ]: INFO > Start asynchronous function for check downloaded spotify tracks.
[ДАТА И ВРЕМЯ]: INFO > Starting Spotify Music Downloader Telegram Bot.
[ДАТА И ВРЕМЯ]: INFO > Skipped None updates.
[ДАТА И ВРЕМЯ]: INFO > Start polling.
```
8. Теперь переходим в вашего ранее созданого Telegram бота и пользуемся им 😁

# Cтруктура проекта
```sh
Spotify-Music-Downloader-Telegram-Bot
├── LICENSE
├── README.md
├── requirements.txt
└── spotify_music_downloader_telegram_bot
    ├── main.py
    └── scripts
        ├── __init__.py
        └── settings.py
```
