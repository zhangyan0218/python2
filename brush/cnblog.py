# coding=utf-8
import urllib2
import re
import sys
import time
import threading
import request
import random

l = []
iparray = []

global totalnum
totalnum = 0

global proxy_list
proxy_list = []

global count
count = 0

totalblog = 0
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


def Get_proxy_ip():
	global proxy_list
	global totalnum
	proxy_list = []

	headers = {
		'Host': 'www.xicidaili.com',
		'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
		'Accept': r'application/json, text/javascript, */*; q=0.01',
		'Referer': r'http://www.xicidaili.com/',
	}
	req = urllib2.Request(r'http://www.xicidaili.com/nn/', headers=headers)
	response = urllib2.urlopen(req)
	html = response.read().decode('utf-8')

	ip_list = re.findall(r'\d+\.\d+\.\d+\.\d+', html)
	port_list = re.findall(r'<td>\d+</td>', html)
	for i in range(len(ip_list)):
		totalnum += 1
		ip = ip_list[i]
		port = re.sub(r'<td>|</td>', '', port_list[i])
		proxy = '%s:%s' % (ip, port)
		proxy_list.append(proxy)

	headers = {
		'Host': 'www.xicidaili.com',
		'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
		'Accept': r'application/json, text/javascript, */*; q=0.01',
		'Referer': r'http://www.xicidaili.com/',
	}
	req = urllib2.Request(r'http://www.xicidaili.com/nn/5', headers=headers)
	response = urllib2.urlopen(req)
	html = response.read().decode('utf-8')
	ip_list = re.findall(r'\d+\.\d+\.\d+\.\d+', html)
	port_list = re.findall(r'<td>\d+</td>', html)
	for i in range(len(ip_list)):
		totalnum += 1
		ip = ip_list[i]
		port = re.sub(r'<td>|</td>', '', port_list[i])
		proxy = '%s:%s' % (ip, port)
		proxy_list.append(proxy)

	return proxy_list


def main():
	list1 = []
	list2 = []
	global l
	global totalblog
	global ip_list
	pr = r'href="http://www.cnblogs.com/zpfbuaa/p/(\d+)'
	rr = re.compile(pr)
	yeurl = ['http://www.cnblogs.com/zpfbuaa/p/?page=1', 'http://www.cnblogs.com/zpfbuaa/p/?page=2',
			 'http://www.cnblogs.com/zpfbuaa/p/?page=3']
	for i in yeurl:
		req = urllib2.Request(i)

		# proxy_ip = random.choice(proxyIP.proxy_list)  # 在proxy_list中随机取一个ip
		# print proxy_ip
		# proxy_support = urllib2.ProxyHandler(proxy_ip)
		# opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)

		req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
		cn = urllib2.urlopen(req)
		f = cn.read()
		list2 = re.findall(rr, f)
		list1 = list1 + list2
		cn.close()
	for o in list1:
		totalblog = totalblog + 1
		url = 'http://www.cnblogs.com/zpfbuaa/p/' + o + ".html"
		l.append(url)
	Get_proxy_ip()
	print totalnum


def su(url):
	proxy_ip = random.choice(proxy_list)
	user_agent = random.choice(user_agent_list)
	print proxy_ip
	print user_agent

	proxy_support = urllib2.ProxyHandler({'http': proxy_ip})
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)

	req = urllib2.Request(url)
	req.add_header("User-Agent", user_agent)

	try:
		c = urllib2.urlopen(req, timeout=3)
	except Exception as e:
		print('******打开失败！******')
	else:
		global count
		count += 1
		print('OK!总计成功%s次！' % count)
		print "当前刷的网址为"
		print url
	sem.release()


if __name__ == "__main__":
	main()
	print "开始刷访问量！"
	print "共计博客个数为 "
	print totalblog
	maxThread = 5
	sem = threading.BoundedSemaphore(maxThread)
	while 1:
		for i in l:
			sem.acquire()
			T = threading.Thread(target=su, args=(i,))
			T.start()
