import re
import json
import execjs
import requests

class ggfy():
    def __init__(self,):
        self.session = requests.Session()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
    
    def get_tk(self,pwd,ttk):
        with open('tk.js','r') as f:
            js_code = f.read()
        res = execjs.compile(js_code).call('get_tk',pwd,ttk)
        return res

    def get_ttk(self):
        
        url = 'https://translate.google.cn'

        res = self.session.get(url,headers=self.headers)

        ptn = r"tkk:'(.*?)',"
        ttk = re.findall(ptn,res.text)[0]
        return ttk
    
    def fanyi(self,keyword):
        ttk = self.get_ttk()
        tk = self.get_tk(keyword,ttk)
        url = 'https://translate.google.cn/translate_a/single'
        params = {
            "client": "webapp",
            "sl": "en",
            "tl": "zh-CN",
            "hl": "zh-CN",
            "dt": ["bd","at","ex","ld","md","qca","rw","rm","sos","ss","t"],
            "otf": "2",
            "ssel": "0",
            "tsel": "0",
            "xid": "45662847",
            "kc": "1",
            "tk": tk,
            "q": keyword,
        }
        han_str = re.findall('[\u4e00-\u9fa5]',keyword)
        if han_str:
            params['sl'] = 'zh-CN'
            params['tl'] = 'en'
        res = self.session.get(url=url,params=params,headers=self.headers)
        jres = json.loads(res.text)
        # 最优选 附音标
        print(jres[0][0][0],jres[0][1][-1])
        # 其它解释
        print(jres[1])
        
if __name__ == "__main__":
    f = ggfy()
    f.fanyi("开始")
