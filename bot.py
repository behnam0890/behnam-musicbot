import logging
import glob
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "7305373575:AAGhyJWh3QEaSLCIx0Qeg84unZu8zQlIBys"
DOWNLOAD_PATH = "/tmp/"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 🎵\nاسم آهنگ، لینک یوتیوب یا اینستاگرام بفرست!")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("⏳ دارم دانلود میکنم...")
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": DOWNLOAD_PATH + "%(title)s.%(ext)s",
            "default_search": "ytsearch1",
            "quiet": False
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            if "entries" in info:
                info = info["entries"][0]
            title = info.get("title", "audio")
        files = glob.glob(DOWNLOAD_PATH + "*.webm") + glob.glob(DOWNLOAD_PATH + "*.m4a") + glob.glob(DOWNLOAD_PATH + "*.mp3") + glob.glob(DOWNLOAD_PATH + "*.mp4")
        if files:
            filename = files[0]
            if filename.endswith(".mp4") or filename.endswith(".webm"):
                await update.message.reply_video(video=open(filename, "rb"), caption=title)
            else:
                await update.message.reply_audio(audio=open(filename, "rb"), title=title)
            os.remove(filename)
        else:
            await update.message.reply_text("❌ پیدا نکردم!")
    except Exception as e:
        print(e)
        await update.message.reply_text("❌ خطا! دوباره امتحان کن.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    print("ربات روشن شد! ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
