
bot_token = "8498919917:AAEJrci5vCXGL2_uvpYHyFhv6qGEi1iohqI"
chat_id = "7589082187"
message = "Hello from Python APP!"

import time
import requests

def run_service():
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"

    # Loop start aagudhu
    while True:
        try:
            # Internet irukka nu try pannum
            response = requests.get(url, timeout=5) # timeout kudukkuradhu romba nalladhu
            print(f"SERVICE LOG: Message sent! Status - {response.status_code}", flush=True)
            
        except requests.exceptions.RequestException as e:
            # Net off-la irundha, script crash aagadhu! Indha error print aagittu, adutha line-kku pogum
            print(f"SERVICE LOG: No Internet! Aana service crash aagala. Error: {e}", flush=True)
            
        except Exception as e:
            # Vera edhavadhu error vandhalum service saagadhu
            print(f"SERVICE LOG: Unknown Error: {e}", flush=True)
        
        # Net irundhalum, illanaalum 5 seconds wait pannittu marubadiyum try pannum
        time.sleep(5)

if __name__ == '__main__':
    run_service()
