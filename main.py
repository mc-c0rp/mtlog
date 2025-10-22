from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType

import asyncio
import db
from telebot import TeleBot

SESSION_NAME = "mtlog_session" 
API_ID = 12345678 # your app id from my.telegram.org/apps
API_HASH = "" # your app hash from my.telegram.org/apps
MY_ID = 123456780 # your telegram account id
BOT_TOKEN = '1234567890:EXAMPLE' # your telegram bot token

bot = TeleBot(BOT_TOKEN, 'HTML')
BOT_ID = bot.get_me().id

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

@app.on_deleted_messages()
async def deleted_messages_handler(client: Client, messages: list[Message]):
    for message in messages:
        saved_message = db.read_message(message.id)
        if saved_message is None:
            continue
        if saved_message['type'] == 'photo':
            bot = TeleBot(BOT_TOKEN, 'HTML')
            with open(f'downloads/{saved_message["id"]}.jpg', "rb") as photo:
                bot.send_photo(MY_ID, photo, caption=f'<a href="https://t.me/{saved_message["username"]}">{saved_message["first_name"]} {saved_message["last_name"]}</a> удалил(а) сообщение:')
            db.delete_message(message.id)
            print(f"Message with ID {message.id} from user @{saved_message['username']} and text (media) was deleted.")
            return
        elif saved_message['type'] == 'video':
            bot = TeleBot(BOT_TOKEN, 'HTML')
            with open(f'downloads/{saved_message["id"]}.mp4', "rb") as video:
                bot.send_video(MY_ID, video, caption=f'<a href="https://t.me/{saved_message["username"]}">{saved_message["first_name"]} {saved_message["last_name"]}</a> удалил(а) сообщение:')
            db.delete_message(message.id)
            print(f"Message with ID {message.id} from user @{saved_message['username']} and text (media) was deleted.")
            return
        elif saved_message['type'] == 'voice':
            bot = TeleBot(BOT_TOKEN, 'HTML')
            with open(f'downloads/{saved_message["id"]}.ogg', "rb") as voice:
                bot.send_message(MY_ID, f'<a href="https://t.me/{saved_message["username"]}">{saved_message["first_name"]} {saved_message["last_name"]}</a> удалил(а) сообщение:')
                bot.send_audio(MY_ID, voice)
            db.delete_message(message.id)
            print(f"Message with ID {message.id} from user @{saved_message['username']} and text (voice) was deleted.")
            return
        elif saved_message['type'] == 'video_note':
            bot = TeleBot(BOT_TOKEN, 'HTML')
            with open(f'downloads/{saved_message["id"]}.mp4', "rb") as video:
                bot.send_message(MY_ID, f'<a href="https://t.me/{saved_message["username"]}">{saved_message["first_name"]} {saved_message["last_name"]}</a> удалил(а) сообщение:')
                bot.send_video_note(MY_ID, video)
            db.delete_message(message.id)
            print(f"Message with ID {message.id} from user @{saved_message['username']} and text (video_note) was deleted.")
            return

        bot.send_message(MY_ID, f'<a href="https://t.me/{saved_message["username"]}">{saved_message["first_name"]} {saved_message["last_name"]}</a> удалил(а) сообщение:\n<code>{saved_message["text"]}</code>')
        db.delete_message(message.id)
        print(f"Message with ID {message.id} from user @{saved_message['username']} and text '{saved_message['text']}' was deleted.")

@app.on_message()
async def new_message_handler(client: Client, message: Message):
    if message.text != None and message.from_user.id == BOT_ID and '/clear' in message.text:
        bot = TeleBot(BOT_TOKEN, 'HTML')
        bot.send_message(MY_ID, 'удаляю все сообщения в памяти...')
        db.clean_messages()
        bot.send_message(MY_ID, 'все сообщения в памяти удалены')
    if message.from_user.id == MY_ID or message.from_user.id == BOT_ID:
        return
    if message.chat.type != ChatType.PRIVATE:
        return
    if message.photo:
        await message.download(file_name=f"downloads/{message.id}.jpg")
        db.add_message(message.id, message.text, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 'photo')
        print(f"New message from @{message.from_user.username}: (media) | added to list")
        return
    elif message.video:
        await message.download(file_name=f"downloads/{message.id}.mp4")
        db.add_message(message.id, message.text, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 'video')
        print(f"New message from @{message.from_user.username}: (media) | added to list")
        return
    elif message.voice:
        await message.download(file_name=f"downloads/{message.id}.ogg")
        db.add_message(message.id, message.text, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 'voice')
        print(f"New message from @{message.from_user.username}: (voice) | added to list")
        return
    elif message.video_note:
        await message.download(file_name=f"downloads/{message.id}.mp4")
        db.add_message(message.id, message.text, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 'video_note')
        print(f"New message from @{message.from_user.username}: (video_note) | added to list")
        return
    
    db.add_message(message.id, message.text, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 'text')
    print(f"New message from @{message.from_user.username}: {message.text} | added to list")

print('started!')
app.run()
