import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Ambil token dari environment variable
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN tidak ditemukan. Tambahkan environment variable 'TOKEN' di Render.")

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sudah online 😎")

# Echo message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Welcome member baru dengan gambar
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        username = member.username or member.full_name
        message = f"🎉 Selamat datang @{username}!\nSemoga betah di grup ini 😎"
        try:
            photo = InputFile("welcome.jpg")  # pastikan file ada di folder project
            await update.message.reply_photo(photo=photo, caption=message)
        except Exception as e:
            await update.message.reply_text(message)
            print("Error sending welcome image:", e)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Echo
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Welcome
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    print("BOT RUNNING...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
