import yaml
import re
import requests
from copy import deepcopy

class Clash():
    def __init__(self, url):
        self.url = url
        self.content = requests.get(url).text.encode('utf-8')
        self.file = yaml.load(self.content, Loader=yaml.Loader)

    # def replace(self, old, new):
    #     pass

    def del_proxy_group(self, name, policy=None):
        # policy refers to the policy replaced by the rule corresponding to the original rule set after the rule set is deleted
        for i in range(len(self.file['proxy-groups'])-1, -1, -1):
            if name == self.file['proxy-groups'][i]['name']:
                del self.file['proxy-groups'][i]
        for i in range(len(self.file['rules'])-1, -1, -1):
            rl = self.file['rules'][i].split(',')
            try:
                if rl[2] == name:
                    if policy == None:
                        del self.file['rules'][i]
                    else:
                        del rl[2]
                        rl.append(policy)
                        self.file['rules'][i] = ','.join(rl)
            except:
                pass

    def append_proxy(self, dict):
        self.file['proxies'].append(dict)

    def append_proxy_group(self, dict):
        self.file['proxy-groups'].append(dict)
    
    def insert_proxy_group(self, dict):
        self.file['proxy-groups']=[dict]+self.file['proxy-groups']

    def proxy_selector(self, pattern=None, reverse_select=False, proxies=None):
        # mode can be select or reverse_select
        if proxies == None:
            all_proxies = [i['name'] for i in self.file['proxies']]
        else:
            all_proxies=proxies
        result = []
        if reverse_select:
            for i in all_proxies:
                if not re.search(pattern, i):
                    result.append(i)
        else:
            for i in all_proxies:
                if re.search(pattern, i):
                    result.append(i)
        return deepcopy(result)

    def insert_rules(self, type=None, content=None, policy=None, list=None):
        if not list == None:
            self.file['rules'] = list + self.file['rules']
        elif not type == None and not content == None and not policy == None:
            self.file['rules'].insert(0, type + ',' + content + ',' + policy)
        else:
            raise ValueError()

    def del_rules(self, type=None, content=None, policy=None):
        for i in range(len(self.file['rules'])-1, -1, -1):
            rl = self.file['rules'][i].split(',')
            if type == None and content == None and policy == None:
                raise ValueError("insufficient conditions provided")
            try:
                if (rl[0] == type or type == None) and (rl[1] == content or content == None) and (rl[2] == policy or policy == None):
                    del self.file['rules'][i]
            except:
                pass

    def modify_proxy_group(self, name=None, proxies=None, new_name=None):
        j = None
        for i in range(0, len(self.file['proxy-groups'])):
            if self.file['proxy-groups'][i]['name'] == name:
                j = i
                break
        if j == None:
            raise ValueError()
        if not proxies == None:
            self.file['proxy-groups'][j]['proxies'] = proxies
        if not new_name == None:
            for i in range(len(self.file['rules'])-1, -1, -1):
                rl = self.file['rules'][i].split(',')
                try:
                    if rl[2] == name:
                        del rl[2]
                        rl.append(new_name)
                        self.file['rules'][i] = ','.join(rl)
                except:
                    pass
            self.file['proxy-groups'][j]['name'] = new_name
        if proxies == None and new_name == None:
            raise ValueError()

    def dump(self):
        return yaml.dump(self.file)
