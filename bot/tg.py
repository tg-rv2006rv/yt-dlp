import os
#from bot import chat_info
import time
import logging
from bot.utils import humanbytes, get_duration, get_thumbnail, progress_for_pyrogram
from bot import userbot


class tgUploader:
    def __init__(self, app, msg, messageid):
        self.app = app
        self.userbot = userbot
        self.msg = msg
        self.messageid = messageid
        self.__sent_msg = ''
        self.__ldump = "-1001963446260"

    def upload_file(self, file_path):
        try:
            file_name = os.path.basename(file_path)  
            duration = get_duration(file_name)
            thumb = get_thumbnail(file_name, "", duration / 2)

            file_size = humanbytes(os.stat(file_path).st_size)
            logging.info(file_size)
            if int(file_size.split( )[0].split('.')[0]) < 2 or (file_size.split( )[1] == "GB" and int(file_size.split( )[0].split('.')[0]) < 2 ) or (file_size.split( )[1] == "MB") or (file_size.split( )[1] == "KB")  :
                self.userbot = self.app

            caption = '''<code>{}</code>'''.format(file_name)

            msg5 = True
            progress_args_text = "<code>[+]</code> <b>{}</b>\n<code>{}</code>".format("Uploading Be Patient", file_name)
            if msg5:
                for channel_id in self.__ldump.split():
                    dump_chat = self.app.get_chat(int(channel_id))
                    nrml = self.userbot.send_video(
                               video=file_path, 
                               chat_id=dump_chat.id, 
                               caption=caption, 
                               progress=progress_for_pyrogram, 
                               progress_args=(
                                       progress_args_text,
                                       self.msg, 
                                       time.time()
                               ), thumb=thumb, duration=duration, width=1280, height=720
                           )

                try:
                    
                    
                    self.app.copy_message(self.messageid, nrml.chat.id, nrml.id)
                    self.msg.reply_text("Sent In PM")
                except Exception as e:
                    logging.info(e)
                    self.__sent_msg = nrml
                    self.msg.reply_text("Not Sent In Dm Start Bot in Dm")
            else:
                self.app.send_video(
                           video=file_path, 
                           chat_id=self.msg.chat.id, 
                           caption=caption, 
                           progress=progress_for_pyrogram, 
                           progress_args=(
                                   progress_args_text,
                                   self.msg, 
                                   time.time()
                           ), thumb=thumb, duration=duration, width=1280, height=720
                       )
            
            os.remove(file_path)
            os.remove(thumb)
            self.msg.delete()
        except Exception as e:
            print(e)
