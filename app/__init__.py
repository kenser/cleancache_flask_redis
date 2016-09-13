#coding=utf8
import os
from flask import Flask

#-- create app --
app = Flask(__name__)

#读配置文件
app.config.from_object("app.config")

#初始化redis
from flask.ext.redis import FlaskRedis
redis_store = FlaskRedis(app)

#初始化flask-bootstrap
#from flask.ext.bootstrap import Bootstrap
#bootstrap = Bootstrap(app)

#初始化flask-login
#from flask.ext.login import LoginManager
#login_manager = LoginManager(app)

#Flask-WTF


from flask import jsonify,make_response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(401)
def not_auth(error):
    return make_response(jsonify({'error': 'not_auth'}), 401)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(Exception)
def all_exception_handler(error):
    print "exception: %s" %error
    return u'暂时无法访问，请联系管理员', 500

from view import api
from view import admin
from view import account
