import sqlite3
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== CONFIG ==================
BOT_TOKEN = "8419709904:AAHZj2v9_qwvC8Pw_ksX53EATcSaSTwHSkM"
ADMIN_ID = 7849592882  # 🔴 apna telegram numeric id
DB_NAME = "users.db"

# 🔥 WELCOME CONTENT (EDIT AS YOU WANT)
WELCOME_TEXT = (
    "🎉 Welcome to Raja Game Panel!\n\n"
    "🔥 Best earning platform\n"
    "📲 Join now and start winning!"
)

WELCOME_VOICE = "VOICEHACK.ogg"  # repo me present
WELCOME_FILE = "𝗥ᴀᴊᴀ_𝗚ᴀᴍᴇ_𝗣ᴀɴᴇʟ_𝗛ᴀᴄᴋ.apk"

# ================== LOGGING ==================
logging.basicConfig(level=logging.INFO)

# ================== DATABASE ==================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    return [u[0] for u in users]

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)

    # ✅ always send welcome pack
    try:
        await update.message.reply_text(WELCOME_TEXT)

        # send voice
        with open(WELCOME_VOICE, "rb") as v:
            await context.bot.send_voice(chat_id=user_id, voice=v)

        # send file
        with open(WELCOME_FILE, "rb") as f:
            await context.bot.send_document(chat_id=user_id, document=f)

    except Exception as e:
        logging.error(f"Welcome send failed: {e}")

    # admin info message
    if user_id == ADMIN_ID:
        await update.message.reply_text("✅ Bot Activated (Admin)")

# ================== BROADCAST ==================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    users = get_all_users()

    if not users:
        await update.message.reply_text("❌ No users in database.")
        return

    status_msg = await update.message.reply_text("🚀 Broadcasting started...")

    success = 0
    failed = 0
    total = len(users)

    msg = update.message

    for user_id in users:
        if user_id == ADMIN_ID:
            continue

        try:
            if msg.text:
                await context.bot.send_message(user_id, msg.text)

            elif msg.photo:
                await context.bot.send_photo(
                    user_id,
                    msg.photo[-1].file_id,
                    caption=msg.caption
                )

            elif msg.video:
                await context.bot.send_video(
                    user_id,
                    msg.video.file_id,
                    caption=msg.caption
                )

            elif msg.voice:
                await context.bot.send_voice(
                    user_id,
                    msg.voice.file_id,
                    caption=msg.caption
                )

            elif msg.document:
                await context.bot.send_document(
                    user_id,
                    msg.document.file_id,
                    caption=msg.caption
                )

            else:
                continue

            success += 1

        except Exception as e:
            failed += 1
            logging.error(f"Failed for {user_id}: {e}")

    await status_msg.edit_text(
        f"✅ Broadcast Completed\n\n"
        f"👥 Total Users: {total}\n"
        f"📬 Success: {success}\n"
        f"❌ Failed/Blocked: {failed}\n"
        f"🔥 Active Users: {success}"
    )

# ================== MAIN ==================
def main():
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(~filters.COMMAND, broadcast))

    print("🚀 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()

