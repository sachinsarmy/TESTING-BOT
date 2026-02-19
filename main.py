import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    filters,
)

# ================= CONFIG =================
BOT_TOKEN = "8419709904:AAHZj2v9_qwvC8Pw_ksX53EATcSaSTwHSkM"
ADMIN_ID = 7849592882  # <-- PUT YOUR TELEGRAM USER ID HERE
APK_PATH = "𝗥ᴀᴊᴀ_𝗚ᴀᴍᴇ_𝗣ᴀɴᴇʟ_𝗛ᴀᴄᴋ.apk"
VOICE_PATH = "VOICEHACK.ogg"
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Store users in memory
users = set()


# ================= START COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    await update.message.reply_text("Bot Activated ✅")


# ================= JOIN REQUEST =================
async def approve_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    if not request:
        return

    user = request.from_user
    chat_id = request.chat.id

    welcome_message = f"""
👋🏻 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 {user.mention_html()}
"""

    await context.bot.send_message(
        chat_id=user.id,
        text=welcome_message,
        parse_mode="HTML",
    )

    if os.path.exists(APK_PATH):
        with open(APK_PATH, "rb") as apk:
            await context.bot.send_document(
                chat_id=user.id,
                document=apk,
                caption="📂 Premium File"
            )

    if os.path.exists(VOICE_PATH):
        with open(VOICE_PATH, "rb") as voice:
            await context.bot.send_voice(
                chat_id=user.id,
                voice=voice,
                caption="🎙 Proof"
            )


# ================= BROADCAST =================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a message to broadcast.")
        return

    msg = update.message.reply_to_message
    success = 0
    failed = 0

    for user_id in users.copy():
        try:
            await msg.copy(chat_id=user_id)
            success += 1
        except:
            failed += 1

    await update.message.reply_text(
        f"Broadcast Complete ✅\n\nSuccess: {success}\nFailed: {failed}"
    )


# ================= MAIN =================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(ChatJoinRequestHandler(approve_and_send))

    app.run_polling(
        allowed_updates=["message", "chat_join_request"]
    )


if __name__ == "__main__":
    main()

