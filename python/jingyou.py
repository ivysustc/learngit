from gevent import monkey;

monkey.patch_all()
import random
import gevent
import urllib2
import urllib
from bs4 import BeautifulSoup
import MySQLdb
import sys


def openURl(pk, pi):
    url = 'http://www.jyeoo.com/math3/ques/partialques'
    url += '?q=' + pk
    url += '&f=0&tk=0&ct=0&dg=0&fg=0&po=0&pd=1'
    url += '&pi=' + str(pi)
    url += '&r=' + str(random.random())
    data = {}
    headers = {
        'Cookie': 'QS_ED=6; QS_GD=3; QS_TM=1; JYERN=0.276221488734119; j_math3_q_q_0=412d080b-9b13-4ea9-a43a-954b7ddb0dbe~9a05ba92-deee-408e-9190-686363d8f9da~9C; j_math3_q_ct=1; j_math3_q_dg=0; j_math3_q_fg=0; j_math3_q_po=0; j_math3_q_pd=1; jyean=Tuqj3knIzxeZ9EBcRoxxZ65GdnDkWslZRKvLrvnPVjQ-PqFZUuw--p-uUjFLbNAuFfPrv9356n2VZDIYLGcNeOjLyTKgr1N06w-TuZ4fKHw7vMhbCzi4yHedq08BTgKx0; JYE_FP2=15fa7fa0d7035f0f9b378a4521345c88; JYERN=0.5587514430074363'
        ,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        , 'Referer': 'http://www.jyeoo.com/math3/ques/search'
        , 'Host': 'www.jyeoo.com'
    }
    data = urllib.urlencode(data)
    request = urllib2.Request(url, data, headers)
    while 1:
        try:
            resp = urllib2.urlopen(request)
            response = resp.read()
            break
        except:
            gevent.sleep(10)
            continue
    return response


def findProblemUrl(id, pk, pi):
    resp = openURl(pk, pi)
    soap = BeautifulSoup(resp, from_encoding='utf-8')
    problems = soap.findAll('span', class_='fieldtip')
    for problemTemp in problems:
        url = problemTemp.findAll('a')[0]['href']
        insertProblem(id, url)
    updateCatelog(id)
    print pk, pi, 'done'
    return

def parsePt(pt):
    content=[]
    nodes=pt.contents
    for nodetemp in nodes:
        if isinstance(nodetemp,basestring):
            content.append({'name':'string','content':nodetemp})
        else :
            name=nodetemp.name
            if name =='img':
                content.append({'name':'img','src':nodetemp['src'],'style':nodetemp['style']})
            if name =='br':
                content.append({'name':'br'})
            if name == 'div':
                content.append({'name':'div','class':nodetemp['class'],'content':nodetemp.string})
    return content

def parsePt2(pt2):
    options=[]
    nodes=pt2.findAll('td',class_='selectoption')
    for node in nodes:
        options.append(parsePt(node.find('label')))
    return options


def findProblemContent(id,url):
    data = {}
    headers = {
        'Cookie': 'QS_ED=6; QS_GD=3; QS_TM=1; JYERN=0.276221488734119; j_math3_q_q_0=412d080b-9b13-4ea9-a43a-954b7ddb0dbe~9a05ba92-deee-408e-9190-686363d8f9da~9C; j_math3_q_ct=1; j_math3_q_dg=0; j_math3_q_fg=0; j_math3_q_po=0; j_math3_q_pd=1; jyean=Tuqj3knIzxeZ9EBcRoxxZ65GdnDkWslZRKvLrvnPVjQ-PqFZUuw--p-uUjFLbNAuFfPrv9356n2VZDIYLGcNeOjLyTKgr1N06w-TuZ4fKHw7vMhbCzi4yHedq08BTgKx0; JYE_FP2=15fa7fa0d7035f0f9b378a4521345c88; JYERN=0.5587514430074363'
        ,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        , 'Referer': 'http://www.jyeoo.com/math3/ques/search'
        , 'Host': 'www.jyeoo.com'
    }
    data = urllib.urlencode(data)
    request = urllib2.Request(url, data, headers)
    while 1:
        try:
            resp = urllib2.urlopen(request)
            response = resp.read()
            break
        except:
            gevent.sleep(10)
            continue
    soap = BeautifulSoup(response,from_encoding='utf-8')
    pt1=soap.findAll('div',class_='pt1')
    if len(pt1)==0 :
        pt1=''
    else:
        pt1=parsePt(pt1[0])
    pt2 = soap.findAll('div', class_='pt2')
    if len(pt2) == 0:
        pt2 = ''
    else:
        pt2 = parsePt2(pt2[0])
    updateProblem(id,str(pt1),str(pt2))

def insertCatelog(title1, title2, pk, max_pi):
    cur.execute('insert into catelog(title1,title2,pk,max_pi) values (%s,%s,%s,%s)', [title1, title2, pk, max_pi])
    return


def insertProblem(catelogid, url):
    cur.execute('insert into problem(catelogid,url) values(%s,%s)', [catelogid, url])
    return

def updateProblem(problemid,pt1,pt2):
    cur.execute('update problem set pt1 =%s,pt2 =%s where id = %s',[pt1,pt2,problemid])
    return

def updateCatelog(id):
    cur.execute('update catelog set is_done = %s where id =%s',[1,id])
    return


db = MySQLdb.connect("172.18.129.21", "lzw", "sustclzw", "jingyou", charset="utf8")
cur = db.cursor()


# with open('/home/anthony/Desktop/jingyou2.html','r')as f:
#     html=f.read()
# soap=BeautifulSoup(html,from_encoding='utf-8')
# root=soap.findAll('div',id="divTree")[0]
# collapsables=root.findAll('li',class_="collapsable")
# for tip_a in collapsables:
#     lis=tip_a.findAll('a')
#     title1=lis[0]['title']
#     for li in lis[1:]:
#         title2=li['title']
#         pk=li['pk']
#         resps=openURl(pk,1)
#         soap2=BeautifulSoup(resps,from_encoding='utf-8')
#         max_pis=soap2.findAll('a',class_='last')
#         if(len(max_pis)>0):
#             max_pi=max_pis[0]['href']
#             max_pi=max_pi[max_pi.find('(')+1:max_pi.find(',')]
#         else:
#             max_pi=1
#         print title1,title2,pk,max_pi
#         insertCatelog(title1,title2,pk,max_pi)


# cur.execute('select* from catelog')
# allCatalog = cur.fetchall()
# for row in allCatalog:
#     max_pin = row[4]
#     findProblemSpwans = []
#     for pi in range(1, max_pin+1):
#         findProblemSpwans.append(gevent.spawn(findProblemUrl, row[0], row[3], pi))
#     gevent.joinall(findProblemSpwans)
#     db.commit()
#     print row[0],'done'

cur.execute('select id,url from problem where pt1 is null')
allproblem = cur.fetchall()
problen =len(allproblem)
for i in range(problen /100):
    problemSpawns=[]
    for row in allproblem[i*100:(i+1)*100]:
        id=row[0]
        url=row[1]
        problemSpawns.append(gevent.spawn(findProblemContent,id,url))
    gevent.joinall(problemSpawns)
    print i * 100000 / problen, 'done'
    db.commit()

db.commit()
cur.close()
db.close()