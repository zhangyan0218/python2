# -*- coding:utf-8 -*-
import re
import random
import time
import logging
from Logger import Logger
import sys
import requests
from contextlib import closing

reload(sys)
sys.setdefaultencoding('utf-8')

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
blog_id_list = []
errorNumber = 0
successNumber = 0
log_success = Logger(logName='brushLogger_success', logLevel=logging.DEBUG,
					 logFilePath='log/brush_success.log').getlog()
log_fail = Logger(logName='brushLogger_fail', logLevel=logging.DEBUG, logFilePath='log/brush_fail.log').getlog()
log_html = Logger(logName='brushLogger_html', logLevel=logging.DEBUG, logFilePath='log/brush_html.log').getlog()

'''
获取国内高匿IP:PORT
'''
def get_proxy_ip():
	global proxy_list
	lines = open('assets/ip.txt', 'r').readlines()
	for line in lines:
		proxy = line.strip('\n')
		proxy_list.append(proxy)


''' 获取指定的文章id '''
def get_blog_id_list():
	global blog_id_list
	lines = open('assets/blog_id.txt', 'r').readlines()
	for line in lines:
		blog_id_list.append(line.strip('\n'))


''' 根据指定的url去爬 '''
def brush(url):
	global errorNumber, successNumber
	url = blog_url_pre + url
	currentIp = random.choice(proxy_list)

	headers = getHeaders(currentIp[0:currentIp.index(":")])
	myCookies = dict(
		UserInfo='TBJy4EC1o570hzB28nK%2FKb6FXqQzY9RTAZnWSXtXKLgG67twnPVEV%2B%2Fer4AIiXDhZp4nBrsBC%2B6KDbxNu0cuoTUYOCkCP%2BqnoupS%2B7G2GvCczZE09qrlxtQjWob%2FZK9L%2BAOj%2FOM4eJ%2FcacZ2O4hxdQ%3D%3D123')

	# req = requests.get(url, headers=headers, proxies={'HTTPS': currentIp})
	# req = requests.get('http://www.baidu.com',headers=headers)

	with closing(requests.get(url, cookies=myCookies)) as req:
		html = ""
		try:
			html = req.text
		except Exception as e:
			errorNumber += 1
			log_fail.error((' error! %s' % (errorNumber), e, url))
		else:
			successNumber += 1
			' 获取readCount的span内容'
			readNumberSpan = re.findall(r'<span class="read-count">(.+)</span>', html)
			' unicode-->str '
			readNumber = re.findall(r'(\d+)', readNumberSpan[0])[0].encode('unicode-escape').decode('string_escape')
			if len(readNumber) > 0:
				log_success.debug(
					('success! %s' % (++successNumber), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
					 , url,'阅读数：', readNumber))
			else:
				log_success.debug(
					('success! %s' % (++successNumber), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
					 , url))
		if not html.strip():
			log_html.debug(html)


'给request添加Header头'
def getHeaders(proxy_ip):
	header = {
		"User-Agent": random.choice(user_agent_list)
		, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		, "Accept-Encoding": "gzip, deflate"
		, "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"
		, "Connection": "keep-alive"
		# , "X-Forwarded-For": proxy_ip
		, "Content-Length": "31"
		, "Content-Type": "application/x-www-form-urlencoded"
		# , "Referer", "https://blog.csdn.net"
	}
	return header


if __name__ == "__main__":
	get_proxy_ip()
	get_blog_id_list()

	while 1:
		for blog_id in blog_id_list:
			try:
				brush(blog_id)
			except Exception as e:
				log_fail.error(e)
				time.sleep(random.randint(30,60))
			time.sleep(random.randint(1,3))
		time.sleep(random.randint(30,35))