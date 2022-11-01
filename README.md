# Smart-Mixin
## 一个开源的Clash配置预处理器。
## Tips
### 过滤节点
```Python
select_all(CONF.Proxies, False, re_name = "官网").delete()
```
从代理列表和全部代理组中删除正则匹配到名称的节点，相当于过滤节点。
## Change Log
### 2.0.4
实例化 `Config` 的方式迎来改变：原 `url` 参数名称变为 `Url`；不再可用 `path` 初始化， `File` 取而代之（文件对象），解决了编码导致读取错误的问题。  
我们引入了模板！这是一种快捷创建你想要的配置文件的方式，将来模板还会进行扩充。
在 `Readme` 中加入了使用提示。
### 2.0.3
修复了 `ProxyGroup` 初始化时 `DICT` 中代理不能为代理类型的问题；本次修复有几率带来其他潜在问题。
### 2.0.2
修复了 `Proxy` 重命名原名称与新名称相同时出现死循环的情况；  
修复了 `ProxyGroup` 重命名导致配置文件解析错误的问题。
### 2.0.1
加入了 `Mixin` 功能；  
`ReadMe` 小改。
### 2.0.0
更加面向对象，语法更加简洁，交互更为友好，新版本2.0.0已经正式发布；请前往[Release](https://github.com/hexin-lin-1024/Smart-Mixin/releases/tag/2.0.0)体验。  
在编写 `2.0.0` 的时候，程序经历了好几次重构；这些迭代都只为了一个目的，更简洁直观的操作。
## 安装外部依赖
`pip3 install requests pyyaml`
## 引入
```Python
from PreProcesser import *
```
## 加载配置文件
在 `2.x` 版本中，加载配置文件的方式更加多样化（这些方法等价，全给出时按照优先级 Url > YAML > File 加载）：
### 通过模板加载：(从 `2.0.4` 或更高版本)
模板可以以和 `Config` 无异的方法初始化：
```Python
from Templates.Nexitally import Nexitally
CONF = Nexitally(Url = "https://example.com/exp.yaml")
```
也可以通过提供代理列表来初始化：
```Python
from Templates.Nexitally import Nexitally
CONF_TMP = Config(Url = "https://example.com/exp.yaml")
CONF = Nexitally(Proxies = CONF_TMP.Proxies)
```
### 通过 `Url` 加载：(从 `2.0.4` 开始参数更名)
```Python
CONF = Config(Url = "https://example.com/exp.yaml")
```
 `2.0.3` 及以下版本：
```Python
CONF = Config(url = "https://example.com/exp.yaml")
```
### 通过 `YAML` 字符串加载：
```Python
CONF = Config(YAML = """此处省略""")
```
### 通过文件路径加载：（从 `2.0.4` 废除，不再可用）
```Python
CONF = Config(path = r"./exp.yaml")
```
### 通过文件对象加载：（ `2.0.4` 或更高版本）
```Python
CONF = Config(File=open(r"./exp.yaml", encoding="utf-8"))
```
## 新建
在 `2.x` 版本中，新建代理、代理组、规则的语法都发生了改变：
### 新建代理
```Python
Shadowsocks = Proxy(DICT={'name': '🇨🇳 Shadowsocks', 'type': 'ss', 'server': '127.0.0.1', 'port': '12345', 'cipher': 'chacha20-ietf-poly1305', 'udp': True, 'password': 'PassWD', 'plugin': 'obfs', 'plugin-opts': {'host': '6d1af65d074041a0.swcdn.apple.com', 'mode': 'http'}})
```
另一种等价写法：
```Python
Shadowsocks = Proxy(YAML="""
- cipher: chacha20-ietf-poly1305
  name: "\U0001F1E8\U0001F1F3 Shadowsocks"
  password: PassWD
  plugin: obfs
  plugin-opts:
    host: 6d1af65d074041a0.swcdn.apple.com
    mode: http
  port: '12345'
  server: 127.0.0.1
  type: ss
  udp: true
""")
```
### 新建代理组
这里有好几种等价方法：
```Python
No = ProxyGroup(DICT={'name': 'No', 'url': 'https://cp.cloudflare.com/generate_204', 'type': 'select', 'proxies': [Shadowsocks, Trojan]})
```
```Python
No = ProxyGroup(YAML="""
- name: No
  proxies:
  - "\U0001F1E8\U0001F1F3 Shadowsocks"
  - "\U0001F1E8\U0001F1F3 Trojan"
  type: select
  url: https://cp.cloudflare.com/generate_204
""")
```
```Python
No = ProxyGroup(DICT={'name': 'No', 'url': 'https://cp.cloudflare.com/generate_204', 'type': 'select', 'proxies': []})
No.proxies = [Shadowsocks, Trojan] #书接上文
```
### 新建规则
此二种方法等价：
```Python
R = Rule("DOMAIN-SUFFIX", "Apple.com", "\U0001F34E Apple")
```
```Python
R = Rule(YAML="DOMAIN-SUFFIX,Apple.com,\U0001F34E Apple")
```
## 绑定与修改
### 绑定
在2.0的前几次迭代中，笔者曾打算为对象加上绑定函数，让用户自行绑定，但是这无疑违背了简洁方便的原则。故笔者用继承实现了自动绑定，当对象通过任何方式添加时，它们将自动被绑定。
### 属性
可以直接给对象特定属性赋值来修改，此表格为可用(其他属性不建议操作)属性：  
Config 相关属性不建议直接修改  
|对象类型|对象属性|接受的值|
|---|---|---
|`Config`|`DICT`|字典
|`Config`|`YAML`|字符串<sup>1</sup>
|`Config`|`Proxies`|全部代理的列表
|`Config`|`ProxyGroups`|代理组的列表
|`Config`|`Rules`|规则列表
|`Proxy`|`name`|名称(字符串)<sup>2</sup>
|`ProxyGroup`|`DICT`|字典
|`ProxyGroup`|`name`|名称(字符串)<sup>2</sup>
|`ProxyGroup`|`proxies`|包含的代理 `[<Proxy object>]`
|`Rule`<sup>3</sup>|`YAML`|字符串
|`Rule`|`type`|字符串
|`Rule`|`matchedTraffic`|字符串
|`Rule`|`strategy`|字符串|

注解：  
1.相当于重新加载配置文件  
2.改动会引起全局的名称修改  
3.约定一个 `Rule` 的 `YAML` 组成如下 `type, matchedTraffic, strategy`  
框架也提供了两个函数方便用户修改：
```Python
pop_front(obj, item)
```
```Python
pop_back(obj, item)
```
这些函数的作用为加指定的对象(item)加入可迭代对象(obj)的头部或尾部。  
当然也可以直接使用内置函数操作，这里展示两种等价的方法。
```Python
pop_back(CONF.Proxies, Shadowsocks)
```
通过内置函数操作：
```Python
CONF.Proxies.append(Shadowsocks)
```
### 可用成员函数
|对象类型|函数名称|函数作用|接受的参数|返回值|
|---|---|---|---|---
|`Config`|`getProxies`|获取所有代理|`groups = False`<sup>1</sup>, `embedded = False`<sup>2</sup>|`[<object Proxy>]`
|`Config`|`mixin`|追加配置|`YAML` (字符串) 或者 `DICT` (字典)|无返回值
|`Proxy`|`delete`|删除自身<sup>4</sup>|不接受参数|无返回值
|`ProxyGroup`|`delete`|删除自身<sup>5</sup>|`strategy = None`<sup>6</sup>|无返回值|

注解：  
1.包含代理组  
2.包含 `DIRECT` / `REJECT` 等内置代理   
3.类似于 `Clash For Windows` 的 `Mixin` ，可以起到覆盖已有配置的作用  
4.如果该代理位于 `Config.Proxy` 中，将会从所有代理组中删除  
5.也会从其他 `ProxyGroup` 中删除自身  
6.默认为删除所有相关规则，若提供 `strategy` 代表将所有相关规则的目的地改写为该值
## 筛选
框架提供了两个辅助筛选的函数
```Python
select(obj, reverse=False, **kwargs)
#示例
select(CONF.Proxies, reverse=False, name="Japan 16")
```
```Python
select_all(obj, reverse=False, **kwargs)
#示例
select_all(CONF.Proxies, reverse=False, re_name="Japan")
```
`select` 和 `select_all` 函数的语法一致， `obj` 表示要从中查找的可迭代对象， `reverse` 是否反向选择，后面是对象的任意属性（查找规则），由 `re_` 前缀开头时，以正则表达式方式查找。  
在有多个符合条件的对象时， `select` 函数返回有最小索引值的一个；  
`select_all` 函数返回一个 `SELECT_ALL` 对象(继承自列表)，包含全部符合条件的对象，且有一个特殊语法：
```Python
select_all(CONF.Proxies, reverse=False, re_name="Japan").delete()
```
等价于
```Python
r = select_all(CONF.Proxies, reverse=False, re_name="Japan")
for i in r:
  i.delete()
```
## 框架使用例
```Python
CONF = Config(url=r"https://example.com/example.yaml")
aa = [
    'DOMAIN-SUFFIX,example.com,aa',
    'DOMAIN-SUFFIX,example.net,aa'
]
for i in aa:
    pop_front(c.Rules, Rule(YAML=i))
select_all(c.getProxies(), False, re_name="Premium").delete()
select(c.getProxies(), False, re_name=" | ").delete()
select(c.getProxies(), False, re_name="Traffic Reset").delete()
select(c.getProxies(), False, re_name="Expire Date").delete()
aa = ProxyGroup(DICT={'name': 'aa', 'url': 'https://cp.cloudflare.com/generate_204', 'type': 'select', 'proxies': []})
Shadowsocks = Proxy(DICT={'name': '🇨🇳 Shadowsocks', 'type': 'ss', 'server': 's.example.com', 'port': '12345', 'cipher': 'chacha20-ietf-poly1305', 'udp': True, 'password': 'PassWD', 'plugin': 'obfs', 'plugin-opts': {'host': '6d1af65d074041a0.swcdn.apple.com', 'mode': 'http'}})
Trojan = Proxy(DICT={'name': '🇨🇳 Trojan', 'type': 'trojan', 'server': 't.example.com', 'port': '54321', 'udp': True, 'password': 'PassWD', 'skip-cert-verify': True, 'sni': 't.example.com'})
aa.proxies = [Shadowsocks, Trojan]
pop_back(c.Proxies, Shadowsocks)
pop_back(c.Proxies, Trojan)
pop_back(c.ProxyGroups, aa)
select_all(c.Rules, False, strategy="REJECT").delete()
select(c.ProxyGroups, False, name="Hijacking").delete(strategy="REJECT")
select(c.ProxyGroups, False, name="\U0001F3AC myTVSUPER").delete()
select(c.ProxyGroups, False, name="\U0001F3AC Emby").delete()
select(c.ProxyGroups, False, name="\U0001F4F2 LineTV").delete()
select(c.ProxyGroups, False, name="\U0001F3AC iQiyi").delete()
select(c.ProxyGroups, False, name="\U0001F4DF Twitter").delete()
select(c.ProxyGroups, False, name="\U0001F4FA Disney").delete()
select(c.ProxyGroups, False, name="\U0001F4FA Netflix").delete()
select(c.ProxyGroups, False, name="\U0001F3B5 Tiktok").delete()
select(c.ProxyGroups, False, name="\U0001F310 Google").delete()
with open("RES.yaml", "w") as f:
    f.write(c.YAML)
```
