import time,subprocess,requests

def send_message(message,chat_id):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data={'chat_id':chat_id,'text':message,'parse_mode':'Markdown'})
        return {'ok':True,'result':result.status_code}
    except Exception as error:
        return {'ok':False,'result':error}

def send_photo(path,caption,chat_id):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendPhoto', data={'chat_id':chat_id,'caption':caption},files={'photo':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error:
        return {'ok':False,'result':error}

def send_video(path,caption,chat_id):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendVideo', data={'chat_id':chat_id,'caption':caption},files={'video':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error:
        return {'ok':False,'result':error}

def send_audio(path,caption,chat_id):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendAudio', data={'chat_id':chat_id,'caption':caption},files={'audio':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error:
        return {'ok':False,'result':error}

def send_document(path,caption,chat_id):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendDocument', data={'chat_id':chat_id,'caption':caption},files={'document':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error:
        return {'ok':False,'result':error}

def get_update():
    try:
        result = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates',timeout=5)
        return {'ok':True,'result':result.json()}
    except Exception as error:
        return {'ok':False,'result':error}

def gen_response(cmd):
    try:
        parts = cmd.strip().split()
        if not parts: return {'result':f'*status:* `command not given`','type':'message'}
        cmdlen = len(parts)
        main = parts[0]
        if cmdlen == 1 and main.lower() == 'active': return {'result':f'*status:* `active`','type':'message'}
        elif cmdlen > 1 and main == ':':
            result = subprocess.run(parts[1:],capture_output=True,text=True,timeout=5)
            if result.stderr: return {'result':f'*error(out):* ```{result.stderr}```','type':'message'}
            if result.stdout: return {'result':f'*result(out):*\n```{result.stdout}```','type':'message'}
            return {'result':'*result(out):* `executed`','type':'message'}
        else: return {'result':f'*status:* `invalid`','type':'message'}
    except Exception as error:
        return {'result':f'*error:* `{error}`','type':'message'}

seen_id = []
admin_id = 7589082187
print('running....\n')
bot_token = '8498919917:AAEJrci5vCXGL2_uvpYHyFhv6qGEi1iohqI'

while True:
    try:
        update = get_update()
        if not update['ok']:
            print('update error:',update['result'],'\n')
            time.sleep(1)
            continue
        update = update['result']
        if not update['ok']:
            print('api error:',update['result'],'\n')
            time.sleep(1)
            continue
        update = update['result']
        if not update:
            print('message not found:',update,'\n')
            time.sleep(1)
            continue
        update = update[-1]
        update_id = update['update_id']
        if update_id in seen_id:
            time.sleep(1)
            continue
        chat_id = update['message']['chat']['id']
        if chat_id != admin_id:
            print('skipping unknown user:',chat_id,'\n')
            time.sleep(1)
            continue
        try:
            message = update['message']['text']
        except KeyError:
            print('send warning:',send_message('*error:* `invalid text format`',admin_id))
            print('error: invalid text format','\n')
            seen_id.append(update_id)
            time.sleep(1)
            continue
        response = gen_response(message)
        if response['type'] == 'message':
            print('message send:',send_message(response['result'],admin_id),'\n')
            seen_id.append(update_id)
        time.sleep(1)
    except Exception as error:
        print('main eror:',error)
        time.sleep(1)
        continue
