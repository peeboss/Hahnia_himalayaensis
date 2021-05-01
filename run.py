import requests
import os
import re
from bs4 import BeautifulSoup
#设置请求头
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49'}
#设置本地存储地址
localdir=r'E:\himalaya'
# 从所有网页上获取播放链接
def getlinks(url):
	global localdir
	rep =  	requests.get(url,headers=headers)
	bs =   	BeautifulSoup(rep.text,'html.parser')
	links =	bs.select('div.sound-list._is > ul > li a')
	# 根据音频名字创建目录
	localdir =	os.path.join(localdir,bs.select('h1')[0].text)
	if not os.path.exists(localdir):
		os.makedirs(localdir)
	#从<class=sound-list is>中读取<a>标签
	pagenums =	bs.select('ul.pagination-page.WJ_ a')
	if(pagenums!=[]):
		for index in range(2,int(pagenums[-2].text)+1):
			rep =   requests.get(url+'/p'+str(index),headers=headers)
			bs =   	BeautifulSoup(rep.text,'html.parser')
			links =	links + (bs.select('div.sound-list._is > ul > li a'))
	return links
# 根据播放链接里的id值使用网站的api解析出下载链接
def parse(url):
	rep =	requests.get(url,headers=headers)
	json =	rep.json()
	print(json['data']['src'])
	return json['data']['src']
#下载到本地
def download(links):
	for link in links:
		#正则表达式从超链接中读出音频id号
		#例如/renwen/15158548/207024308中的207024308
		print('chapter :'+link['title'])
		filename =	os.path.join(localdir,link['title']+'.m4a')
		if not os.path.isfile(filename):
			#使用解析的出的链接下载到本地
			resource =	parse('https://www.ximalaya.com/revision/play/v1/audio?id='+re.match(r'/(\w+)/(\d+)/(\d+)',link['href'])[3]+'&ptype=1')
			rep =	requests.get(resource,headers=headers)
			file =	open(filename,'wb')
			file.write(rep.content)
			file.close()
		else:
			print(filename+' is exists!')

if __name__ ==  '__main__':
	url =	input('请输入页面链接:')
	urls =	getlinks(url)
	# print(urls)
	download(urls)
