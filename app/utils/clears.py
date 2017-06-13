#!coding=utf8
from urlparse import urlparse
import requests
import logging
from bs4 import BeautifulSoup
import re
import os
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8') 




def clearnginx(urlstr,remote_ip):
    hostname = urlparse(urlstr).hostname
    if hostname is None:
        message = "%s is not a valid url" % urlstr
        result = {'status':'error','message':message} 
        logs(message+" "+remote_ip) 
        return result 

    #获取url后缀
    schemelen = len(urlparse(urlstr).scheme)
    hostnamelen = len(hostname)
    urlpath = urlstr[schemelen+hostnamelen+3:]
    if urlpath == '':
        urlpath = '/'


    #判断domain是否在配置文件中
    try:
        from app import redis_store
        #从redis取的对应域名的ip
        ips = redis_store.hget("nginxip",hostname).split(',')
        if ips is None:
            message = "url %s hostname %s Not nginx cached" % (urlstr,hostname)
            result = {'status':'error','message': message}
            logs(message+" "+remote_ip) 
            return result 
    except Exception:
        message = "url %s hostname %s Not nginx cached" % (urlstr,hostname)
        result = {'status':'error','message': message} 
        logs(message+" "+remote_ip)
        return result 

    message = ""
    
    #判断对应的ip80端口是否还在启用状态
    from app.utils.verify import verify_ip
    ips80 = []
    for ip80 in ips:
        if verify_ip(ip80) is True:
            ips80.append(ip80) 

    #执行nginx purge cache
    for ip in ips80:
        headers = {'host':hostname}
        purgeurl = "http://"+ip+"/purge"+urlpath
        rhtml = requests.get(purgeurl,headers=headers,timeout=15)
        httpStatus = str(rhtml.status_code)
        soup = BeautifulSoup(str(rhtml.text).replace("\r\n",""),"html.parser")
        key = str(soup.find_all(text=re.compile("Key")))
        path =  str(soup.find_all(text=re.compile("Path")))
        title = str(soup.title)
        message += " nginx_ip : %s ,httpStatus : %s ,title : %s ,key : %s ,path : %s "  % (ip,httpStatus,title,key,path)
    result = {'status':'success','message':message}
    logs("url "+ urlstr +message+" "+remote_ip)
    return result 

def clearcdn(urlstr,remote_ip, network):
    #从redis读取akamai相关配置参数
    from app import redis_store
    #weurl = redis_store.hget('wechat','weurl')

    #akamaiusername = redis_store.hget('akamai','username')
    #akamaipassword = redis_store.hget('akamai','password')
    apiurl = redis_store.hget('akamaiv3','apiurl')
    #执行akamai clear cdn cache
    headers = {'content-type': 'application/json'}
    data = '{"clean_url":"%s","network":"%s"}' % (urlstr,network)
    r = requests.post(apiurl,data=data,headers=headers)
    logs("url "+ urlstr + str(r) + remote_ip)
    return r.json()

def logs(message):
    from app import config
    try:
        logpath = config.LOG_PATH
        logname = config.LOG_NAME
    except Exception:
        pass
    mkDir(logpath)
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logpath+logname,
        filemode='a')

    return logging.info(message)

def mkDir(path):
    if os.path.exists(path) is False:
        os.makedirs(path)
    pass  
