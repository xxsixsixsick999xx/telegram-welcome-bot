import os
import asyncio
from dotenv import load_dotenv

from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sudah online bangsat 😎")

# Echo message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Welcome with Image
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for member in update.message.new_chat_members:

        username = member.username or member.full_name
        message = f"🎉 Selamat datang @{username}!\nSemoga betah di grup ini 😎"

        # Kirim gambar welcome
        try:
            photo = InputFile("welcome.jpg")  # harus ada file ini
            await update.message.reply_photo(photo=photo, caption=message)
        except Exception as e:
            # fallback kalau gagal kirim foto
            await update.message.reply_text(message)
            print("Error sending welcome image:", e)

# Main app
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Echo
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Welcome event
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    print("BOT RUNNING...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
