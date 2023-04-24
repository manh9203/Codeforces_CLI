import os
import requests
import hashlib
from app import helper

from dotenv import load_dotenv
load_dotenv()
apiKey = os.getenv('CF_KEY')
secret = os.getenv('CF_SECRET')
handle = os.getenv('CF_HANDLE')

def API_call(method, param):
    req = "https://codeforces.com/api/" + method + "?"
    now = str(helper.get_real_time())
    rand = helper.gen_rand()

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