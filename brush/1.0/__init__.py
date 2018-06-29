# -*- coding:utf-8 -*-
import re
import urllib2
import random
import threading
import time
import ssl

user_agent_list = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
	'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
	'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]

proxy_list =[]
all_article_url = []
totalblog = 0
errorNumber = 0
successNumber = 0

'''
获取国内高匿IP:PORT
'''
def get_proxy_ip():
	global proxy_list
	lines = open('ip.txt', 'r').readlines()
	for line in lines:
		proxy_list.append(line.strip('\n'))


'''
获取https://blog.csdn.net/zy_281870667/article/list/博客的列表数量，多少页
'''
def get_max_pageNumber():
	csdn_url = 'https://blog.csdn.net/zy_281870667/article/list/'
	req = urllib2.Request(csdn_url)
	resppnse = urllib2.urlopen(req)
	html = resppnse.read().decode('UTF-8')

	# html = open('csdn.html','r').read()
	all_page = re.findall(r'listTotal = \d+', html)
	article_number = 0
	if all_page:
		t = all_page[0]
		index = t.find('= ')
		article_number = int(t[index + 2:])
	return (article_number - 1) / 20 + 1


''' 获取所有的文章链接 '''
def get_all_article():
	global totalblog,all_article_url
	article_reg = re.compile(r'data-articleid="(\d+)"')

	max_pageNumber = get_max_pageNumber()
	''' 获取指定页码下的所有文章ID '''
	for i in range(max_pageNumber):
		req = urllib2.Request('https://blog.csdn.net/zy_281870667/article/list/%s' % (i + 1))
		req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
		content = urllib2.urlopen(req)
		html = content.read().decode('utf-8')
		page_articles = re.findall(article_reg, html)
		if len(page_articles) > 0:
			''' 所有文章id '''
			for o in page_articles:
				totalblog += 1
				url = 'https://blog.csdn.net/zy_281870667/article/details/%s' % (o)
				all_article_url.append(url)
		content.close()


''' 根据指定的url去爬 '''
def brush(url):
	global errorNumber,successNumber
	proxy_ip = random.choice(proxy_list)
	user_agent = random.choice(user_agent_list)
	# print('proxy_ip:%s,user_agent:%s'%(proxy_ip,user_agent))

	proxy_support = urllib2.ProxyHandler({'https': proxy_ip})
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)

	req = urllib2.Request(url)
	req.add_header("User-Agent", user_agent)

	context = ssl._create_unverified_context()
	try:
		c = urllib2.urlopen(req, timeout=3,context=context)
	except Exception as e:
		errorNumber += 1
		if errorNumber % 30 == 0 :
			print(' error! %s' % (errorNumber), e)
	else:
		successNumber +=1
		if successNumber % 100 == 0 :
			print('success! %s' % (++successNumber), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	sem.release()


if __name__ == "__main__":
	get_proxy_ip()
	get_all_article()
	print "开始刷访问量！"
	print "共计博客个数为 "
	print(totalblog)
	sem = threading.BoundedSemaphore(1)
	while 1:
		randomUrl = random.choice(all_article_url)
		sem.acquire()
		T = threading.Thread(target=brush, args=(randomUrl,))
		T.start()