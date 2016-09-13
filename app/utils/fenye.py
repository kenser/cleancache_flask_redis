# coding=utf8
from app import redis_store
def fenYe(request,fenyeno,hashname):
    all=redis_store.hgetall(hashname)
    allkeys=redis_store.hkeys(hashname)
    allCounts = redis_store.hlen(hashname)

    try:
        curPage = int(request.args.get('curPage','1'))
        allPage = int(request.args.get('allPage','1'))
        pageType = str(request.args.get('pageType',''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * fenyeno
    endPos = startPos + fenyeno

    posts = allkeys[startPos:endPos]


    if curPage == 1 and allPage == 1:
        allPage = allCounts / fenyeno
        remainPost = allCounts % fenyeno
        if remainPost > 0:
            allPage += 1
    return posts,allPage,curPage,allCounts,all



def fenYeSearch(request,fenyeno,hashname,searchstr):
    #根据searchstr查询出所有key
    allkeys=[]
    for key in redis_store.hkeys(hashname):
        if searchstr in key:
            allkeys.append(key)
    #求搜索相关的所有keys的个数
    allCounts=len(allkeys)
    #求出相关的所有key和value
    all={}
    for k in allkeys:
       all[k]=redis_store.hget(hashname,k) 


    try:
        curPage = int(request.args.get('curPage','1'))
        allPage = int(request.args.get('allPage','1'))
        pageType = str(request.args.get('pageType',''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * fenyeno
    endPos = startPos + fenyeno

    posts = allkeys[startPos:endPos]


    if curPage == 1 and allPage == 1:
        allPage = allCounts / fenyeno
        remainPost = allCounts % fenyeno
        if remainPost > 0:
            allPage += 1
    return posts,allPage,curPage,allCounts,all

