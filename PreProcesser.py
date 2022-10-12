import requests
import yaml
import re


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


class Proxy:
    def __init__(self, DICT=None, YAML=None, proxies_list=None, proxy_groups_list=None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)[0]
        else:
            raise ValueError
        self.name = self.DICT["name"]

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

    def rename(self, name):
        self.name = name
        self.DICT["name"] = name

    def bind(self, proxies_list, proxy_groups_list=None):
        self.__bind__(proxies_list, proxy_groups_list)

    def delete(self):
        raise RuntimeError("To Do: Active Sync")
        if self.proxy_groups_list_len:
            tmp_length = self.proxy_groups_list_len()
            for i in range(0, self.proxy_groups_list_len()):
                if i == tmp_length:
                    break
                for j in self.proxy_groups_list_getitem(i).proxies:
                    if j.name == self.name:
                        j.delete()
                tmp_length = self.proxy_groups_list_len()
        if self.proxies_list_remove:
            self.proxies_list_remove(self)
    
    def dump(self):
        return self.DICT


class Config():
    def __init__(self, url=None, YAML=None, path=None):
        if url:
            res = requests.get(url)
            self.sub_info = {
                "subscription-userinfo": res.headers["subscription-userinfo"]}
            self.file = yaml.load(res.text.encode("utf-8"), Loader=yaml.Loader)
        elif YAML:
            self.file = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        elif path:
            self.file = yaml.load("\n".join(open(path, "r").readlines()).encode(
                "utf-8"), Loader=yaml.Loader)
        else:
            raise ValueError

        self.Proxies = []
        self.ProxyGroups = []
        self.Rules = []
        for i in self.file["proxy-groups"]:
            self.ProxyGroups.append(ProxyGroup(DICT=i, config=self))
        for i in self.file["proxies"]:
            self.Proxies.append(
                Proxy(DICT=i, proxies_list=self.Proxies, proxy_groups_list=self.ProxyGroups))
        for i in self.file["rules"]:
            self.Rules.append(Rule(YAML=i, config=self))

    def getProxies(self, groups=False, embedded=False):
        result = self.Proxies
        if groups:
            result += [Proxy(DICT={"name": i.name}, proxies_list=result)
                       for i in self.ProxyGroups]
        if embedded:
            result += [Proxy(DICT={"name": "DIRECT"}, proxies_list=result),
                       Proxy(DICT={"name": "REJECT"}, proxies_list=result)]
        return result

    def insert(self, obj, i, item):
        obj.insert(i, item)

    def cover(self, YAML=None, DICT=None):
        raise RuntimeError("To Do")
        if DICT:
            pass
        elif YAML:
            tmp = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        else:
            raise ValueError

    def pop_front(self, obj, item):
        obj.insert(0, item)

    def pop_back(self, obj, item):
        obj.append(item)

    def dump(self):
        self.file["proxies"] = [i.dump() for i in self.Proxies]
        self.file["proxy-groups"] = [i.dump() for i in self.ProxyGroups]
        self.file["rules"] = [i.dump() for i in self.Rules]
        return yaml.dump(self.file)


class ProxyGroup():
    def __init__(self, DICT=None, YAML=None, config=None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        else:
            raise ValueError
        self.name = DICT["name"]
        self.proxies = []
        self.proxies = [
            Proxy(DICT={"name": i}, proxies_list=self.proxies) for i in DICT["proxies"]]
        for i in self.proxies:
            i.bind(self.proxies)

        def _bind(config):
            if not config == None:
                self.proxy_groups_list_remove = config.ProxyGroups.remove
                self.rules_list_getitem = config.Rules.__getitem__
                self.rules_list_len = config.Rules.__len__
            else:
                self.proxy_groups_list_remove = None
                self.rules_getitem = None
                self.rules_list_len = None
        self.__bind__ = _bind

        self.__bind__(config)

    def rename(self, name):
        self.name = name
        self.DICT["name"] = name

    def getProxy(self, ):
        return self.proxies

    def modifyProxies(self, proxies):
        self.proxies = proxies
        self.DICT["proxies"] = [i.name for i in proxies]

    def bind(self, config):
        self.__bind__(config)

    def delete(self, strategy=None):
        raise RuntimeError("To Do: Check and detele self from other proxy-groups")
        if not strategy == None:
            if self.rules_list_len:
                tmp_length = self.rules_list_len()
                for i in range(0, self.rules_list_len()):
                    if i == tmp_length:
                        break
                    self.rules_list_getitem(i).delete()
                    tmp_length = self.rules_list_len()
        else:
            if self.rules_list_len:
                for i in range(0, self.rules_list_len()):
                    self.rules_list_getitem(i).modify(strategy=strategy)
        if self.proxy_groups_list_remove:
            self.proxy_groups_list_remove(self)
    
    def dump(self):
        raise RuntimeError("To Do")
        self.DICT["proxies"] = [i.name for i in self.proxies]
        return self.DICT


class Rule():
    def __init__(self, type=None, matchedTraffic=None, strategy=None, YAML=None, config=None):
        if (type == None or matchedTraffic == None or strategy == None) and YAML == None:
            raise ValueError
        elif YAML == None:
            self.type = type
            self.matchedTraffic = matchedTraffic
            self.strategy = strategy
        else:
            tmp = YAML.split(",")
            if len(tmp) == 3:
                self.type = tmp[0]
                self.matchedTraffic = tmp[1]
                self.strategy = tmp[2]
            else:
                self.type = None
                self.matchedTraffic = tmp[0]
                self.strategy = tmp[1]

        if not self.type == None:
            self.YAML = self.type + "," + self.matchedTraffic + "," + self.strategy
        else:
            self.YAML = self.matchedTraffic + "," + self.strategy

        def _bind(config):
            if not config == None:
                self.rules_list_remove = config.Rules.remove
            else:
                self.rules_list_remove = None
        self.__bind__ = _bind

        self.__bind__(config)

    def modify(self, type=None, matchedTraffic=None, strategy=None, YAML=None):
        if type == None and matchedTraffic == None and strategy == None and YAML == None:
            raise ValueError
        elif not YAML == None:
            tmp = YAML.split(",")
            self.type = tmp[0]
            self.matchedTraffic = tmp[1]
            self.strategy = tmp[2]
        else:
            if not type == None:
                self.type = type
            if not matchedTraffic == None:
                self.matchedTraffic = matchedTraffic
            if not strategy == None:
                self.strategy = strategy

        if not self.type == None:
            self.YAML = self.type + "," + self.matchedTraffic + "," + self.strategy
        else:
            self.YAML = self.matchedTraffic + "," + self.strategy

    def bind(self, config):
        self.__bind__(config)

    def delete(self):
        if self.rules_list_remove:
            self.rules_list_remove(self)

    def dump(self):
        return self.YAML
