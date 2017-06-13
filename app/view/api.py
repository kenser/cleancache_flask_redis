# coding=utf8
from flask import jsonify,make_response,request
import json
from app import app
from app import redis_store



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


#获取远程客户端IP
@app.route('/ip', methods=['GET'])
def get_ip():
    remote_ip = request.remote_addr
    return make_response(jsonify({'your ip': remote_ip}), 200)

#订阅亚马逊告警信息
@app.route('/lbalert', methods=['POST', 'GET'])
def lbAlert():
    if request.method == 'POST':
        headers = request.headers
        data = request.data
        all = json.loads(data)

        # print all["Message"]
        message = json.loads(all["Message"])
        # print message["AlarmName"]
        # print message["NewStateReason"]
        content = "AlarmName:\"" + str(message["AlarmName"]) + "\"" 

        #从redis中读取weChat相关配置参数
        weurl = redis_store.hget('wechat','weurl')
        weCorpid = redis_store.hget('wechat','weCorpid')
        weSecret = redis_store.hget('wechat','weSecret')
        wegroupids = redis_store.hget('wechat','wegroupids')

        #发微信
        from app.utils.send import weChat
        wechat = weChat(weurl, weCorpid, weSecret)
        wechat.send_message(wegroupids, content)

        return "yes yes"

    else:
        return "no no"

#清理cdn和nginx缓存
@app.route('/clear', methods=['GET'])
def get_url():
    urlstr = request.full_path.strip()
    if '&purge_url=' in urlstr:
        urlstr = urlstr.split('&purge_url=')[1]
    else:
        urlstr = request.full_path[11:].strip()

    # 执行清理缓存
    from app.utils.clears import clearnginx
    from app.utils.clears import clearcdn
    remote_ip = request.remote_addr
    resultnginx = clearnginx(urlstr, remote_ip)
    #networks = ('production','staging')
    resultproduction = clearcdn(urlstr, remote_ip, network='production')
    resultstaging = clearcdn(urlstr, remote_ip, network='staging')
    results = {'results': [{"url": urlstr}, {"type": "nginx", "result": resultnginx}, {
        "production": resultproduction, "staging": resultstaging}]}
    return jsonify(results)




