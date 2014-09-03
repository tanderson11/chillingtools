from config import *
from customize import *
from search_params import *

import os
import re
import subprocess
import json
import time
import calendar

### Requests to the databse ###

def curl(flags, completion, authentication_key=False):
    command = [CURL_ROOT]
    command.extend(DEFAULT_FLAGS)
    command.extend(flags)
    command.append(URL_ROOT + completion)
    out = subprocess.check_output(command)
    return out

def recover(hashed, search=False):
    print "Recovering cached file."
    f = open(os.path.join(CACHE_ROOT, str(hashed)), "r")
    d = f.read()
    f.close()
    return d

def build(data, hashed):
    print "Building file into cache."
    f = open(os.path.join(CACHE_ROOT, str(hashed)), "w+")
    f.write(data)
    f.close()

def process_user_macro(args):
    name = args[0]
    args = args[1:]
    required_args = {"date": 1, "range": 2, "daterange": 2}
    try:
        if required_args[name] != len(args):
            raise Exception("{0} takes {1} arguments. You gave {2}".format(name, required_args, len(args)))
    except KeyError:
        raise Exception("{0} is not defined as a macro.".format(name))
    if name == "date":
        return str(calendar.timegm(time.strptime(args[0], "%Y/%m/%d"))) #year month day 2014/09/03
    if name == "range":
        return args[0] + ".." + args[1]
    if name == "daterange":
        return "{{range {{date {0}}} {{date {1}}}}}".format(args[0], args[1])

def process_user_input(stream):
    stream = stream.lower()
    while re.findall(r'{([^{}]*)}', stream):
        stream = re.sub(r'{([^{}]*)}', lambda m: process_user_macro(m.group(1).split(' ')), stream)
    terms = stream.split(' ')
    return terms

def search(dic, cache_override=False):
    ### 
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
        if os.path.exists(os.path.join(CACHE_ROOT + str(hashed))) and not cache_override:
            restore = True
            return SEARCH_HANDLER(recover(hashed, True))

    target = SEARCH_SUFFIX
    for n,ql in dic.iteritems():
        p = PARAMS[n]
        if ql[-1] == "require_all":
            ql.pop()
            req_all = True
        else:
            req_all = False
        for i in xrange(0, len(ql)):
            t = ql[i]
            del ql[i]
            ql[i-1:i-1] = process_user_input(t)
            print ql
        print p.generate_request(ql, req_all)
        target += p.generate_request(ql, req_all) + "&"
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
    while True:
        try:
            if PARAMS[n].require_all:
                query_string = raw_input("Value(s)? (separate by spaces) ")
            else:
                query_string = raw_input("Value? ")
            query_string = query_string.lower()
            query_list = process_user_input(query_string)
                
            if PARAMS[n].require_all and len(query_list) > 1:
                r = raw_input("Require all (Y/n)? ")+"y"
                if r[0] == "y":
                    query_list.append("require_all")

            break
        except Exception as m:
            print "{0} Please try again.".format(m)

    return query_list

def interactive_search(fully_interactive=True, seed_dic={}, cache_override=False):
    dic = {}
    dic = dict(seed_dic.items() + dic.items())
    if fully_interactive:
        for n,o in PARAMS.iteritems():
            output(dic)
            describe(n, o)
            query_list = query(n)
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

    return search(dic, cache_override=cache_override)

def download(notice_id, cache_override=False):
    restore = False
    if CACHE_BOOL:
        hashed = abs(hash(str(notice_id))) % (10 ** 15)
        if os.path.exists(os.path.join(CACHE_ROOT, str(hashed))) and not cache_override:
            restore = True
            return DOWNLOAD_HANDLER(recover(hashed))
    response = curl([], "{0}.json".format(str(notice_id)))
    if CACHE_BOOL and not restore:
        build(response, hashed)
    return DOWNLOAD_HANDLER(response)

def download_set(l, cache_override=False):
    ret_values = []
    for i in l:
        try:
            ret_values.append(download(int(i), cache_override=cache_override))
        except ValueError:
            print "{0} could not be coerced to an integer."
            return False
    return ret_values
