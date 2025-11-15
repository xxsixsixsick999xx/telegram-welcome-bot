import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN tidak ditemukan. Tambahkan environment variable 'TOKEN' di Render.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sudah online 😎")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        username = member.username or member.full_name
        message = f"🎉 Selamat datang @{username}!\nSemoga betah di grup 😎"
        try:
            await update.message.reply_photo(
                photo=InputFile("welcome.jpg"), 
                caption=message
            )
        except Exception as e:
            await update.message.reply_text(message)
            print("Error sending image:", e)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    print("BOT RUNNING...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
