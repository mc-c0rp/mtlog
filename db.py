import json
from os import path, remove, listdir

def _load_json(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_json(filename: str, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_message(id: int, text: str, username: str, first_name: str, last_name: str):
    if last_name == None:
        last_name = ''

    data = {'id': id, 'text': text, 'username': username, 'first_name': first_name, 'last_name': last_name}
    _save_json(f'messages/{id}.json', data)
    print(f'message {id} saved')

def read_message(id: int):
    if not path.exists(f'messages/{id}.json'):
        print(f'message {id} not exists')
        return None
    
    return _load_json(f'messages/{id}.json')

def delete_message(id: int):
    for msg in listdir('messages'):
        if path.isfile(msg):
            if str(id) in msg:
                remove(f'messages/{msg}')
                print(f'{msg} -> deleted')

def clean_messages():
    for msg in listdir('messages'):
        if '.json' in msg:
            remove(f'messages/{msg}')
            print(f'{msg} -> deleted')
