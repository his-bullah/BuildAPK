import time
from jnius import autoclass

# Idhu unga service-oda main loop
def run_service():
    while True:
        print("Ennoda Foreground Service run aagitu irukku!")
        # 5 seconds-kku oru thadava print aagum
        time.sleep(5) 

if __name__ == '__main__':
    run_service()
