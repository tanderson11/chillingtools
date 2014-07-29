from config import *
from search_params import *

import re

### Default handlers ###

DOWNLOAD_HANDLER = download_handler
SEARCH_HANDLER = search_handler

###

### Handler functions ###

def default_download_handler():
    pass

def default_search_handler():
    pass

###

def curl(flags, completion):
    pass

def process_user_input(stream):
    stream = stream.lower()
    commands = re.findall(r'{(.*)}', stream)
    stream = re.sub(r'{.*}', ' ', stream)
    terms = stream.split(' ')
    for c in commands:
        if c == "":
            pass

def search(dic):
    if CACHE_BOOL:
        ul = []
        us = ""
        for n,ql in dic.iteritems():
            ul.append((n, ql))
        for t in sorted(ul):
            us += t[0]
            for qt in sorted(t[1]):
                us += qt
        hash = abs(hash(us)) % (10 ** 15)
        if os.path_exists(CACHE_ROOT + hash):
            pass

    target = SEARCH_SUFFIX
    for n,ql in dic.iteritems():        
        p = PARAMS[n]
        target += p.generate_request(ql) + "&"
    flags = ['-H', 'Accept: application/json', '-H', 'Content-type: application/json']
    return curl(target)

def interactive_search(fully_interactive, seed_dic={}):
    dic = {}
    if fully_interactive:
        pass
    else:
        pass

    dic = dict(seed_dic.items() + dic.items())
    return search(dic)

def download():
    pass
