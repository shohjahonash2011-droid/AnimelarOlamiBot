from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8811406011:AAGJWa3oZruncw0TEWI_tcsnBl3UyiPb57k"

# Hozircha bo'sh
ANIME_CODES = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 Animelar Olami botiga xush kelibsiz!\n\n"
        "📥 Iltimos, qidirayotgan animengizning kodini kiriting."
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.upper()

    if code in ANIME_CODES:
        await update.message.reply_video(ANIME_CODES[code])
    else:
        await update.message.reply_text(
            "❌ Bunday kod topilmadi.\n\n"
            "Iltimos, kodni qayta tekshirib yuboring."
        )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

print("Bot ishga tushdi...")
app.run_polling()
