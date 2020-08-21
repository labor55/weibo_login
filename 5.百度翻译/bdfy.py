import requests
import execjs,re

class BaiDuFy():
    def __init__(self,keyword):
        self.keyword = keyword
        
    def get_sign(self,string):
        with open('bdfy.js','r') as f:
            js_code = f.read()
        res = execjs.compile(js_code).call("get_res",string)
        return res

    # 未使用，需求只有英中
    def detect_lang(self,string):
        url = 'https://fanyi.baidu.com/langdetect'
        data = {
            'query': string,
        }
        headers = {
            'user-agent':'mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/83.0.4103.97 safari/537.36'
        }
        res = requests.post(url,data=data,headers=headers).json()
        if res.get('error') == 0:
            return res.get('lan')
        return

    def start(self):
        sign = self.get_sign(self.keyword)
        url = 'https://fanyi.baidu.com/v2transapi'
        # 检测中文是否存在
        patten =  "[\u4e00-\u9fa5]"
        result = re.findall(patten,self.keyword)
        # 不存在  英--> 中
        if result:
            params = {
                'from':'zh',
                'to':'en'
            }
        # 输入存在中文 中---> 英
        else:
            params = {
                'from':'en',
                'to':'zh'
            }
        temp_data = {
            "query":self.keyword,
            "transtype":"translang",
            "simple_means_flag":"3",
            "sign":sign,
            "token":"c2edebbbeeee95ae8d95944d251f65a5",
            "domain":"common",
        }
        data = dict(temp_data,**params)
        headers = {
            "content-type":"application/x-www-form-urlencoded; charseT=UTF-8",
            "origin":"https://fanyi.baidu.com",
            "pragma":"no-cache",
            "referer":"https://fanyi.baidu.com/",
            "user-agent":"mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/83.0.4103.97 safari/537.36",
            "x-requested-with":"XMlhtTprequest",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"same-origin",
            'cookie': 'BAIDUID=F8F9094160A546E5B6FB6006DACBCDC5:FG=1'
        }
        
        resp = requests.post(url,data=data,params=params,headers=headers).json()
        res = resp.get('trans_result').get('data')[0].get('dst')
        print(res)

if __name__ == "__main__":
    keyword = input('请输入你要翻译的文本:\n')
    i = BaiDuFy(keyword)
    i.start()
    

