# -*- coding:utf-8 -*-
import logging
import random
import re
import sys
import time
from contextlib import closing
import requests
from Logger import Logger
from selenium import webdriver


reload(sys)
sys.setdefaultencoding('utf-8')

userName = 'zhangyanchuxian@gmail.com'
passWord = 'Qq123456789'
blog_url_pre = "https://blog.csdn.net/zy_281870667/article/details/"
blog_id_list = []
errorNumber = 0
successNumber = 0
log_success = Logger(logName='brushLogger_success', logLevel=logging.DEBUG,
					 logFilePath='log/brush_success.log').getlog()
log_fail = Logger(logName='brushLogger_fail', logLevel=logging.DEBUG, logFilePath='log/brush_fail.log').getlog()
log_html = Logger(logName='brushLogger_html', logLevel=logging.DEBUG, logFilePath='log/brush_html.log').getlog()


''' 获取指定的文章id '''
def get_blog_id_list():
	global blog_id_list
	lines = open('assets/blog_id.txt', 'r').readlines()
	for line in lines:
		blog_id_list.append(line.strip('\n'))


''' 根据指定的url去爬 '''
def brush(url,browser):
	global errorNumber, successNumber

	readNumber = 0
	try:
		readNumber = brush_selenium(blog_url_pre + url, browser)
	except Exception as e:
		errorNumber += 1
		log_fail.error((' error! %s' % (errorNumber), e, url))
	else:
		successNumber += 1
		if (readNumber != None and readNumber >0):
			log_success.debug(
				('success! %s' % (++successNumber), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				 , url,'阅读数：', readNumber))
		else:
			log_success.debug(
				('success! %s' % (++successNumber), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				 , url))
		browser.close()


def brush_selenium(url,browser):
	browser.get(url)

	elem = browser.find_element_by_class_name("login-user__active")
	if None != elem:
		elem.click()
		''' 防止执行太快出现 "element not visible" 异常 '''
		time.sleep(1)
		elem = browser.find_element_by_id("username")
		elem.send_keys(userName)
		elem = browser.find_element_by_id("password")
		elem.send_keys(passWord)
		elem = browser.find_element_by_class_name("logging")
		elem.click()

		time.sleep(1)
		return browser.find_element_by_class_name('read-count').text()

if __name__ == "__main__":
	get_blog_id_list()
	browser = webdriver.Chrome()

	while 1:
		for blog_id in blog_id_list:
			try:
				brush(blog_id,browser)
			except Exception as e:
				log_fail.error(e)
				time.sleep(random.randint(30,60))
				browser.close()
				browser = webdriver.Chrome()