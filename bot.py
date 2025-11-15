import os
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN tidak ditemukan. Tambahkan environment variable 'TOKEN' di Render/GitHub.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sudah online 😎")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        username = member.username or member.full_name
        message = f"🎉 Selamat datang @{username}!\nSemoga betah di grup ini 😎"
        keyboard = [
            [InlineKeyboardButton("📜 Rules", callback_data="rules")],
            [InlineKeyboardButton("ℹ️ Info Grup", callback_data="info")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            photo = InputFile("welcome.jpg")
            await update.message.reply_photo(photo=photo, caption=message, reply_markup=reply_markup)
        except Exception:
            await update.message.reply_text(message, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "rules":
        await query.edit_message_text("📜 Rules:\n1. Hormati semua member\n2. Tidak spam\n3. Enjoy!")
    elif query.data == "info":
        await query.edit_message_text("ℹ️ Info Grup:\nBot ini dibuat untuk menyambut member baru.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
