import requests
import yaml
import re


class plist(list):
    def __init__(self):
        list.__init__([])

    def append(self, __object):
        __object.bind(self)
        return super().append(__object)

    def insert(self, __index, __object):
        __object.bind(self)
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            i.bind(self)
        return super().extend(__iterable)

class pglist(list):
    def __init__(self):
        list.__init__([])

    def append(self, __object):
        __object.bind(self)
        return super().append(__object)

    def insert(self, __index, __object):
        __object.bind(self)
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            i.bind(self)
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
    return result


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
    def __init__(self, DICT=None, YAML=None, proxies_list=None, proxy_groups_list=None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)[0]
        else:
            raise ValueError

        def _bind(proxies_list=None, proxy_groups_list=None):
            if not proxies_list == None:
                self.proxies_list_remove = proxies_list.remove
            else:
                self.proxies_list_remove = None

            if not proxy_groups_list == None:
                self.proxy_groups_list_getitem = proxy_groups_list.__getitem__
                self.proxy_groups_list_len = proxy_groups_list.__len__
            else:
                self.proxy_groups_list_getitem = None
                self.proxy_groups_list_len = None
        self.__bind__ = _bind

        self.__bind__(proxies_list, proxy_groups_list)

    @property
    def name(self):
        return self.DICT["name"]

    @name.setter
    def name(self, name):
        self.DICT["name"] = name

    def bind(self, proxies_list, proxy_groups_list=None):
        self.__bind__(proxies_list, proxy_groups_list)

    def delete(self):
        if self.proxy_groups_list_len:
            tmp_length = self.proxy_groups_list_len()
            for i in range(0, self.proxy_groups_list_len()):
                if i >= tmp_length:
                    break
                for j in self.proxy_groups_list_getitem(i).proxies:
                    if j.name == self.name:
                        j.delete()
                tmp_length = self.proxy_groups_list_len()
        if self.proxies_list_remove:
            self.proxies_list_remove(self)


class Config():
    def __init__(self, url=None, YAML=None, path=None):
        self.Proxies = []
        self.ProxyGroups = []
        self.Rules = []
        # self._DICT = {}

        if url:
            res = requests.get(url)
            self.sub_info = {
                "subscription-userinfo": res.headers["subscription-userinfo"]}
            self.YAML = res.text
        elif YAML:
            self.YAML = YAML
        elif path:
            self.YAML = "\n".join(open(path, "r").readlines())
        else:
            raise ValueError

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

    def cover(self, YAML=None, DICT=None):
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
            self.ProxyGroups.append(ProxyGroup(DICT=i, config=self))
        for i in self._DICT["proxies"]:
            self.Proxies.append(
                Proxy(DICT=i, proxies_list=self.Proxies, proxy_groups_list=self.ProxyGroups))
        for i in self._DICT["rules"]:
            self.Rules.append(Rule(YAML=i, config=self))

    @property
    def YAML(self):
        return yaml.dump(self.DICT)

    @YAML.setter
    def YAML(self, YAML):
        self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)


class ProxyGroup():
    def __init__(self, DICT=None, YAML=None, config=None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        else:
            raise ValueError

        def _bind(config):
            if not config == None:
                self.proxy_groups_list_remove = config.ProxyGroups.remove
                self.proxy_groups_list_getitem = config.ProxyGroups.__getitem__
                self.proxy_groups_list_len = config.ProxyGroups.__len__
                self.rules_list_getitem = config.Rules.__getitem__
                self.rules_list_len = config.Rules.__len__
            else:
                self.proxy_groups_list_remove = None
                self.proxy_groups_list_getitem = None
                self.proxy_groups_list_len = None
                self.rules_getitem = None
                self.rules_list_len = None
        self.__bind__ = _bind

        self.__bind__(config)

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, proxies):
        self._proxies = proxies
        for i in self._proxies:
            i.bind(self._proxies)

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

    def bind(self, config):
        self.__bind__(config)

    def delete(self, strategy=None):
        if strategy == None:
            if self.rules_list_len:
                tmp_length = self.rules_list_len()
                for i in range(0, tmp_length):
                    if i >= tmp_length:
                        break
                    self.rules_list_getitem(i).delete()
                    tmp_length = self.rules_list_len()
        else:
            if self.rules_list_len:
                for i in range(0, self.rules_list_len()):
                    self.rules_list_getitem(i).strategy = strategy

        if self.proxy_groups_list_remove:
            self.proxy_groups_list_remove(self)

        if self.proxy_groups_list_len:
            for i in range(0, self.proxy_groups_list_len()):
                tmp = select(self.proxy_groups_list_getitem(
                    i).proxies, False, name=self.name)
                if tmp:
                    tmp.delete()


class Rule():
    def __init__(self, type=None, matchedTraffic=None, strategy=None, YAML=None, config=None):
        if (type == None or matchedTraffic == None or strategy == None) and YAML == None:
            raise ValueError
        elif YAML == None:
            self.type = type
            self.matchedTraffic = matchedTraffic
            self.strategy = strategy
        else:
            self.YAML = YAML

        def _bind(config):
            if not config == None:
                self.rules_list_remove = config.Rules.remove
            else:
                self.rules_list_remove = None
        self.__bind__ = _bind

        self.__bind__(config)

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

    def bind(self, config):
        self.__bind__(config)

    def delete(self):
        if self.rules_list_remove:
            self.rules_list_remove(self)
