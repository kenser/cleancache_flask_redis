# coding=utf8
from flask import jsonify,flash,request,make_response,render_template,request,redirect,session,url_for
from app import app
from app import redis_store

@app.errorhandler(401)
def not_auth(error):
    return redirect(url_for('login'))

class User():
    username = redis_store.hget('user','username')
    password = redis_store.hget('user','password')

@app.route('/cclogin', methods=['GET', 'POST'])
def login():
    username = None
    user = User()

    #登录判断用户密码是否正确
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash(u'用户名密码错误')
            return redirect(url_for('login'))
    #如果session存在则直接跳到管理首页
    if session.get('username') == user.username:
        #持久化redis数据到硬盘
        redis_store.save()
        return redirect(url_for('index'))
        
    return render_template('account/login.html', username=session.get('username'))

@app.route('/cclogout', methods=['GET'])
def logout():
    session['username'] = None
    #持久化redis数据到硬盘
    redis_store.save()
    return redirect(url_for('login')) 
