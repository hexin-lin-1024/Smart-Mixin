import requests
import yaml
import re
import inspect


class SELECT_ALL(list):
    def __init__(self, li):
        list.__init__([])
        super().extend(li)
        built_in = ['__module__', '__init__', '__dict__', '__weakref__', '__doc__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__',
                    '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']

        def call_func(**kwargs):
            func_name = inspect.stack()[1][4][0]
            func_name = func_name[func_name.rfind("select_all"):]
            func_name = func_name[func_name.find(").") + 2:]
            func_name = func_name[:func_name.find("(")]
            for i in self:
                i.__getattribute__(func_name)(**kwargs)

        for i in li[0].__dir__():
            if hasattr(li[0].__getattribute__(i), '__call__') and i not in built_in:
                self.__setattr__(i, call_func)


class ConfigProxies(list):
    def __init__(self, proxy_groups_list, __iterable=None):
        list.__init__([])
        self.proxy_groups_list_getitem = proxy_groups_list.__getitem__
        self.proxy_groups_list_len = proxy_groups_list.__len__
        if not __iterable == None:
            for i in __iterable:
                i.proxies_list_remove = self.remove
                i.proxy_groups_list_getitem = self.proxy_groups_list_getitem
                i.proxy_groups_list_len = self.proxy_groups_list_len
            super().extend(__iterable)

    def append(self, __object):
        __object.proxies_list_remove = self.remove
        __object.proxy_groups_list_getitem = self.proxy_groups_list_getitem
        __object.proxy_groups_list_len = self.proxy_groups_list_len
        return super().append(__object)

    def insert(self, __index, __object):
        __object.proxies_list_remove = self.remove
        __object.proxy_groups_list_getitem = self.proxy_groups_list_getitem
        __object.proxy_groups_list_len = self.proxy_groups_list_len
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            i.proxies_list_remove = self.remove
            i.proxy_groups_list_getitem = self.proxy_groups_list_getitem
            i.proxy_groups_list_len = self.proxy_groups_list_len
        return super().extend(__iterable)


class ConfigProxyGroups(list):
    def __init__(self, rules_list, __iterable=None):
        list.__init__([])
        self.rules_list_getitem = rules_list.__getitem__
        self.rules_list_len = rules_list.__len__
        if not __iterable == None:
            for i in __iterable:
                i.proxy_groups_list_remove = self.remove
                i.proxy_groups_list_getitem = self.__getitem__
                i.proxy_groups_list_len = self.__len__
                i.rules_list_getitem = self.rules_list_getitem
                i.rules_list_len = self.rules_list_len
            super().extend(__iterable)

    def append(self, __object):
        __object.proxy_groups_list_remove = self.remove
        __object.proxy_groups_list_getitem = self.__getitem__
        __object.proxy_groups_list_len = self.__len__
        __object.rules_list_getitem = self.rules_list_getitem
        __object.rules_list_len = self.rules_list_len
        return super().append(__object)

    def insert(self, __index, __object):
        __object.proxy_groups_list_remove = self.remove
        __object.proxy_groups_list_getitem = self.__getitem__
        __object.proxy_groups_list_len = self.__len__
        __object.rules_list_getitem = self.rules_list_getitem
        __object.rules_list_len = self.rules_list_len
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            i.proxy_groups_list_remove = self.remove
            i.proxy_groups_list_getitem = self.__getitem__
            i.proxy_groups_list_len = self.__len__
            i.rules_list_getitem = self.rules_list_getitem
            i.rules_list_len = self.rules_list_len
        return super().extend(__iterable)


class ConfigRules(list):
    def __init__(self, __iterable=None):
        list.__init__([])
        if not __iterable == None:
            for i in __iterable:
                i.rules_list_remove = self.remove
            super().extend(__iterable)

    def append(self, __object):
        __object.rules_list_remove = self.remove
        return super().append(__object)

    def insert(self, __index, __object):
        __object.rules_list_remove = self.remove
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            i.rules_list_remove = self.remove
        return super().extend(__iterable)


class ProxyGroupProxies(list):
    def __init__(self, __iterable=None):
        list.__init__([])
        if not __iterable == None:
            for i in __iterable:
                i.proxies_list_remove = self.remove
                i.proxy_groups_list_getitem = None
                i.proxy_groups_list_len = None
            super().extend(__iterable)

    def append(self, __object):
        __object.proxies_list_remove = self.remove
        __object.proxy_groups_list_getitem = None
        __object.proxy_groups_list_len = None
        return super().append(__object)

    def insert(self, __index, __object):
        __object.proxies_list_remove = self.remove
        __object.proxy_groups_list_getitem = None
        __object.proxy_groups_list_len = None
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            i.proxies_list_remove = self.remove
            i.proxy_groups_list_getitem = None
            i.proxy_groups_list_len = None
        return super().extend(__iterable)


def select_all(obj, reverse=False, **kwargs):
    result = []
    for i in obj:
        tmp = True
        for j in kwargs.keys():
            if j.startswith("re_"):
                if not re.search(kwargs[j], getattr(i, j[3:])):
                    tmp = False
                    break
            else:
                if not kwargs[j] == getattr(i, j):
                    tmp = False
                    break
        if tmp and not reverse:
            result.append(i)
        elif not tmp and reverse:
            result.append(i)
    return SELECT_ALL(result)


def select(obj, reverse=False, **kwargs):
    for i in obj:
        tmp = True
        for j in kwargs.keys():
            if j.startswith("re_"):
                if not re.search(kwargs[j], getattr(i, j[3:])):
                    tmp = False
                    break
            else:
                if not kwargs[j] == getattr(i, j):
                    tmp = False
                    break
        if tmp and not reverse:
            return i
        elif not tmp and reverse:
            return i
    return None


