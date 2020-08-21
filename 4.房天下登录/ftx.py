from config import userinfo
username = userinfo.get('username')
password = userinfo.get('password')
import requests
import execjs

def get_pwd():
    with open('ftx.js','r') as f:
        js_code = f.read()
    res = execjs.compile(js_code).call("get_pwd",password)
    return res

def login():
    pwd = get_pwd()
    url = 'https://passport.fang.com/login.api'
    
    data = {
        "uid":username,
        "pwd":pwd,
        "AutoLogin":"1",
        'Service': 'soufun-passport-web'
    }
    headers = {
        "host":"passport.fang.com",
        "origin":"https://passport.fang.com",
        "pragma":"no-cache",
        "referer":"https://passport.fang.com/?backurl=https%3A%2F%2fgz.fang.com%2F",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "user-agent":"mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/83.0.4103.97 safari/537.36",
        "X-requested-with":"XMlhtTprequest",

    }
    res = requests.post(url,data=data,headers=headers)
    print(res.json())

        
if __name__ == "__main__":
    login()