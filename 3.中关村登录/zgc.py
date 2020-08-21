from config import userinfo
username = userinfo.get('username')
password = userinfo.get('password')
import requests
import execjs,re

session = requests.Session()

def get_pwd(pwd):
    with open('zgc.js','r') as f:
        js_code = f.read()
    res = execjs.compile(js_code).call("get_pwd",pwd)
    return res

def check_ip():
    HEADER = {
        "user-agent":"mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/83.0.4103.97 safari/537.36",
    }

    url = 'http://zdw.w8.com.cn/p.ht?h=&t=1592272&c='

    ret = session.get(url,headers = HEADER)

    pattern = r"third_ip_ck = '(.*?)'"
    ip_ck = re.findall(pattern,ret.text)[0]
    session.cookies.set('ip_ck',ip_ck)
    print(session.cookies)

def login():
    check_ip()
    pwd = get_pwd(password)
    url = 'http://service.zol.com.cn/user/ajax/siteLogin/login.php'
    
    data = {
        "userid":username,
        "pwd":pwd,
        "iSauto":"1",
        "backurl":"http://www.zol.com.cn/",
        "tmalLbtn":"0",
        "activEbtn":"0",
        "heaDpicid":"0",
    }
    headers = {
        "content-type":"application/x-www-form-urlencoded; charseT=UTF-8",
        "host":"service.zol.com.cn",
        "origin":"http://service.zol.com.cn",
        "pragma":"no-cache",
        "referer":"http://service.zol.com.cn/user/siTelogin.php?type=small&callback=usErlogIncallback&backurl=http://www.zol.com.cn/",
        "user-agent":"mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/83.0.4103.97 safari/537.36",
        "X-requested-with":"XMlhtTprequest",
    }
    res = session.post(url,data=data,headers=headers)
    print(res.json())

        
if __name__ == "__main__":
    login()

