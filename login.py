#!/usr/bin/env python3
import os
import sys
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded

def main():
    api_id = 123456 # your app id
    api_hash = '' # your app hash
    phone = '+3731337666' # your phone
    password = 'example' # your 2FA pass (or don't touch this if you don't have 2FA)
    session_name = 'mtlog_session' # session file name (may not touch this)

    app = Client(session_name, api_id=api_id, api_hash=api_hash)

    print(f'creating session -> {phone} | {session_name}')
    app.connect()

    try:
        print('sending code...')
        sent_code = app.send_code(phone)
        code = input('enter code from Telegram: ')
        print('signing in...')
        app.sign_in(phone, sent_code.phone_code_hash, code)
    except SessionPasswordNeeded:
        print('checking 2FA...')
        app.check_password(password)

    me = app.get_me()
    print(f'logged as @{me.username} ({me.id}) | session saved -> {session_name}.session')

    app.disconnect()

if __name__ == "__main__":
    main()
