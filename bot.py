from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

# TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ADMIN ID
ADMIN_ID = 7626487549

# DATA STORAGE
ANIME_CODES = {}
waiting_for_video = {}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 Animelar Olami botiga xush kelibsiz!\n\n"
        "📥 Anime kodini kiriting (masalan: A001)"
    )


# ADD ANIME (ADMIN ONLY)
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
        f"✅ {code} yaratildi.\n\n"
        "Endi videolarni yuboring.\nTugatish uchun /done yozing."
    )


# SAVE VIDEO
async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        return

    if user_id not in waiting_for_video:
        return

    file_id = None

    # Video bo'lsa
    if update.message.video:
        file_id = update.message.video.file_id

    # Fayl (Document) bo'lsa va video bo'lsa
    elif update.message.document:
        if update.message.document.mime_type and update.message.document.mime_type.startswith("video/"):
            file_id = update.message.document.file_id
        else:
            await update.message.reply_text("❌ Bu video fayl emas.")
            return

    else:
        return

    code = waiting_for_video[user_id]
    ANIME_CODES[code].append(file_id)

    await update.message.reply_text(
        f"✅ Video qo'shildi. Jami: {len(ANIME_CODES[code])} ta."
    )

# DONE (FINISH ADDING)
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        return

    if user_id not in waiting_for_video:
        await update.message.reply_text("❌ Hozir hech narsa qo‘shilmayapti.")
        return

    code = waiting_for_video.pop(user_id)

    await update.message.reply_text(
        f"🎉 {code} saqlandi!\n📺 Jami: {len(ANIME_CODES[code])} ta video."
    )


# SEARCH ANIME (USER SIDE)
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.upper()

    if code in ANIME_CODES:
        for video in ANIME_CODES[code]:
            await update.message.reply_video(video)
    else:
        await update.message.reply_text(
            "❌ Bunday kod topilmadi."
        )


# APP SETUP
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("done", done))
app.add_handler(MessageHandler(filters.VIDEO, save_video))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

print("Bot ishga tushdi...")
app.run_polling()
