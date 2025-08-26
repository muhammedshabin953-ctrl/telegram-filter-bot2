# Telegram Filter Bot

This is a Telegram bot with permanent filter functionality using SQLite.

## Features
- Add filters: `/addfilter <keyword> <reply>`
- List filters: `/listfilters`
- Delete filters: `/delfilter <keyword>`
- Bot replies automatically if a message contains a keyword.

## Setup
1. Clone this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your bot token (from BotFather) as an environment variable:
   ```bash
   export BOT_TOKEN=your_telegram_bot_token
   ```
   (On Windows PowerShell: `setx BOT_TOKEN "your_telegram_bot_token"`)
4. Run the bot:
   ```bash
   python bot.py
   ```

## Deployment (Railway/Heroku)
- Deploy this repo and set `BOT_TOKEN` as a config variable in your hosting environment.
