# Spotify Music Downloader Telegram-Bot
**Spotify Music Downloader Telegram Bot** - Telegram Bot для скачивание музыки с Spotify.

# Требование
- Python 3.10.10

# Установка Telegram ботa
1. Устанавливаем Telegram ботa:
```sh
git clone https://github.com/EXG1O/Spotify-Music-Downloader-Telegram-Bot.git
cd Spotify-Music-Downloader-Telegram-Bot
python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd spotify_music_downloader_telegram_bot
```
2. Запускаем Telegram ботa:
```sh
python main.py
```
3. Если вы всё правильно сделали, то у вас будет такой вывод:
```sh
Enter the Constructor Telegram bot token in the file ./data/spotify_music_downloader_telegram_bot.token!
```
4. Теперь нам нужно создать своего Telegram бота через BotFather Telegram бота (Ссылка на Telegram бота: https://t.me/BotFather);
5. После создание Telegram бота через BotFather Telegram бота, получаем его API-токен и добавляем его в файл ./data/spotify_music_downloader_telegram_bot.token;
6. Запускаем ещё раз Telegram ботa:
```sh
python main.py
```
7. Если вы всё сделали правильно, то в файле ./data/spotify_music_downloader_telegram_bot.log будет такое сообщение:
```log
[ДАТА И ВРЕМЯ]: INFO > Scheduler started
```
8. Теперь переходим в вашего ранее созданого Telegram бота через BotFather Telegram бота и пользуемся им 😁

# Примечание
- Все ошибки будут появляться в файле ./data/spotify_music_downloader_telegram_bot.log.