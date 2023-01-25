import os
import time
import random
import requests
import hashlib

from dotenv import load_dotenv
load_dotenv()
apiKey = os.getenv('CF_KEY')
secret = os.getenv('CF_SECRET')
handle = os.getenv('CF_HANDLE')

rand = ""
for i in range(0, 6):
    ch = chr(random.randint(48, 57))
    rand += ch

def API_call(method, param):
    req = "https://codeforces.com/api/" + method + "?"
    now = str(int(time.time()))

    for key in param:
        req += key + "=" + str(param[key]) + "&"
    req += "apiKey=" + apiKey + "&"
    req += "time=" + now + "&"
    req += "apiSig=" + rand

    param["apiKey"] = apiKey
    param["time"] = now
    param = dict(sorted(param.items()))

    s = rand + "/" + method + "?"
    for k in param:
        s += k + "=" + str(param[k]) + "&"
    s = s[:len(s) - 1]

    s += "#" + secret
    req += (hashlib.sha512(s.encode('utf-8'))).hexdigest()

    response = requests.get(req)
    return response.json()