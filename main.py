from datetime import datetime, timedelta
import time
import requests
import os

URL = os.environ['URL']
ENTRY_TIME = os.environ['ENTRY_TIME']
ENTRY_STATUS = os.environ['ENTRY_STATUS']
ENTRY_PLAYERS = os.environ['ENTRY_PLAYERS']
ENTRY_MOTD = os.environ['ENTRY_MOTD']
TIME_FORMAT = '%m-%d-%Y %#I:%M:%S.%f %p'

def main():
    while True:
        time.sleep(delay_calc())
        print(f'Checking server stats @ {datetime.now().strftime(TIME_FORMAT)}')
        
        try: request = requests.get(f'https://api.mcsrvstat.us/2/9b9t.com').json()
        except Exception as error:
            print('Error Receiving Data', error)
            return
        
        data = {
            ENTRY_TIME:str(time.time()),
            ENTRY_STATUS:'Offline',
            ENTRY_PLAYERS:'',
            ENTRY_MOTD:''
        }

        if request.get('online'):
            data[ENTRY_STATUS] = 'Online',
            data[ENTRY_PLAYERS] = request['players']['online'],
            data[ENTRY_MOTD] = request['motd']['clean'][0]
        
        try: requests.post(URL, data=data)
        except Exception as error:
            print('Error Sending Data', error)
 
# Initial Loop Start Delay Calc
def delay_calc():
    now = datetime.now()
    print(f'Starting delay calc @ {now.strftime(TIME_FORMAT)}')
    next_execution = now + (timedelta(minutes=10) - timedelta(minutes=now.minute % 10)) - timedelta(seconds=now.second, microseconds=now.microsecond)
    delay = datetime.timestamp(next_execution) - datetime.timestamp(now)
    print(f'Calculated next request in {delay}s @ {next_execution.strftime(TIME_FORMAT)}')
    return delay

if __name__ == '__main__':
    main()