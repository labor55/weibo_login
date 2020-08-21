import re
import os
import json
import time
import random
import execjs
import requests
from PIL import Image
from urllib import parse
import matplotlib.pyplot as plt

from config import ACCOUNT,PASSWORD

session = requests.Session()
ua_headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
    }

# 生成13位整数时间戳
def get_timestamp():    
    timestamp = int(round(time.time()*1000))
    return timestamp

# 获取账户加密
def get_su(user):
    with open('web.js','r',encoding="utf8") as f:
        js_code = f.read()
    su = execjs.compile(js_code).call("get_su",user)
    return su

# 获取密码加密
def get_sp(me,pwd):
    with open('web.js','r',encoding="utf8") as f:
        js_code = f.read()
    sp = execjs.compile(js_code).call("get_sp",me,pwd)

    return sp

# 预登录获取参数
def prelogin(su):
    prelogin_url = "https://login.sina.com.cn/sso/prelogin.php"
    prelogin_params = {
        'entry':'weibo',
        'callback':'sinaSSOController.preloginCallBack',
        'su':su,
        'rsakt':'mod',
        'checkpin':"1",
        'client':"ssologin.js(v1.4.19)",
        "_":str(get_timestamp())
    }
    
    resp = session.get(prelogin_url,headers=ua_headers,params=prelogin_params)
    res = eval(resp.text.replace("sinaSSOController.preloginCallBack",''))
    return res

# 获取验证码
def get_captcha(pcid):
    captcha_url = 'https://login.sina.com.cn/cgi/pin.php'
    params = {
        'r':int(random.random() * 1e8),
        's':"0",
        'p':pcid,
    }
    res = session.get(url=captcha_url,headers=ua_headers,params=params)
    # 先移除之前的验证码图片
    img_path = './captcha.jpg'
    if os.path.exists(img_path):
        os.remove(img_path)
    # 生成验证码图片
    with open(img_path,r'wb') as f:
        f.write(res.content)
    # 展示验证码图片
    img = Image.open('./captcha.jpg')
    plt.imshow(img)
    plt.title('image')
    plt.show()
    captcha_code = input("请输入验证码: ")
    if captcha_code:
        return captcha_code


# 登录提交参数
def login(su,sp,me):
    login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
    login_data = {
        "entry":"weibo",
        "gateway":"1",
        "from":"",
        "savestate":"7",
        "qrcode_flag":"false",
        "useticket":"1",
        "pagerefer":'',
        "vsnf":"1",
        "su":su,
        "service":"miniblog",
        "servertime":me['servertime'],
        "nonce":me['nonce'],
        "pwencode":"rsa2",
        "rsakv":me['rsakv'],
        "sp":sp,
        "sr":"1920*1080",
        "encoding":"UTF-8",
        "prelt":me['exectime'],
        "url":"https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
        "returntype":"META",
    }
    if me.get('showpin'):
        login_data['pcid'] = me['pcid']
        login_data['door'] = get_captcha(me['pcid'])
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
        "Host":"login.sina.com.cn",
        "Origin":"https://weibo.com",
        "Pragma":"no-cache",
        "Referer":"https://weibo.com/",
        "Sec-Fetch-Dest":"iframe",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"cross-site",
        "Sec-Fetch-User":"?1",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
    }
    # 发送数据2
    resp = session.post(url=login_url,data=login_data,headers=headers)
    resp.encoding = resp.apparent_encoding
    
    # 提取响应,返回一个url，
    pattern = r'location.replace\((.*?)\);'
    result_url = eval(re.findall(pattern,resp.text)[0])
    res = session.get(url=result_url,headers=ua_headers)
    res.encoding = res.apparent_encoding
    
    # 获取参数，
    result_url = parse.unquote(result_url)
    print(result_url)
    pattern = "ssosavestate=(.*?)&"
    ssosavestate = re.findall(pattern,result_url)[0]
    pattern = 'ticket=(.*?)&'
    ticket = re.findall(pattern,result_url)[0]
    
    # 再次验证4
    pwd_url = 'https://passport.weibo.com/wbsso/login'
    params = {
        'ticket':ticket,
        'ssosavestate':ssosavestate,
        'callback':'sinaSSOController.doCrossDomainCallBack',
        'scriptId':'ssoscript0',
        'client':'ssologin.js(v1.4.19)',
        '_':get_timestamp(),
    }
    headers = {
        "Referer": "https://login.sina.com.cn/",
        'Host': 'passport.weibo.com',
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
    }
    res = session.get(url=pwd_url,params=params,headers=headers)
    res.encoding = res.apparent_encoding
    
    jres = json.loads(res.text.replace('sinaSSOController.doCrossDomainCallBack(','').replace(');',''))
    print(jres)
    if jres.get('result'):
        print("登录成功，欢迎您: "+ jres['userinfo']['displayname'])
    
    # 个人主页测试
    # test_url = 'https://account.weibo.com/set/index?topnav=1&wvr=6'
    # response = session.get(test_url,headers=ua_headers)
    # response.encoding = response.apparent_encoding
    # print(response.text)
    

def main():
    su = get_su(ACCOUNT)
    me = prelogin(su)
    sp = get_sp(me,PASSWORD)
    login(su,sp,me)

if __name__ == '__main__':
    main()

    
    