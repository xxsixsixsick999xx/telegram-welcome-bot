import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

WELCOME_MEDIA = "https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif"

AUTO_DELETE_SECONDS = 20


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:

            keyboard = [
                [
                    InlineKeyboardButton("📢 Peraturan Grup", url="https://example.com/rules"),
                    InlineKeyboardButton("💬 Chat Admin", url="https://t.me/usernameadmin"),
                ],
                [
                    InlineKeyboardButton("📌 Info Grup", callback_data="info"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            msg = await update.message.reply_animation(
                animation=WELCOME_MEDIA,
                caption=(
                    f"🎉 Selamat datang {member.mention_html()}!\n\n"
                    "Terima kasih sudah bergabung ke grup ini.\n"
                    "Jangan lupa baca peraturan dan perkenalkan diri ya! 😊"
                ),
                reply_markup=reply_markup,
                parse_mode="HTML"
            )

            if AUTO_DELETE_SECONDS > 0:
                await context.job_queue.run_once(
                    lambda ctx: ctx.bot.delete_message(update.message.chat_id, msg.message_id),
                    AUTO_DELETE_SECONDS
                )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "info":
        await query.edit_message_caption(
            caption="ℹ️ **Info Grup**\n\nGrup ini dibuat untuk diskusi dan sharing.",
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
