# coding=utf8
from flask import flash,jsonify,request,make_response,render_template,request,redirect,session,url_for
import json
from app import app
from app import redis_store
from app import api
from functools import wraps


@app.errorhandler(401)
def not_auth(error):
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = redis_store.hget('user','username')
        if username != session.get('username'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/ccadmin', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

@app.route('/ccadmin/nginx', methods=['GET'])
@login_required
def nginx():
    
    fenyeno = 15
    hashname = 'nginxip'
    from app.utils.fenye import fenYe
    posts,allPage,curPage,allCounts,all = fenYe(request,fenyeno,hashname)
    addno = fenyeno * (curPage - 1)
    lists = range(1,allPage+1)
    r = {'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists,'allCounts':allCounts,'all':all}
    return render_template('nginx/table.html',r=r)



@app.route('/ccadmin/nginxsearch', methods=['POST','GET'])
@login_required
def nginxsearch():
    if request.method == 'POST':
        searchstr=request.form['searchstr'].strip()
        session['searchstr'] = searchstr
    searchstr = session.get('searchstr')
    fenyeno = 15
    hashname = 'nginxip'
    from app.utils.fenye import fenYeSearch
    posts,allPage,curPage,allCounts,all = fenYeSearch(request,fenyeno,hashname,searchstr)
    addno = fenyeno * (curPage - 1)
    lists = range(1,allPage+1)
    r = {'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists,'allCounts':allCounts,'all':all}
    return render_template('nginx/table.html',r=r)


@app.route('/ccadmin/nginxedit/<domain>', methods=['GET','POST'])
@login_required
def nginxedit(domain):
    if request.method == 'POST':
        ipsstr=request.form['ips'].strip()
        ips=ipsstr.split(',')
        #编辑时只允许编辑IP
        #校验IP
        from app.utils.verify import verify_ip
        ipflag=0
        for ip in ips:
            if verify_ip(ip) is False:
                ipflag=ipflag+1
                flash(u'IP校验失败，请检查')


        #ip都校验通过后则进行保存到redis动作
        if ipflag == 0:
            redis_store.hset('nginxip',domain,ipsstr)
            return redirect(url_for('nginx'))

    
    #如果不是post则是get，并做如下动作
    k=domain
    v=redis_store.hgetall('nginxip')[k]
    r = {'k':k,'v':v}
    return render_template('nginx/edit.html',r=r)


@app.route('/ccadmin/nginxdel/<domain>', methods=['GET'])
@login_required
def nginxdel(domain):
    k=domain
    redis_store.hdel('nginxip',k)
    return redirect(url_for('nginx'))


@app.route('/ccadmin/nginxadd', methods=['GET','POST'])
@login_required
def nginxadd():
    if request.method == 'POST':
        domain=request.form['domain'].strip()
        ipsstr=request.form['ips'].strip()
        ips=ipsstr.split(',')
        #校验IP
        ipflag=0
        from app.utils.verify import verify_ip
        for ip in ips:
            if verify_ip(ip) is False:
                ipflag=ipflag+1
                flash(u'IP校验失败，请检查')

        #校验域名
        from app.utils.verify import verify_domain
        if verify_domain(domain) is False:
            flash(u'域名校验失败，请检查')
        #域名是否已经存在
        domainexists=redis_store.hexists('nginxip',domain)
        if domainexists is True:
            flash(u'域名已经存在，不能新增添加，只能编辑')
        #域名和ip都校验通过后则进行保存到redis动作
        if verify_domain(domain) == True and ipflag == 0 and domainexists == False:
            redis_store.hset('nginxip',domain,ipsstr)
            return redirect(url_for('nginx'))
    return render_template('nginx/add.html')

@app.after_request
def app_after_request(response):  
    if request.endpoint != 'static':
        return response
    response.cache_control.max_age = 15552000
    return response
