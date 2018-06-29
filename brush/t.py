# -*- coding:utf-8 -*-
import re


proxy = "123.45.45.52:8080"
html = u'\u9605\u8bfb\u6570\uff1a214'
all = re.findall(r'(\d+)',html)
readNumber = all[0].encode('unicode-escape').decode('string_escape')
# print(type(readNumber))

myCookies = dict(UserInfo='TBJy4EC1o570hzB28nK%2FKb6FXqQzY9RTAZnWSXtXKLgG67twnPVEV%2B%2Fer4AIiXDhZp4nBrsBC%2B6KDbxNu0cuoTUYOCkCP%2BqnoupS%2B7G2GvCczZE09qrlxtQjWob%2FZK9L%2BAOj%2FOM4eJ%2FcacZ2O4hxdQ%3D%3D123')
print(myCookies)