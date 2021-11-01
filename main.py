from datetime import datetime, timedelta
from time import sleep
import requests
import json
import os

def playerwatcher():
    
    # Send Request
    try: res = requests.get(f'https://api.mcsrvstat.us/2/9b9t.com').json()
    except: raise Exception('PlayerCount request denied @ {datetime.now().strftime("%I:%M%p")}.')
    if res['online'] == False: raise Exception(f'Server offline @ {datetime.now().strftime("%I:%M%p")}')
    
    # Check for today's file. If it doesn't exist, create a new one
    current_date = datetime.now().strftime('%m-%d-%y')
    if f'{current_date}.json' not in os.listdir('logs'):
        with open(f'logs/{current_date}.json','r') as file:
            json.dump({}, file, indent=2)

    # Playercount
    playercount = res['players']['online']
    with open(f'logs/{current_date}.json', 'r') as file:
        data = json.load(file)
        data[datetime.now().timestamp()] = playercount
        print(f'PlayerCount logged @ {datetime.now().strftime("%I:%M%p")}.')
        with open(f'logs/{current_date}.json', 'w') as file:
            json.dump(data, file, indent=2)

    # MOTD logger
    motd = res['motd']['clean'][0]
    with open(f'logs/motds.txt', 'r') as file:
        if motd not in file.read().splitlines():
            with open(f'logs/motds.txt', 'a') as file:
                file.write(motd+'\n')
                print('Unique MOTD found and logged.')
 
# Initial Loop Start Delay Calc
def main():
    now = datetime.now()
    next_execution = now + (timedelta(minutes=10) - timedelta(minutes=now.minute % 10)) - timedelta(seconds=now.second)
    pw_delay = datetime.timestamp(next_execution) - datetime.timestamp(now)
    print(f'Calculated PW start in {pw_delay} seconds @ {next_execution}')
    sleep(pw_delay)

    # Loop
    while True:
        try: playerwatcher()
        except Exception as err: print(err)
        sleep(600)

if __name__ == '__main__': main()