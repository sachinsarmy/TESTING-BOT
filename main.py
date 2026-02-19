import os
import logging
import sqlite3
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    ChatJoinRequestHandler,
    CommandHandler,
)

# ================= CONFIG =================
BOT_TOKEN = "8419709904:AAHZj2v9_qwvC8Pw_ksX53EATcSaSTwHSkM"
ADMIN_ID = 7849592882  # ← your telegram numeric id
APK_PATH = "𝗥ᴀᴊᴀ_𝗚ᴀᴍᴇ_𝗣ᴀɴᴇʟ_𝗛ᴀᴄᴋ.apk"
VOICE_PATH = "VOICEHACK.ogg"
DB_NAME = "users.db"
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ================= DATABASE =================
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)"
)
conn.commit()


def add_user(user_id: int):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,),
    )
    conn.commit()


def get_all_users():
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]


def remove_user(user_id: int):
    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()


# ================= COMMON SEND =================
async def send_welcome_package(user, context: ContextTypes.DEFAULT_TYPE):
    add_user(user.id)

    welcome_message = f"""
👋🏻 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 {user.mention_html()} 𝐁𝐑𝐎𝐓𝐇𝐄𝐑 𝐓𝐎 𝗢𝗨𝗥 - 𝐑𝐀𝐉𝐀 𝐏𝐑𝐈𝐕𝐀𝐓𝐄 𝐇𝐀𝐂𝐊 𝐒𝐄𝐑𝐕𝐄𝐑 🤑💵
"""

    await context.bot.send_message(
        chat_id=user.id,
        text=welcome_message,
        parse_mode="HTML",
    )

    # ---------- APK ----------
    if os.path.exists(APK_PATH):
        with open(APK_PATH, "rb") as apk:
            await context.bot.send_document(
                chat_id=user.id,
                document=apk,
                caption="""📂 ☆𝟏𝟎𝟎% 𝐍𝐔𝐌𝐁𝐄𝐑 𝐇𝐀𝐂𝐊💸

(केवल प्रीमियम उपयोगकर्ताओं के लिए)💎
(𝟏𝟎𝟎% नुकसान की भरपाई की गारंटी)🧬

♻सहायता के लिए @RDX_SONU_01
🔴हैक का उपयोग कैसे करें
https://t.me/rajaindiaprediction/54"""
            )

    # ---------- VOICE ----------
    if os.path.exists(VOICE_PATH):
        with open(VOICE_PATH, "rb") as voice:
            await context.bot.send_voice(
                chat_id=user.id,
                voice=voice,
                caption="""🎙 सदस्य 9X गुना लाभ का प्रमाण 👇🏻
https://t.me/rajaindiaprediction/56

♻सहायता के लिए @RDX_SONU_01
लगातार नंबर पे नंबर जीतना 🤑♻👑"""
            )


# ================= /START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await send_welcome_package(user, context)


# ================= JOIN REQUEST =================
async def approve_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    if not request:
        return

    user = request.from_user
    await send_welcome_package(user, context)


# ================= BROADCAST =================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to message to broadcast.")
        return

    users = get_all_users()
    total = len(users)

    progress_msg = await update.message.reply_text(
        "🚀 Broadcasting started...\n\n0%"
    )

    success = 0
    failed = 0

    for index, user_id in enumerate(users, start=1):
        try:
            await update.message.reply_to_message.copy(chat_id=user_id)
            success += 1
        except:
            remove_user(user_id)
            failed += 1

        # 🔥 ANIMATED PROGRESS UPDATE
        if index % 10 == 0 or index == total:
            percent = int((index / total) * 100)
            try:
                await progress_msg.edit_text(
                    f"""🚀 Broadcasting in progress...

📤 Processed: {index}/{total}
📊 Progress: {percent}%"""
                )
            except:
                pass

        await asyncio.sleep(0.03)  # anti-flood safety

    active_users = success

    await progress_msg.edit_text(
        f"""✅ Broadcast Completed

📤 Sent Successfully: {success}
❌ Failed/Blocked: {failed}
👥 Active Users: {active_users}
📊 Total Database: {len(get_all_users())}"""
    )


# ================= USERS COUNT =================
async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total = len(get_all_users())
    await update.message.reply_text(f"👥 Total Users: {total}")


# ================= MAIN =================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users_count))
    app.add_handler(ChatJoinRequestHandler(approve_and_send))

    app.run_polling(allowed_updates=["message", "chat_join_request"])


if __name__ == "__main__":
    main()

