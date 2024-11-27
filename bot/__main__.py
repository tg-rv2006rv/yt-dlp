from pyrogram import Client, filters as Filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import yt_dlp
from bot import queue
import subprocess
import threading
import time
LANG_MAP = {     "en": "English",     "hi": "Hindi",     "gu": "Gujarati",     "ta": "Tamil",     "te": "Telugu",     "kn": "Kannada",     "mr": "Marathi",     "ml": "Malayalam",     "bn": "Bengali",     "bho": "Bhojpuri",     "pa": "Punjabi",     "or": "Oriya" }
jiodl = 'bot/jiod'
from bot import app
proxy = "0"
def download_video(url, format, message):
    if proxy != "0":
        for audio, video in format.items():
           jio_cmd = [f"{jiodl}", "-f", f"{audio}+{video}", "--proxy", f"{proxy}",  "-P", "downloads", "--cache-dir", "temp", f"{url}"]

    for audio, video in format.items():
        print(f"{audio}+{video}")
        jio_cmd = [f"jiod", "-f", f"bestaudio[language={audio}]+{video}", f"{url}"]
    try:
        process = subprocess.run(jio_cmd)
        while process.poll() is None:
            output = process.stdout.readline().decode('utf-8')
            if 'Downloading' in output:
                speed = output.split('at')[1].strip()
                message.edit(f'Downloading video at {speed}...')
                time.sleep(1)
    except Exception as e:
        print(e)
    directory = "downloads"
 #    file_name = os.listdir("downloads")[0]

    #file_path = yt_dlp.utils.get_downloaded_file(url)
    from yt_dlp import YoutubeDL

    ydl_opts = {}
    ydl = YoutubeDL(ydl_opts)
    info = ydl.extract_info(url, download=False)
    filename = ydl.prepare_filename(info)
    file_path = f"{filename}"
#    for file in os.listdir(directory):
 #           if file.endswith(".mkv") or file.endswith(".mp4"):
  #              file_path = os.path.join(directory, file)
    from bot.tg import tgUploader
    try:
        uploader = tgUploader(app, message, 7126874550)
        uploader.upload_file(file_path)
    except Exception as e:
        message.reply_text(f"UPLOADING failed Contact Developer @aryanchy451{e}")
#    split_and_upload_video(file_path, message)

def split_and_upload_video(file_name, message):
    file_size = os.path.getsize(file_name)
    chunk_size = 2047152000
    chunk_count = 0
    
    if file_size > chunk_size:
        app.send_message(message.chat.id, 'File size exceeds 2GB, splitting into chunks...')
        
        with open(file_name, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunk_count += 1
                chunk_file_name = f'{file_name}.part{chunk_count}'
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                app.send_document(message.chat.id, chunk_file_name, caption=f'Video chunk {chunk_count}')
                os.remove(chunk_file_name)
        
        message.edit('Video uploaded successfully!')
    else:
        app.send_video(message.chat.id, file_name, caption='Video uploaded by JioCinema Downloader Bot')
        message.edit('Video uploaded successfully!')
        os.remove(file_name)
@app.on_message(Filters.command('start'))
def start_command(client, message):
    app.send_message(message.chat.id, 'Send a JioCinema link to download!')
@app.on_message(Filters.regex(r'^https:'))
def youtube_link(client, message):
    url = message.text
    keyboard = []
    for format, key in LANG_MAP.items():
        print(format)
        keyboard.append([InlineKeyboardButton(f"{key}", callback_data=f"audio_{format}_{message.from_user.id}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text(f'Select a audio format to download For :{url}', reply_markup=reply_markup)
@app.on_callback_query(Filters.regex(r'^audio_.*$'))
def video(_, query):
    audio = query.data.split('_')[1]
    url = query.message.text.split(":",maxsplit=1)[1]
    keyboard = []
    keyboard.append([InlineKeyboardButton("1080p", callback_data=f"download_{audio}_hls-2571")])
    keyboard.append([InlineKeyboardButton("720p Low Quality", callback_data=f"download_{audio}_hls-735")])
    keyboard.append([InlineKeyboardButton("720p", callback_data=f"download_{audio}_hls-981")])
    keyboard.append([InlineKeyboardButton("1080p Low Quality", callback_data=f"download_{audio}_hls-1405")])
    keyboard.append([InlineKeyboardButton("480p", callback_data=f"download_{audio}_hls-261")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = app.send_message(query.message.chat.id, f'Select a video format to download For :{url}', reply_markup=reply_markup)
    query.message.delete()
    sleep(30)
    msg.delete()

@app.on_callback_query(Filters.regex(r'^download_.*$'))
def download_button(_, callback_query):
    url = callback_query.message.text.split(":",maxsplit=1)[1]
    video = callback_query.data.split('_')[2]
    audio = callback_query.data.split('_')[1]
    format = {audio:video}
    message = app.send_message(callback_query.message.chat.id, f'Downloading ...')
    download_video(url, format, message)
app.start()
idle()
app.stop()

