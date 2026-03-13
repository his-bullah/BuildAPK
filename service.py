import time,subprocess,requests

bot_token = "8498919917:AAEJrci5vCXGL2_uvpYHyFhv6qGEi1iohqI"

def send_message(message,chat_id):
    try:
        result = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id":chat_id,"text":message,"parse_mode":"Markdown"})
        return {"ok":True,"result":result.status_code}
    except Exception as error:
        return {"ok":False,"result":error}

def send_photo(photo,caption,chat_id):
    try:
        result = requests.post(f"https://api.telegram.org/bot{bot_token}/sendPhoto", data={"chat_id":chat_id,"caption":caption},files={"photo":photo})
        return {"ok":True,"result":result.status_code}
    except Exception as error:
        return {"ok":False,"result":error}

def send_video(video,caption,chat_id):
    try:
        result = requests.post(f"https://api.telegram.org/bot{bot_token}/sendVideo", data={"chat_id":chat_id,"caption":caption},files={"video":video})
        return {"ok":True,"result":result.status_code}
    except Exception as error:
        return {"ok":False,"result":error}

def send_audio(audio,caption,chat_id):
    try:
        result = requests.post(f"https://api.telegram.org/bot{bot_token}/sendAudio", data={"chat_id":chat_id,"caption":caption},files={"audio":audio})
        return {"ok":True,"result":result.status_code}
    except Exception as error:
        return {"ok":False,"result":error}

def send_document(document,caption,chat_id):
    try:
        result = requests.post(f"https://api.telegram.org/bot{bot_token}/sendDocument", data={"chat_id":chat_id,"caption":caption},files={"document":document})
        return {"ok":True,"result":result.status_code}
    except Exception as error:
        return {"ok":False,"result":error}

def get_update():
    try:
        result = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates",timeout=5)
        return {"ok":True,"result":result.json()}
    except Exception as error:
        return {"ok":False,"result":error}

def gen_response(cmd):

    parts = cmd.strip().split()

    if not parts:
        return {"ok":False,"result":"cmd not given"}

    cmdlen = len(parts)

    main = parts[0]

    if cmdlen == 1 and main == "Hi":
        return {"ok":True,"result":"Wellcome nanba...","type":"text"}
    elif cmdlen == 1 and main == "Active":
        return {"ok":True,"result":"Active nanba...","type":"text"}
    elif cmdlen > 1 and main == "$":
        result = subprocess.getoutput(' '.join(parts[1:]))
        return {"ok":True,"result":f"```{result}```","type":"text"}
    else:
        return {"ok":True,"result":"Invalid command nanba...","type":"text"}

seen_id = []

print("running....")

while True:

    try:

        update = get_update()

        if not update['ok']:
            print("error:",update['result'])
            time.sleep(1)
            continue

        update = update["result"]

        if not update['ok']:
            print("error:",update['result'])
            time.sleep(1)
            continue

        update = update['result']

        if not update:
            print("error: message not found",update)
            time.sleep(1)
            continue

        update = update[-1]

        update_id = update['update_id']

        if update_id in seen_id:
            time.sleep(1)
            continue

        chat_id = update['message']['chat']['id']

        try:
            text = update['message']['text']
        except KeyError:
            print("error: invalid text format")
            time.sleep(1)
            continue

        response = gen_response(text)

        if response['ok'] and response['type'] == 'text':
            print(send_message(response['result'],chat_id))
            seen_id.append(update_id)
            print('message send')
        
        time.sleep(1)

    except Exception as error:
        print('>>>',error)
