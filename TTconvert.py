import os
import re
import requests
from moviepy.editor import *
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token bot Telegram kamu
TOKEN = '7586237226:AAHPMFLJKX91meJaUdlhQKHvOz2n41PRZnI'

# Fungsi untuk mengunduh video dari API pihak ketiga dan mengonversi ke MP3
def download_tiktok_video(tiktok_url, file_name):
    try:
        # Gunakan API pihak ketiga seperti ttsave.app atau yang lainnya
        api_url = f"https://ttsave.app/download?url={tiktok_url}"  # Contoh API
        response = requests.get(api_url)

        if response.status_code == 200:
            with open(f"{file_name}.mp4", 'wb') as f:
                f.write(response.content)

            # Konversi video ke MP3
            video_clip = AudioFileClip(f"{file_name}.mp4")
            video_clip.write_audiofile(f"{file_name}.mp3")
            video_clip.close()

            # Hapus file video setelah konversi
            os.remove(f"{file_name}.mp4")

            return f"{file_name}.mp3"
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Fungsi untuk menangani pesan masuk
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text

    # Validasi link TikTok
    tiktok_url = re.search(r"(https?://[^\s]+)", message_text)
    if tiktok_url:
        tiktok_url = tiktok_url.group(1)
        await update.message.reply_text("Sedang mengunduh dan mengonversi video TikTok ke MP3...")

        # Proses unduh dan konversi
        mp3_file = download_tiktok_video(tiktok_url, "tiktok_audio")
        if mp3_file:
            # Kirim file MP3 ke pengguna
            await update.message.reply_audio(audio=open(mp3_file, 'rb'))
            os.remove(mp3_file)  # Hapus file MP3 setelah dikirim
        else:
            await update.message.reply_text("Gagal mengunduh atau mengonversi video TikTok.")
    else:
        await update.message.reply_text("Kirim link TikTok yang valid untuk diunduh!")

# Fungsi untuk memulai bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim tautan video TikTok dan saya akan mengonversinya menjadi MP3.")

def main():
    # Inisialisasi bot
    application = Application.builder().token(TOKEN).build()

    # Command handler
    application.add_handler(CommandHandler("start", start))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    application.run_polling()

if __name__ == '__main__':
    main()
