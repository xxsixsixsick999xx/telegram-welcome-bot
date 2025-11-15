import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# List GIF/Foto random welcome
WELCOME_MEDIA_LIST = [
    "https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/3o6ZsX2T4Zn8L1J3DW/giphy.gif"
]

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:

            # Random GIF
            media = random.choice(WELCOME_MEDIA_LIST)

            # Tombol inline
            keyboard = [
                [InlineKeyboardButton("📢 Rules", url="https://example.com/rules")],
                [InlineKeyboardButton("📌 Info", callback_data="info")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Kirim welcome GIF
            sent_message = await update.message.reply_animation(
                animation=media,
                caption=f"🎉 Selamat datang {member.mention_html()}!",
                parse_mode="HTML",
                reply_markup=reply_markup
            )

            # Auto-delete setelah 30 detik
            await asyncio.sleep(30)
            await sent_message.delete()

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "info":
        await query.edit_message_caption(
            caption="ℹ️ Info Grup: Grup untuk diskusi dan sharing.",
            parse_mode="Markdown"
        )

async def main():
    # ApplicationBuilder v20+ tanpa Updater
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("BOT RUNNING...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
