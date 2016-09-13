import urllib2
import simplejson as json
import sys
class weChat:
    def __init__(self,url,Corpid,Secret): 
        url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url,Corpid,Secret)
        res = self.url_req(url)
        self.token = res['access_token']

    def url_req(self,url,method='get',data={}):
        if method == 'get':
            req = urllib2.Request(url)
            res = json.loads(urllib2.urlopen(req).read())
        elif method == 'post':
                        req = urllib2.Request(url,data)
                        res = json.loads(urllib2.urlopen(req).read())
        else:
            print 'error request method...exit'
            sys.exit()  
        return res
    def send_message(self,groupids,content,agentid=0):
        self.groupids = groupids
        self.content = content
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % self.token
        data = {
                      "touser": "",
                      "toparty": "",
                      "totag": "",
                      "msgtype": "text",
                      "agentid": "0",
                      "text": {
                          "content": ""
                      },
                      "safe":"0"
                   } 
        data['toparty'] = groupids
        data['agentid'] = agentid
        data['text']['content'] = content
        data = json.dumps(data,ensure_ascii=False)
    #   print data
        res = self.url_req(url,method='post',data=data)
        if res['errmsg'] == 'ok':
            print 'send sucessed!!!'
        else:
            print 'send failed!!'
            print res
