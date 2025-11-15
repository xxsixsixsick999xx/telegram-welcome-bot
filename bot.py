import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WELCOME_MEDIA = "https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif"

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            keyboard = [
                [InlineKeyboardButton("📢 Rules", url="https://example.com/rules")],
                [InlineKeyboardButton("📌 Info", callback_data="info")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_animation(
                animation=WELCOME_MEDIA,
                caption=f"Selamat datang {member.mention_html()}!",
                parse_mode="HTML",
                reply_markup=reply_markup
            )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "info":
        await query.edit_message_caption(
            caption="ℹ️ Info Grup: Grup untuk diskusi dan sharing.",
            parse_mode="Markdown"
        )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("BOT RUNNING...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
