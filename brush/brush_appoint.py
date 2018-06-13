# -*- coding:utf-8 -*-
import re
import urllib2
import random
import threading
import time
import ssl
import logging
from Logger import Logger
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import socket
socket.setdefaulttimeout(10)

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
blog_url_pre = "https://blog.csdn.net/zy_281870667/article/details/"
proxy_list = []
proxy_ip = []
blog_id_list = []
errorNumber = 0
successNumber = 0
log_success = Logger(logName='brushLogger_success',logLevel=logging.DEBUG,logFilePath='log/brush_success.log').getlog()
log_fail = Logger(logName='brushLogger_fail',logLevel=logging.DEBUG,logFilePath='log/brush_fail.log').getlog()
log_html = Logger(logName='brushLogger_html',logLevel=logging.DEBUG,logFilePath='log/brush_html.log').getlog()

'''
获取国内高匿IP:PORT
'''
def get_proxy_ip():
	global proxy_list
	global proxy_ip
	lines = open('ip.txt', 'r').readlines()
	for line in lines:
		proxy = line.strip('\n')
		proxy_list.append(proxy)
		proxy_ip.append(proxy[0:proxy.index(":")])

''' 获取指定的文章id '''
def get_blog_id_list():
	global blog_id_list
	lines = open('blog_id.txt', 'r').readlines()
	for line in lines:
		blog_id_list.append(line.strip('\n'))


''' 根据指定的url去爬 '''
def brush(url):
	global errorNumber, successNumber
	proxy_ip = random.choice(proxy_list)

	proxy_support = urllib2.ProxyHandler({'https': proxy_ip})
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)

	req = urllib2.Request(blog_url_pre + url)
	req = addHeader(req)

	context = ssl._create_unverified_context()
	html = ""
	try:
		response = urllib2.urlopen(req, timeout=10, context=context)
		html = response.read().decode('UTF-8')
	except Exception as e:
		errorNumber += 1
		log_fail.error((' error! %s' % (errorNumber), e, url))
	else:
		successNumber += 1
		readNumber = re.findall(r'<span class="read-count">\W+：(\d+)</span>', html)
		if len(readNumber) > 0:
			log_success.debug(
				('success! %s' % (++successNumber), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				 , url, '访问量：' ,readNumber[0]))
		else:
			log_success.debug(
				('success! %s' % (++successNumber), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				 , url))
	if not html.strip():
		log_html.debug(html)
	# sem.release()

'给request添加Header头'
def addHeader(req):
	req.add_header("User-Agent", random.choice(user_agent_list))
	req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.add_header("Accept-Encoding", "gzip, deflate")
	req.add_header("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3")
	req.add_header("Connection", "keep-alive")
	req.add_header("X-Forwarded-For", random.choice(proxy_ip))
	req.add_header("Content-Length", "31")
	req.add_header("Content-Type", "application/x-www-form-urlencoded")
	return req

if __name__ == "__main__":
	get_proxy_ip()
	get_blog_id_list()

	while 1:
		for blog_id in blog_id_list:
			brush(blog_id)

if __name__ == "__main2__":
	get_proxy_ip()
	get_blog_id_list()

	sem = threading.BoundedSemaphore(1)
	while 1:
		for blog_id in blog_id_list:
			sem.acquire()
			T = threading.Thread(target=brush, args=(blog_id,))
			T.start()
			time.sleep(random.randint(5, 10))
