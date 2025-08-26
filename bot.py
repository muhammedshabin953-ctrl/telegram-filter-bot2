import logging
import sqlite3
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database setup
conn = sqlite3.connect("filters.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS filters (keyword TEXT PRIMARY KEY, reply TEXT)")
conn.commit()

# Add filter command
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addfilter <keyword> <reply>")
        return
    keyword = context.args[0].lower()
    reply = " ".join(context.args[1:])
    cursor.execute("REPLACE INTO filters (keyword, reply) VALUES (?, ?)", (keyword, reply))
    conn.commit()
    await update.message.reply_text(f"✅ Filter added: {keyword} → {reply}")

# List filters
async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT keyword FROM filters")
    rows = cursor.fetchall()
    if not rows:
        await update.message.reply_text("No filters found.")
    else:
        filters_list = "\n".join([row[0] for row in rows])
        await update.message.reply_text(f"📋 Filters:\n{filters_list}")

# Delete filter
async def del_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /delfilter <keyword>")
        return
    keyword = context.args[0].lower()
    cursor.execute("DELETE FROM filters WHERE keyword=?", (keyword,))
    conn.commit()
    await update.message.reply_text(f"🗑️ Filter deleted: {keyword}")

# Check messages for filters
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    cursor.execute("SELECT keyword, reply FROM filters")
    rows = cursor.fetchall()
    for keyword, reply in rows:
        if keyword in text:
            await update.message.reply_text(reply)
            break

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("addfilter", add_filter))
    application.add_handler(CommandHandler("listfilters", list_filters))
    application.add_handler(CommandHandler("delfilter", del_filter))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

    # Run bot
    application.run_polling()

if __name__ == "__main__":
    main()
