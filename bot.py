import os
import asyncio
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN tidak ditemukan. Tambahkan environment variable 'TOKEN' di Render.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sudah online 😎")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member

    # Deteksi jika user baru JOIN
    if chat_member.new_chat_member.status == "member":
        member = chat_member.new_chat_member.user
        username = member.username or member.full_name

        message = f"🎉 Selamat datang @{username}!\nSemoga betah di grup 😎"

        try:
            await update.effective_chat.send_photo(
                photo=InputFile("welcome.jpg"),
                caption=message
            )
        except Exception:
            await update.effective_chat.send_message(message)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command /start
    app.add_handler(CommandHandler("start", start))

    # Echo chat normal
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Handler welcome user baru (PTB v20)
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    print("BOT RUNNING...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
