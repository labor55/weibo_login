import requests
import hashlib,time,random

class YouDaoFY():
    def __init__(self,keyword):
        self.keyword = keyword

    def md5(self,string):
        '''生成MD5加密字符串'''
        # 创建md5对象
        md5_res = hashlib.md5()
        # 此处必须声明encode
        md5_res.update(string.encode(encoding='utf-8'))
        return md5_res.hexdigest()

    def get_timestamp(self):
        '''出口参数:生成13位整数时间戳'''
        timestamp = int(round(time.time()*1000))
        return timestamp

    def start(self):
        headers = {
            'user-agent':'mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/83.0.4103.97 safari/537.36',
            "cookie":"OUTFOX_SEARCH_USER_ID=569873245@10.169.0.102; JSESSIONId=aAAEAB7guS7W47PWLk8kx; OUTFOX_SEARCH_USER_ID_NCOO=921859326.0235113;",
            "host":"fanyi.youdao.com",
            "origin":"http://fanyi.youdao.com",
            "pragma":"no-cache",
            "referer":"http://fanyi.youdao.com/",
            "X-requested-with":"XMlhtTprequest",
            "content-type":"application/x-www-form-urlencoded; charseT=UTF-8",
        }
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        ts = self.get_timestamp()
        salt =  str(ts) + str(random.randint(0,9))
        sign = self.md5("fanyideskweb" + self.keyword + salt + "mmbP%A-r6U3Nw(n]BjuEU")
        data = {
            "i":self.keyword,
            "from":"AUTO",
            "to":"AUTO",
            "smartresult":"dict",
            "client":"fanyideskweb",
            "salt":salt,
            "sign":sign,
            "ts":ts,
            "bv":"a56dd011b8d23f96cdaae20178ff02ec",
            "doctype":"json",
            "version":"2.1",
            "keyfrom":"fanyi.web",
            "action":"FY_BY_REAlTLME",
        }

        resp = requests.post(url,data=data,headers=headers).json()
        res = resp.get('translateResult')[0][0].get('tgt')
        print(res)

if __name__ == "__main__":
    i = YouDaoFY("hello")
    i.start()