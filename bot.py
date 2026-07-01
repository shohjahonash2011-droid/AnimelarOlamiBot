from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
import json
# ==========================
# TOKEN
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ==========================
# ADMIN
# ==========================
ADMIN_ID = 7626487549

# ==========================
# DATA
# ==========================
ANIME_CODES = {}
waiting_for_video = {}
DATA_FILE = "anime_data.json"

def load_data():
    global ANIME_CODES
    try:
        with open(DATA_FILE, "r") as f:
            ANIME_CODES = json.load(f)
    except:
        ANIME_CODES = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(ANIME_CODES, f, indent=4)
# ==========================
# START
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 Animelar Olami botiga xush kelibsiz!\n\n"
        "📥 Anime kodini kiriting.\nMasalan: A001"
    )

# ==========================
# ADD
# ==========================
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text("Foydalanish:\n/add A001")
        return

    code = context.args[0].upper()

    waiting_for_video[update.effective_user.id] = code
    ANIME_CODES[code] = []

    await update.message.reply_text(
        f"✅ {code} yaratildi.\n\n"
        "🎥 Endi videolarni bittalab yuboring.\n"
        "📎 Video yoki video fayl (MKV, MP4...) yuborishingiz mumkin.\n\n"
        "Tugatgach /done yozing."
    )

# ==========================
# SAVE VIDEO
# ==========================
async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        return

    if user_id not in waiting_for_video:
        return

    file_id = None

    # Oddiy video
    if update.message.video:
        file_id = update.message.video.file_id

    # Document (video file)
    elif update.message.document:
        doc = update.message.document

        if doc.file_name and doc.file_name.lower().endswith(
            (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm")
        ):
            file_id = doc.file_id
        else:
            await update.message.reply_text("❌ Bu video fayl emas.")
            return

    if file_id is None:
        return

    code = waiting_for_video[user_id]
    ANIME_CODES[code].append(file_id)
save_data()
    await update.message.reply_text(
        f"✅ Video saqlandi.\n📺 Jami: {len(ANIME_CODES[code])} ta."
    )

# ==========================
# DONE
# ==========================
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        return

    if user_id not in waiting_for_video:
        await update.message.reply_text(
            "❌ Siz hozir anime qo'shayotganingiz yo'q."
        )
        return

    code = waiting_for_video.pop(user_id)

    await update.message.reply_text(
        f"🎉 {code} saqlandi!\n"
        f"📺 Jami: {len(ANIME_CODES[code])} ta video."
    )

# ==========================
# SEARCH
# ==========================
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.upper()

    if code not in ANIME_CODES:
        await update.message.reply_text("❌ Bunday kod topilmadi.")
        return

    for file_id in ANIME_CODES[code]:
        await update.message.reply_video(file_id)

# ==========================
# APP
# ==========================
load_data()
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("done", done))

# Video + Document
app.add_handler(
    MessageHandler(
        filters.VIDEO | filters.Document.ALL,
        save_video
    )
)

# Kod qidirish
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        search
    )
)

print("✅ Bot ishga tushdi...")
app.run_polling()
