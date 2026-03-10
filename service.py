import requests
import time

BOT_TOKEN = "8498919917:AAEJrci5vCXGL2_uvpYHyFhv6qGEi1iohqI"
CHAT_ID = "7589082187"
TEXT = "Hello from Python APP!"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": TEXT
}

while True:
    r = requests.post(url, data=data)
    print (r.text)
    time.sleep(5)