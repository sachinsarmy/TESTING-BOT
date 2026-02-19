import os
from telegram import Update
from telegram.ext import Application, ContextTypes

try:
    from telegram.ext import ChatJoinRequestHandler
except ImportError:
    raise ImportError("ChatJoinRequestHandler is only available in python-telegram-bot v20+. Please upgrade your library.")

FILE_PATH = "/file/RAJA_VIP_NUMBER_HACK.zip"
VOICE_PATH = "VOICEHACK.ogg"

async def approve_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = getattr(update, "chat_join_request", None)
    if request is None:
        return  # Ignore updates that are not join requests

    user = request.from_user

    # Approve the user
    await request.approve()

    # Build welcome message with username
    welcome_message = f"""
👋🏻 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 {user.mention_html()} 𝐁𝐑𝐎𝐓𝐇𝐄𝐑
 𝐓𝐎 𝗢𝗨𝗥 - 𝐕𝟑_𝐏𝐀𝐍𝐄𝐋  𝐏𝐑𝐈𝐕𝐀𝐓𝐄  𝐇𝐀𝐂𝐊 𝐒𝐄𝐑𝐕𝐄𝐑 🤑💵
  
    """

    # Send welcome message
    await context.bot.send_message(chat_id=user.id, text=welcome_message, parse_mode="HTML")

    # Send file
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            await context.bot.send_document(chat_id=user.id, document=f, caption="""
📂 ☆𝟏𝟎𝟎% 𝐍𝐔𝐌𝐁𝐄𝐑 𝐇𝐀𝐂𝐊💸

(केवल प्रीमियम उपयोगकर्ताओं के लिए)💎

(100% नुकसान की भरपाई की गारंटी)🧬

♻सहायता के लिए @RAJ_A_G_E_N_T

🔴हैक का उपयोग कैसे करें💱
https://t.me/rajaindiaprediction/54

☆ 🚀""")
    else:
        await context.bot.send_message(chat_id=user.id, text="Sorry, the requested file is not available.")

    # Send voice message (if available)
    if os.path.exists(VOICE_PATH):
        with open(VOICE_PATH, "rb") as v:
            await context.bot.send_voice(chat_id=user.id, voice=v, caption="""
🎙 सदस्य 9X गुना लाभ का प्रमाण 👇🏻 -

https://t.me/rajaindiaprediction/54

लगातार नंबर पे नंबर जीतना 🤑♻👑
""")
    else:
        await context.bot.send_message(chat_id=user.id, text="Sorry, the requested voice message is not available.")

def main():
    app = Application.builder().token("8157438383:AAF2hzj6X0CJVDnYOLcR8YUYoUM0r0KKtl0").build()
    app.add_handler(ChatJoinRequestHandler(approve_and_send))
    app.run_polling()

if __name__ == "__main__":
    main()