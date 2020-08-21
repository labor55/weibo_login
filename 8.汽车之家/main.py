import requests
import re
from fontTools.ttLib import TTFont
from lxml import etree
import io

class Crawl:
    def __init__(self):
        self.session = requests.session()
        
    def get_html(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        try:
            res = self.session.get(url,headers=headers)
            if res.status_code == 200:
                return res
        except Exception as e:
            print('抓取失败',e)
            return
    

    def codeShapeMap(self,font):
        base_font = TTFont('base_font.woff')
        # baseCNMap = base_font.getBestCmap()  # 获取code和name的关系
        baseCNMap = base_font.getGlyphOrder()[1:]
        baseGlyf = base_font['glyf'] # 模板形状 # 拿到code
        baseFontMap = [  #  拿到字体
            '上','地','矮','得','九','八','二','很','是','远',
            '四','短','低','下','呢','坏','的','多','少','七',
            '左','大','小','近','右','高','三','十','不','六',
            '了','五','和','长','着','一','好','更',
        ]
        base_shape = []
        base_name = []
        for name in baseCNMap:
            base_shape.append(baseGlyf[name].flags)
            base_name.append(name)
            
        codeNameMap = font.getBestCmap()  # 获取code和name的关系
        glyf = font['glyf']  # 取出形状
        new_shape = {}
        for name in codeNameMap.values():
            new_shape[name] = glyf[name].flags
        
        map_dict = {}
        for i, base_shape in enumerate(base_shape):
            for name, shape in new_shape.items():
                if base_shape == shape:
                    name_lower = eval(r'u"\u' + name.replace('uni','') + '"').lower()
                    map_dict[name_lower] = baseFontMap[i]
                    # print(i,name,baseFontMap[i],base_name[i])
        return map_dict

    
    def main(self,url):
        res = self.get_html(url)
        if res:
            html_str = etree.HTML(res.text)
            con = html_str.xpath('//div[@class="w740"]/div[@class]')[0].xpath('string(.)').strip().replace('\t','')
            font_url_str = html_str.xpath('//head/style[1]/text()')
            font_url = re.search(r",url\('(.*?)'\) format\('woff'\)",font_url_str[0],re.S).group(1)
            font_url = "http:" + font_url if font_url else None
            # print(con)
            if font_url:
                font_con = self.get_html(font_url)
                # new_woff = 'new2_font.woff'
                # with open(new_woff, 'wb') as fp:
                #     fp.write(font_con.content)
                # font = TTFont(new_woff)
                # font.saveXML('new_font.xml')
                font = TTFont(io.BytesIO(font_con.content))
                map_dict = self.codeShapeMap(font)
                print(map_dict)
                for key in map_dict.keys():
                    con = con.replace(key,map_dict[key])
                print(con)

if __name__ == "__main__":
    # url = 'https://club.autohome.com.cn/bbs/thread/bd9ebd6673f4d960/87284151-1.html#pvareaid=6830286'
    url = 'https://club.autohome.com.cn/bbs/thread/a520185a1b14b0cb/87284113-1.html#pvareaid=6830286'
    # url = 'https://club.autohome.com.cn/bbs/thread/31673d87224166a5/87311887-1.html#pvareaid=6830286'
    c = Crawl()
    c.main(url)