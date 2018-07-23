#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
爬wanimal1983的图片
'''



import os, re, requests
from pyquery import PyQuery as pq

def mkDir(path):
	if not os.path.exists(path):
		os.mkdir(path)
	return path

def getMonth(char):
	if char == "Jan":
		return "01"
	elif char == "Feb":
		return "02"
	elif char == "Mar":
		return "03"
	elif char == "Apr":
		return "04"
	elif char == "May":
		return "05"
	elif char == "Jun":
		return "06"
	elif char == "Jul":
		return "07"
	elif char == "Aug":
		return "08"
	elif char == "Sep":
		return "09"
	elif char == "Oct":
		return "10"
	elif char == "Nov":
		return "11"
	elif char == "Dec":
		return "12"
	return char

def getDay(char):
	match = re.compile('\d+').match(char)
	if(match):
		day = (int)(match.group())
		if day < 10:
			return "0%d" % day
		else:
			return day
	return char

def startToDownloadImages(htmlSource):
	d = pq(htmlSource)
	# print(d('autopagerize_page_element .post'))
	# 提取时间

	q = 0
	for post in d('.autopagerize_page_element .post').items():
	# for post in d('.autopagerize_page_element .post').items():
		q +=1
		print('fuck you',q)

		dateList = []
		date = post('.post-foot .datenotes a')
		arr = date.text().split(' ')
				# 时间格式是以空格隔开的，比如：30th Jan 2013
		print(arr	)
		if arr !=['']:dateList.append("%s-%s-%s" % (arr[2], getMonth(arr[1]), getDay(arr[0])))
		# 提取图片url
		index = 0
		post = pq(post)
		v = str(post('.photo-posts .photo-sets .photoset-grid'))
		v = v.split(';')
		for i in v:
			img_url = re.findall('https://[^\s]*?1280\.jpg', i, re.S)
			if img_url:
				img_url=img_url[0]
				print(img_url)
				path = "images/%s" % dateList[index]
				mkDir(path)
				# 开始下载图片
				imgPath = "%s/%s" % (path, img_url.split('/')[-1])
				if os.path.exists(imgPath):
					print(u"跳过已存在图片:%s" % imgPath)
					continue

				print(u"开始下载图片:%s" % img_url)
				try:
					r = requests.get(img_url, stream=True)
				except Exception as e:
					print(e)
					continue
				with open(imgPath, 'wb') as f:
					for chunk in r.iter_content(chunk_size=1024):
						if chunk:
							f.write(chunk)
							f.flush()
		ww = str(post('.photo-posts .media'))
		ww = ww.split(';')
		for img in ww:
			img_url = re.findall('https://[^\s]*?1280\.jpg', img, re.S)
			if img_url:
				img_url = img_url[0]
				print(img_url)
				path = "images/%s" % dateList[index]
				mkDir(path)
			# 开始下载图片
				imgPath = "%s/%s" % (path, img_url.split('/')[-1])
				if os.path.exists(imgPath):
					print(u"跳过已存在图片:%s" % imgPath)
					continue
				print(u"开始下载图片:%s" % img_url)
				try:
					r = requests.get(img_url, stream=True)
				except Exception as e:
					print(e)
					continue
				with open(imgPath, 'wb') as f:
					for chunk in r.iter_content(chunk_size=1024):
						if chunk:
							f.write(chunk)
							f.flush()
		# 判断下是否还有下一页
	if d('#next'):
		return True
	return False

def fetch(pageNum, cookies = None):
	url = "http://wanimal1983.tumblr.com/page/%s" % pageNum
	print(u"开始访问%s" % url)
	
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
	response = requests.get(url, headers = headers, cookies = cookies)
	if response.status_code == 200:
		return startToDownloadImages(response.text)
	# if response.status_code == 500:
		
	print(u"访问%s错误:%d" % (url, response.status_code))
	return False

if __name__ == '__main__':
	mkDir("images")
	page = 1
	while True:
		if fetch(page):
			page += 1
		else:
			break
	print(u"结束")
