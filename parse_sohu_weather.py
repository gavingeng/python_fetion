#!/usr/bin/env python
#coding:utf-8
#filename:parse_sohu_weather.py

'''
author:	gavingeng
date:	2012-04-15 17:13:17 
m.sohu.com的天气获取只有当天的天气比较详细，后两天的就比较简单，并未做抓取，现在在找其他的天气，cntv/fetion的天气都不错
http://wap.sohu.com/weather 这个各地天气没找到规律，由于有其他的比较好的，这里就不做解析了（这个天气直接去网页，很好取）
'''

import os,sys
from BeautifulSoup import BeautifulSoup
import time
import urllib2,urllib
import traceback,re

ISOTIMEFORMAT='%Y-%m-%d %H:%M:%S'
mobile='13512345678,13812345678,13412345678'

def get_time():
	t=time.strftime(ISOTIMEFORMAT,time.localtime())
	return t

def generate_sohu_url(location):
	v=urllib.quote(location)
	#print v
	url='http://m.sohu.com/weather/?city=' + v
	return url

def parse_sohu(city):
	result=""
	#url=generate_sohu_url('北京')
	url=generate_sohu_url(city)
	print url

	request=urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0) Gecko/20count101 Firefox/10.0')
	try:
		ff=urllib2.urlopen(request)
		if ff.getcode() == 200:
			res=''.join(ff.read()).decode('utf-8','ignore')
			#print res
			soup = BeautifulSoup(res)
	#		print soup.originalEncoding
			info=soup.findAll(id=re.compile('info'))
			#info=soup.findAll(attrs = {'class':'info'})[0].findAll("info")
			#天气情况：晴 多云 etc
			info=soup.findAll('div',{'class':'info'})
			info='%s' %info
			p=re.compile('<[^>]+>')
			info=str(p.sub("",info))
			#info=unicode(str(info),'gbk')
			info=unicode(str(info),'utf-8')
			info=info.encode('utf-8')
			#print info

			number=soup.findAll('div',{'class':'number'})
			number='%s' %number
			number=p.sub("",number)
			number=unicode(str(number),'utf-8')
			number=number.encode('utf-8')
			
			list=soup.findAll("ul")[0].findAll('li')
			contents=""
			for l in list:
				x=unicode(str(l.next),'utf-8')
				contents=unicode(str(contents),'utf-8')
				contents=contents.encode('utf-8')
				contents = contents + x.encode('utf-8') + " "

			result=str(get_time()) + str(info) + str(number) + str(contents)
	except Exception,e:
		print traceback.print_exc()

	return result

def usage():
	print "./parse_sohu_weather.py $city"
	print "example: /parse_sohu_weather.py 北京"

def main():
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)
	city = sys.argv[1]	
	result = parse_sohu(city)
	print result

if __name__=='__main__':
	main()
