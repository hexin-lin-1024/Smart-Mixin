# ClashYamlPreProcesser  

## 一个开源的Clash YAML 配置预处理器。  

这里是文档。  

  
依赖
|---
|requests
|Pyyaml（在部分情况下已经预包含在标准环境中）
|Python3|
  

### 约定  
一条规则由三个部分组成，如`- DOMAIN-SUFFIX,onenote.com,\U0001F5A5 Microsoft`，我们约定其格式表示为`- type, content, policy`。若使用列表表示时，我们约定多条规则以`['type, content, policy', 'type, content, policy', 'type, content, policy', etc]`的形式表示。  

使用`from PreProcesser import *`导入模块，并通过`Clash(订阅URL)`实例化。  
Clash 类包含数个成员函数以实现修改配置文件的功能。  

  
|函数名称|作用|参数|
|---|---|---
|del_proxy_group|删除代理组（并替换为某个策略）|name（代理组的名称）, policy=None（不携带此参数代表直接删除所有相关规则，若参数不为None时改写原来所有相关规则的策略）
|append_proxy_group|追加新的代理组|dict（从YAML编码的字典）
|insert_proxy_group|从前端插入新的代理组|dict（从YAML编码的字典）
|proxy_filter|代理筛选器（筛选符合正则表达式的代理名称列表）|pattern（正则表达式）, mode（字符串，可以是select或者reverse_select，代表选择符合正则表达式的代理或者反选）, proxies=None（不携带此参数代表从所有代理中筛选，否则为一个包含代理名称字符串的列表，程序将从中筛选）
|insert_rules|从前端插入规则|type=None, content=None, policy=None, list=None（list代表多条规则）；必须同时给出type, content, policy三个参数或者给出list参数
|del_rules|删除规则|type=None, content=None, policy=None（删除所有匹配的规则）；三个参数中至少给出一个
|modify_proxy_group|修改代理组|name=None（原来的代理组名称）, proxies=None（修改为列表包含的代理）, new_name=None（新的名称）；name参数必须给出，proxies和new_name参数中至少给出一个
|dump|输出YAML为字符串|不接受参数|
  

## 使用例：  
```Python
url = '' #订阅URL

def clash(url):
    c = Clash(url)
    c.insert_rules(list=['DOMAIN-SUFFIX,xiaohuau.xyz,REJECT']) #从前端插入
    c.insert_rules(type='IP-CIDR', content='39.107.15.115/32', policy='REJECT')
    c.append_proxy({'name': 'Shadowsocks', 'type': 'ss', 'server': 'server.com', 'port': '12345', 'cipher': 'chacha20-ietf-poly1305',
                'udp': True, 'password': 'PassWD', 'plugin': 'obfs', 'plugin-opts': {'host': '6d1af65d074041a0.swcdn.apple.com', 'mode': 'http'}})
    c.insert_proxy_group({'name': 'ProxyGroup', 'url': 'https://cp.cloudflare.com/generate_204',
                           'type': 'select', 'proxies': ['Shadowsocks']})
    c.modify_proxy_group(name='\U0001F4F2 Telegram',proxies=c.proxy_filter('Singapore', 'select'))
    c.modify_proxy_group(name='Google', proxies=c.proxy_filter('San Jose', 'reverse_select', proxies = c.proxy_filter('US', 'select')), new_name='谷歌') #将原名称为Google的代理组重命名为谷歌并且将在所有代理中包含US字符串的，在此结果上二次筛选不包含San Jose的作为新的代理。
    c.del_rules(policy='REJECT') #删除所有REJECT的规则
    c.del_proxy_group('Hijacking', 'REJECT') #删除Hijacking代理组，并将所有相关规则改为REJECT
    c.del_proxy_group('\U0001F3AC myTVSUPER') #删除\U0001F3AC myTVSUPER代理组
    return c.dump()

print(clash(url)) #打印处理好的YAML字符串
```
  

## 与FastAPI结合  

```Python
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI
from PreProcesser import *
url = '' #订阅URL
app = FastAPI()
def clash(url):
    c = Clash(url)
    pass
    #在这里补充需要的代码
    return c.dump()
@app.get("/", response_class=PlainTextResponse)
async def process():
    return clash(url)
```
  
效果：访问FastAPI根目录时输出处理好的YAML（以纯文本网页形式）。
