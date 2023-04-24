import time
import random
import datetime
from colorama import Fore

# get time
def get_real_time():
    return int(time.time())

# get random 6 digits for api_call
def gen_rand() -> str: 
    rand = ""
    for i in range(0, 6):
        ch = chr(random.randint(48, 57))
        rand += ch
    return rand

#get time in date format
def get_date_time(secs):
    return datetime.datetime.fromtimestamp(secs)

# get time in hourly format
def get_contest_time(secs):
    res: str = ""
    res += str(int(secs / 3600)) + ":"
    if int((secs % 3600) / 60) < 10:
        res += "0"
    res += str(int((secs % 3600) / 60))
    return res

#    Set color based on rating
def get_color(num):
    if num < 1200:
        return Fore.WHITE
    elif num < 1400:
        return Fore.GREEN
    elif num < 1600:
        return Fore.CYAN
    elif num < 1900:
        return Fore.BLUE
    elif num < 2100:
        return Fore.MAGENTA
    elif num < 2400:
        return Fore.YELLOW
    else:
        return Fore.RED