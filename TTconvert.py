import os
import re
import requests
from pytube import YouTube
from moviepy.editor import *
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Token bot Telegram kamu
TOKEN = '7586237226:AAHPMFLJKX91meJaUdlhQKHvOz2n41PRZnI'

# Fungsi untuk mengunduh video dari TikTok dan mengonversi ke MP3
def tiktok_to_mp3(tiktok_url, file_name):
    try:
        # Download video menggunakan pytube
        yt = YouTube(tiktok_url)
        video = yt.streams.filter(only_audio=True).first()
        output_path = video.download(filename=f"{file_name}.mp4")

        # Konversi video ke MP3
        video_clip = AudioFileClip(output_path)
        video_clip.write_audiofile(f"{file_name}.mp3")
        video_clip.close()

        # Hapus file video setelah konversi
        os.remove(output_path)

        return f"{file_name}.mp3"
    except Exception as e:
        print(f"Error: {e}")
        return None

# Fungsi untuk menangani pesan masuk
async def handle_message(update: Update, context):
    message_text = update.message.text

    # Validasi link TikTok
    tiktok_url = re.search(r"(https?://[^\s]+)", message_text)
    if tiktok_url:
        tiktok_url = tiktok_url.group(1)
        await update.message.reply_text("Sedang mengunduh dan mengonversi video TikTok ke MP3...")

        # Proses unduh dan konversi
        mp3_file = tiktok_to_mp3(tiktok_url, "tiktok_audio")
        if mp3_file:
            # Kirim file MP3 ke pengguna
            await update.message.reply_audio(audio=open(mp3_file, 'rb'))
            os.remove(mp3_file)  # Hapus file MP3 setelah dikirim
        else:
            await update.message.reply_text("Gagal mengunduh atau mengonversi video TikTok.")
    else:
        await update.message.reply_text("Kirim link TikTok yang valid untuk diunduh!")

# Fungsi untuk memulai bot
async def start(update: Update, context):
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
