from config import *
from search_params import *

import os
import re
import subprocess
import json

### Handler functions ###

def default_download_handler(response):
    return json.loads(response)

def default_search_handler(response):
    return json.loads(response)

###

### Default handlers ###

DOWNLOAD_HANDLER = default_download_handler
SEARCH_HANDLER = default_search_handler

###

def curl(flags, completion, authentication_key=False):
    command = [CURL_ROOT]
    command.extend(DEFAULT_FLAGS)
    command.extend(flags)
    command.append(URL_ROOT + completion)
    out = subprocess.check_output(command)
    return out

def recover(hashed, search=False):
    print "Recovering cached file."
    f = open(CACHE_ROOT + str(hashed), "r")
    d = f.read()
    f.close()
    return d

def build(data, hashed):
    print "Building file into cache."
    f = open(CACHE_ROOT + str(hashed), "w+")
    f.write(data)
    f.close()

def process_user_input(stream):
    stream = stream.lower()
    commands = re.findall(r'{(.*)}', stream)
    stream = re.sub(r'{.*}', ' ', stream)
    terms = stream.split(' ')
    for c in commands:
        if c == "":
            pass
    return terms

def search(dic):
    restore = False
    if CACHE_BOOL:
        ul = []
        us = ""
        for n,ql in dic.iteritems():
            ul.append((n, ql))
        for t in sorted(ul):
            us += t[0]
            for qt in sorted(t[1]):
                us += str(qt)
        hashed = abs(hash(us)) % (10 ** 15)
        if os.path.exists(CACHE_ROOT + str(hashed)):
            restore = True
            return SEARCH_HANDLER(recover(hashed, True))

    target = SEARCH_SUFFIX
    for n,ql in dic.iteritems():
        p = PARAMS[n]
        if p.require_all:
            req_all = ql.pop()
            print ql
            print p.generate_request(ql, req_all)
            target += p.generate_request(ql, req_all) + "&"
        else:
            target += p.generate_request(ql) + "&"
    flags = ['-H', 'Accept: application/json', '-H', 'Content-type: application/json']
    response = curl(flags, target)
    if CACHE_BOOL and not restore:
        build(response, hashed)
    return SEARCH_HANDLER(response)

def output(dic):
    os.system('cls' if os.name == 'nt' else 'clear')
    for k,v in dic.iteritems():
        if PARAMS[k].require_all:
            print "{0}:{1} | Require all: {2}.".format(k,str(v[0:-1]),"yes" if v[-1] else "no")
        else:
            print "{0}:{1}".format(k,str(v))
def describe(name, obj):
    print "#"*10 + "\n{0}: {1}\n".format(name,obj.description) + "#"*10

def query(n):
    if PARAMS[n].require_all:
        query_string = raw_input("Value(s)? (separate by spaces) ")
        query_string = query_string.lower()
        query_list = process_user_input(query_string)
        require_all = False
        if len(query_list) > 1:
            r = raw_input("Require all (Y/n)? ")+"y"
            if r[0] == "y":
                require_all = True
        query_list.append(require_all)
    else:
        query_string = raw_input("Value? ")
        query_string = query_string.lower()
        query_list = process_user_input(query_string)
    return query_list

def interactive_search(fully_interactive=True, seed_dic={}):
    dic = {}
    if fully_interactive:
        for n,o in PARAMS.iteritems():
            output(dic)
            describe(n, o)
            query_list = query(n)
            print query_list
            if query_list[0] != "":
                dic[n] = query_list
    else:
        a = "y"
        while a[0] == "y":
            output(dic)
            param_name = raw_input("Paramter name? ")
            describe(param_name, PARAMS[param_name])
            query_list = query(param_name)
            if query_list[0] != "":
                dic[param_name] = query_list
            a = raw_input("Another? (Y/n) ")+"y"

    dic = dict(seed_dic.items() + dic.items())
    return search(dic)

def download(notice_id):
    restore = False
    if CACHE_BOOL:
        hashed = abs(hash(str(notice_id))) % (10 ** 15)
        if os.path.exists(CACHE_ROOT + str(hashed)):
            restore = True
            return DOWNLOAD_HANDLER(recover(hashed))
    response = DOWNLOAD_HANDLER(curl([], "{0}.json".format(str(notice_id))))
    if CACHE_BOOL and not restore:
        build(response, hashed)
    return response

def download_set(l):
    ret_values = []
    for i in l:
        ret_values.append(download(i))
    return ret_values
