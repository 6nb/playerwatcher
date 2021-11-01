from datetime import datetime, timedelta
import time
import requests
import os

URL = os.environ('URL')
ENTRY_TIME = os.environ['ENTRY_TIME']
ENTRY_STATUS = os.environ['ENTRY_STATUS']
ENTRY_PLAYERS = os.environ['ENTRY_PLAYERS']
ENTRY_MOTD = os.environ['ENTRY_MOTD']

def playerwatcher():
    
    # Send Request
    try: res = requests.get(f'https://api.mcsrvstat.us/2/9b9t.com').json()
    except Exception as err: print('GET failure:', err)

    if res.get('online') == True:
        data = {
            ENTRY_TIME:str(time.time()),
            ENTRY_STATUS:'Online',
            ENTRY_PLAYERS:res['players']['online'],
            ENTRY_MOTD:res['motd']['clean'][0]
        }
    else: 
        data = {
            ENTRY_TIME:str(time.time()),
            ENTRY_STATUS:'Offline',
            ENTRY_PLAYERS:'',
            ENTRY_MOTD:''
        }
    
    try: requests.post(URL, data=data)
    except Exception as err: print('POST failure:', err)
 
# Initial Loop Start Delay Calc
def main():
    now = datetime.now()
    next_execution = now + (timedelta(minutes=10) - timedelta(minutes=now.minute % 10)) - timedelta(seconds=now.second)
    pw_delay = datetime.timestamp(next_execution) - datetime.timestamp(now)
    print(f'Calculated PlayerWatcher start in {pw_delay} seconds @ {next_execution}')
    time.sleep(pw_delay)

    # Loop
    while True:
        try: playerwatcher()
        except Exception as err: print(err)
        time.sleep(600)

if __name__ == '__main__': main()