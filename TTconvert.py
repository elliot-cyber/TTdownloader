import telebot
import os
from yt_dlp import YoutubeDL

# Telegram bot token
bot_token = '7586237226:AAHPMFLJKX91meJaUdlhQKHvOz2n41PRZnI'  # Token kamu
bot = telebot.TeleBot(bot_token)

# Fungsi untuk mengunduh dan mengonversi TikTok ke MP3
def download_tiktok_as_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info)
        mp3_file = file_name.rsplit('.', 1)[0] + '.mp3'
        
        return mp3_file

# Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Kirimkan link TikTok yang ingin kamu konversi menjadi MP3.")

# Command untuk menerima link TikTok
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    if "tiktok.com" in url:
        bot.reply_to(message, "Mengunduh dan mengonversi video TikTok ke MP3, mohon tunggu sebentar...")
        
        try:
            mp3_file = download_tiktok_as_mp3(url)
            
            # Kirim file MP3 ke pengguna
            with open(mp3_file, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            
            # Hapus file setelah dikirim
            os.remove(mp3_file)
        except Exception as e:
            bot.reply_to(message, f"Terjadi kesalahan: {str(e)}")
    else:
        bot.reply_to(message, "Link tidak valid. Harap kirimkan link TikTok yang benar.")

# Start bot
if __name__ == '__main__':
    bot.polling()
