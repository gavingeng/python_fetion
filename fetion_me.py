#!/usr/bin/env python
#coding:utf-8
#filename:fetion_me.py

'''
author:	gavingeng
date:	2012-04-29 12:09:15 
'''

import urllib,urllib2,cookielib
import os,sys,datetime,time
import traceback
import re

COOKIEPATH='cookie_me'
LOGIN_URL = 'http://f.10086.cn/im/login/inputpasssubmit1.action'
SEARCH_FRIENDS_URL ='http://f.10086.cn/im/index/searchOtherInfoList.action'
SEND_MSG_URL = 'http://f.10086.cn/im/user/sendMsg.action'
SEND_MSG_ME = 'http://f.10086.cn/im/user/sendMsgToMyselfs.action'
LOGOUT_URL = 'http://f.10086.cn/im/index/logoutsubmit.action'

class Fetion():
	'''
		init fetion
	'''
	def __init__(self,mobile,pwd,loginstatus):
		self.mobile = mobile
		self.pwd = pwd
		self.loginstatus = loginstatus
		self.login = self.login()
		
	def save_cookie():
		cookiejar = cookielib.MozillaCookieJar()
		cookies = urllib2.HTTPCookieProcessor(cookiejar)
		opener = urllib2.build_opener(self.cookies)
	
	'''
		login fetion
	'''
	def login(self):
		
		cookiejar = cookielib.MozillaCookieJar()
		cookies = urllib2.HTTPCookieProcessor(cookiejar)
		opener = urllib2.build_opener(cookies, urllib2.HTTPHandler)
		
		data = {"m":self.mobile,"pass":self.pwd,"loginstatus":self.loginstatus}
		opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
		urllib2.install_opener(opener)

		req = urllib2.Request(LOGIN_URL,urllib.urlencode(data))
		cookiejar.save(COOKIEPATH)
		f = urllib2.urlopen(req)
		if f.getcode() == 200:
			content = f.read()
			#print content ,f.geturl()
		
		#use proxy
		#opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
	
	'''
		send fetion to my friend
	'''
	def send_fetion(self,mobile,message):
		if str(message).strip() == "":
			return false
		if mobile == self.mobile:
			self.to_me(message)
		else:
			uid = self.get_uid(mobile)
			print "uid=",uid
			self.to_uid(uid,message)
	
	def get_uid(self,mobile):
		uid=''	
		params = {'searchText':mobile}
		content = self.process(SEARCH_FRIENDS_URL, params)
		if str(content).strip() != "" :
			pattern='/toinputMsg\.action\?touserid=(\S+)&amp;type=all'
			rule=re.compile(pattern)
			res = rule.findall(content)
			uid=res[0]
		
		return uid

	def to_uid(self,uid,message):
		params = {'touserid':uid,'msg':message}
		self.process(SEND_MSG_URL, params)
		

	def to_me(self,message):
		params = {'msg':message}
		self.process(SEND_MSG_ME, params)
	
	def logout(self):
		req = urllib2.Request(LOGOUT_URL)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0) Gecko/20count101 Firefox/10.0')
		f = urllib2.urlopen(req)
		if f.getcode() == 200:
			content = f.read()
			print content ,f.geturl()
			
	def process(self,url,params):
		try:
			data = urllib.urlencode(params)
			req = urllib2.Request(url, data)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0) Gecko/20count101 Firefox/10.0')
			f = urllib2.urlopen(req)
			if f.getcode() == 200:
				content = f.read()
				print content
			return content
		except Exception,e:
			traceback.print_exc()	

def usage():
	print "./fetion_me.py mobile pwd status location to_mobile"
	print "example: ./fetion_me.py 13501234567 abcdefg 1 北京 13501234567|13501234568|13501234569"
	sys.exit(1)

def main():
	if len(sys.argv) < 5 :
		usage()
	mobile = sys.argv[1]
	password = sys.argv[2]
	status = sys.argv[3]
	location = sys.argv[4]
	to_mobile = sys.argv[5]

	fetion = Fetion(mobile,password,status)
	import parse_sohu_weather
	#msg=parse_sohu_weather.parse_sohu('北京')
	msg=parse_sohu_weather.parse_sohu(location)
	print msg
	
	mobiles = to_mobile.split("|")
	for m in mobiles:
		fetion.send_fetion(m, msg)

	fetion.logout()

if __name__=='__main__':
	main()
