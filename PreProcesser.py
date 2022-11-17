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


class LIST(list):
    def __init__(self, bind=None, bind_attrs={}, attrs={}, __iterable=None):
        list.__init__([])
        if not bind == None:
            for i in bind_attrs.keys():
                self.__setattr__(i, bind.__getattribute__(bind_attrs[i]))
        self.attrs = attrs
        if not __iterable == None:
            for i in __iterable:
                for j in self.attrs.keys():
                    i.__setattr__(j, self.__getattribute__(self.attrs[j]))
            super().extend(__iterable)

    def append(self, __object):
        for j in self.attrs.keys():
            __object.__setattr__(j, self.__getattribute__(self.attrs[j]))
        return super().append(__object)

    def insert(self, __index, __object):
        for j in self.attrs.keys():
            __object.__setattr__(j, self.__getattribute__(self.attrs[j]))
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            for j in self.attrs.keys():
                i.__setattr__(j, self.__getattribute__(self.attrs[j]))
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
        foregone = self.DICT["name"]
        if not foregone == name:
            self.DICT["name"] = name
            for i in range(self.proxy_groups_list_len() - 1, -1, -1):
                for j in self.proxy_groups_list_getitem(i).proxies:
                    if j.name == foregone:
                        j.name = name

    def delete(self):
        if self.proxies_list_remove:
            self.proxies_list_remove(self)
        if self.proxy_groups_list_len:
            for i in range(self.proxy_groups_list_len() - 1, -1, -1):
                for j in self.proxy_groups_list_getitem(i).proxies:
                    if j.name == self.name:
                        j.delete()


class Config():
    def __init__(self, Url=None, YAML=None, File=None):
        self._Rules = LIST(attrs={"rules_list_remove": "remove"})
        self._ProxyGroups = LIST(self.Rules,
                                 {"rules_list_getitem": "__getitem__",
                                  "rules_list_len": "__len__"},
                                 {"proxy_groups_list_remove": "remove",
                                  "proxy_groups_list_getitem": "__getitem__",
                                  "proxy_groups_list_len": "__len__",
                                  "rules_list_getitem": "rules_list_getitem",
                                  "rules_list_len": "rules_list_len"})
        self._Proxies = LIST(self.ProxyGroups,
                             {"proxy_groups_list_getitem": "__getitem__",
                              "proxy_groups_list_len": "__len__"},
                             {"proxies_list_remove": "remove",
                              "proxy_groups_list_getitem": "proxy_groups_list_getitem",
                              "proxy_groups_list_len": "proxy_groups_list_len"})
        self._DICT = {}

        if Url:
            res = requests.get(Url)
            try:
                self.sub_info = {
                    "subscription-userinfo": res.headers["subscription-userinfo"]}
            except:
                pass
            self.YAML = res.text
        elif YAML:
            self.YAML = YAML
        elif File:
            self.YAML = File.read()
        else:
            raise ValueError

    @property
    def Proxies(self):
        return self._Proxies

    @Proxies.setter
    def Proxies(self, Proxies):
        self._Proxies = LIST(self.ProxyGroups,
                             {"proxy_groups_list_getitem": "__getitem__",
                              "proxy_groups_list_len": "__len__"},
                             {"proxies_list_remove": "remove",
                              "proxy_groups_list_getitem": "proxy_groups_list_getitem",
                              "proxy_groups_list_len": "proxy_groups_list_len"},
                             Proxies)

    @property
    def ProxyGroups(self):
        return self._ProxyGroups

    @ProxyGroups.setter
    def ProxyGroups(self, ProxyGroups):
        self._ProxyGroups = LIST(self.Rules,
                                 {"rules_list_getitem": "__getitem__",
                                  "rules_list_len": "__len__"},
                                 {"proxy_groups_list_remove": "remove",
                                  "proxy_groups_list_getitem": "__getitem__",
                                  "proxy_groups_list_len": "__len__",
                                  "rules_list_getitem": "rules_list_getitem",
                                  "rules_list_len": "rules_list_len"},
                                 ProxyGroups)

    @property
    def Rules(self):
        return self._Rules

    @Rules.setter
    def Rules(self, Rules):
        self._Rules = LIST(attrs={"rules_list_remove": "remove"}, __iterable=Rules)

    def getProxies(self, groups=False, embedded=False):
        result = self.Proxies
        if groups:
            result += [Proxy(DICT={"name": i.name})
                       for i in self.ProxyGroups]
        if embedded:
            result += [Proxy(DICT={"name": "DIRECT"}),
                       Proxy(DICT={"name": "REJECT"})]
        return result

    def mixin(self, YAML=None, DICT=None):
        if DICT:
            YAML = yaml.dump(self.DICT)
        elif YAML:
            pass
        else:
            raise ValueError
        self.YAML = self.YAML + "\n" + YAML

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
            for j in self.ProxyGroups[len(self.ProxyGroups) - 1].proxies:
                j.proxy_groups_list_getitem = self.ProxyGroups.__getitem__
                j.proxy_groups_list_len = self.ProxyGroups.__len__

        for i in self._DICT["proxies"]:
            self.Proxies.append(
                Proxy(DICT=i))
        for i in self._DICT["rules"]:
            self.Rules.append(Rule(YAML=i))

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
        self._proxies = LIST([],
                             {"proxy_groups_list_getitem": "__getitem__",
                              "proxy_groups_list_len": "__len__"},
                             {"proxies_list_remove": "remove",
                              "proxy_groups_list_getitem": "proxy_groups_list_getitem",
                              "proxy_groups_list_len": "proxy_groups_list_len"},
                             proxies)

    @property
    def DICT(self):
        self._DICT["proxies"] = [i.name for i in self._proxies]
        return self._DICT

    @DICT.setter
    def DICT(self, DICT):
        self._DICT = DICT
        self.proxies = [Proxy(DICT={"name": i.name}) if isinstance(
            i, Proxy) else Proxy(DICT={"name": i}) for i in self._DICT["proxies"]]

    @property
    def name(self):
        return self._DICT["name"]

    @name.setter
    def name(self, name):
        foregone = self._DICT["name"]
        if not foregone == name:
            self._DICT["name"] = name
            for i in range(self.proxy_groups_list_len() - 1, -1, -1):
                for j in self.proxy_groups_list_getitem(i).proxies:
                    if j.name == foregone:
                        j.name = name

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