def pop_front(obj, item):
    obj.insert(0, item)


def pop_back(obj, item):
    obj.append(item)


class Proxy:
    def __init__(self, DICT=None, YAML=None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)[0]
        else:
            raise ValueError

    @property
    def name(self):
        return self.DICT["name"]

    @name.setter
    def name(self, name):
        self.DICT["name"] = name

    def delete(self):
        if self.proxy_groups_list_len:
            for i in range(self.proxy_groups_list_len() - 1, -1, -1):
                for j in self.proxy_groups_list_getitem(i).proxies:
                    if j.name == self.name:
                        j.delete()
        if self.proxies_list_remove:
            self.proxies_list_remove(self)


class Config():
    def __init__(self, url=None, YAML=None, path=None):
        self._Rules = ConfigRules()
        self._ProxyGroups = ConfigProxyGroups(self.Rules)
        self._Proxies = ConfigProxies(self.ProxyGroups)
        self._DICT = {}

        if url:
            res = requests.get(url)
            try:
                self.sub_info = {
                    "subscription-userinfo": res.headers["subscription-userinfo"]}
            except:
                pass
            self.YAML = res.text
        elif YAML:
            self.YAML = YAML
        elif path:
            self.YAML = "\n".join(open(path, "r").readlines())
        else:
            raise ValueError

    @property
    def Proxies(self):
        return self._Proxies

    @Proxies.setter
    def Proxies(self, Proxies):
        self._Proxies = ConfigProxies(self.ProxyGroups, Proxies)

    @property
    def ProxyGroups(self):
        return self._ProxyGroups

    @ProxyGroups.setter
    def ProxyGroups(self, ProxyGroups):
        self._ProxyGroups = ConfigProxyGroups(self.Rules, ProxyGroups)

    @property
    def Rules(self):
        return self._Rules

    @Rules.setter
    def Rules(self, Rules):
        self._Rules = ConfigRules(Rules)

    def getProxies(self, groups=False, embedded=False):
        # 这里的绑定需要考虑
        result = self.Proxies
        if groups:
            result += [Proxy(DICT={"name": i.name}, proxies_list=result)
                       for i in self.ProxyGroups]
        if embedded:
            result += [Proxy(DICT={"name": "DIRECT"}, proxies_list=result),
                       Proxy(DICT={"name": "REJECT"}, proxies_list=result)]
        return result

    def mixin(self, YAML=None, DICT=None):
        raise RuntimeError("To Do")
        if DICT:
            pass
        elif YAML:
            tmp = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        else:
            raise ValueError

    @property
    def DICT(self):
        self._DICT["proxies"] = [i.DICT for i in self.Proxies]
        self._DICT["proxy-groups"] = [i.DICT for i in self.ProxyGroups]
        self._DICT["rules"] = [i.YAML for i in self.Rules]
        return self._DICT

    @DICT.setter
    def DICT(self, DICT):
        self._DICT = DICT
        for i in self._DICT["proxy-groups"]:
            self.ProxyGroups.append(ProxyGroup(DICT=i))
        for i in self._DICT["proxies"]:
            self.Proxies.append(
                Proxy(DICT=i))
        for i in self._DICT["rules"]:
            self.Rules.append(Rule(YAML=i, config=self))

    @property
    def YAML(self):
        return yaml.dump(self.DICT)

    @YAML.setter
    def YAML(self, YAML):
        self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)


class ProxyGroup():
    def __init__(self, DICT=None, YAML=None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        else:
            raise ValueError

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, proxies):
        self._proxies = ProxyGroupProxies(proxies)

    @property
    def DICT(self):
        self._DICT["proxies"] = [i.name for i in self._proxies]
        return self._DICT

    @DICT.setter
    def DICT(self, DICT):
        self._DICT = DICT
        self.proxies = [Proxy(DICT={"name": i}) for i in self._DICT["proxies"]]

    @property
    def name(self):
        return self._DICT["name"]

    @name.setter
    def name(self, name):
        self._DICT["name"] = name

    def delete(self, strategy=None):
        if strategy == None:
            if self.rules_list_len:
                for i in range(self.rules_list_len() - 1, -1, -1):
                    if self.rules_list_getitem(i).strategy == self.name:
                        self.rules_list_getitem(i).delete()
        else:
            if self.rules_list_len:
                for i in range(0, self.rules_list_len()):
                    if self.rules_list_getitem(i).strategy == self.name:
                        self.rules_list_getitem(i).strategy = strategy

        if self.proxy_groups_list_remove:
            self.proxy_groups_list_remove(self)

        if self.proxy_groups_list_len:
            for i in range(self.proxy_groups_list_len() - 1, -1, -1):
                tmp = select(self.proxy_groups_list_getitem(
                    i).proxies, False, name=self.name)
                if tmp:
                    tmp.delete()


class Rule():
    def __init__(self, type=None, matchedTraffic=None, strategy=None, YAML=None):
        if (type == None or matchedTraffic == None or strategy == None) and YAML == None:
            raise ValueError
        elif YAML == None:
            self.type = type
            self.matchedTraffic = matchedTraffic
            self.strategy = strategy
        else:
            self.YAML = YAML

    @property
    def YAML(self):
        if not self.type == None:
            return self.type + "," + self.matchedTraffic + "," + self.strategy
        else:
            return self.matchedTraffic + "," + self.strategy

    @YAML.setter
    def YAML(self, YAML):
        tmp = YAML.split(",")
        if len(tmp) == 3:
            self.type = tmp[0]
            self.matchedTraffic = tmp[1]
            self.strategy = tmp[2]
        else:
            self.type = None
            self.matchedTraffic = tmp[0]
            self.strategy = tmp[1]

    def delete(self):
        if self.rules_list_remove:
            self.rules_list_remove(self)
