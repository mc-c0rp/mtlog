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

        print(f"Message with ID {message.id} from user @{saved_message['username']} and text '{saved_message['text']}' was deleted.")

        bot = TeleBot(BOT_TOKEN, 'HTML')
        bot.send_message(MY_ID, f'<a href="https://t.me/{saved_message["username"]}">{saved_message["first_name"]} {saved_message["last_name"]}</a> удалил(а) сообщение:\n<code>{saved_message["text"]}</code>')
        db.delete_message(message.id)

@app.on_message()
async def new_message_handler(client: Client, message: Message):
    if message.chat.id == BOT_ID and '/clear' in message.text:
        bot = TeleBot(BOT_TOKEN, 'HTML')
        bot.send_message(MY_ID, 'удаляю все сообщения в памяти...')
        db.clean_messages()
        bot.send_message(MY_ID, 'все сообщения в памяти удалены')
    if message.from_user.id == MY_ID or message.from_user.id == BOT_ID:
        return
    if message.chat.type != ChatType.PRIVATE:
        return
    
    print(f"New message from @{message.from_user.username}: {message.text} | added to list")
    db.add_message(message.id, message.text, message.from_user.username, message.from_user.first_name, message.from_user.last_name)

app.run()
