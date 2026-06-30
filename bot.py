from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7626487549

ANIME_CODES = {}
waiting_for_video = {}
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz admin emassiz.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Foydalanish: /add A001")
        return

    code = context.args[0].upper()
    waiting_for_video[update.effective_user.id] = code
    ANIME_CODES[code] = []

    await update.message.reply_text(
        f"✅ {code} yaratildi.\n\nEndi videolarni bittalab yuboring.\nTugatgach /done yozing."
    )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 Animelar Olami botiga xush kelibsiz!\n\n"
        "📥 Iltimos, qidirayotgan animengizning kodini kiriting."
    )
async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.effective_user.id not in waiting_for_video:
        return

    code = waiting_for_video[update.effective_user.id]
    file_id = update.message.video.file_id

    ANIME_CODES[code].append(file_id)

    await update.message.reply_text(f"✅ Video saqlandi. Jami: {len(ANIME_CODES[code])} ta.")
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
app.add_handler(CommandHandler("add", add))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

print("Bot ishga tushdi...")
app.run_polling()
