import requests
import os
import re
from bs4 import BeautifulSoup
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49'}
def getlinks(url):
	rep =   requests.get(url,headers=headers)
	bs  =   BeautifulSoup(rep.text,'html.parser')
	sound_list  =   bs.select('div.sound-list._is a')
	#/renwen/15158548/207024308
	for link in sound_list:
		print(re.match(r'/(\w+)/(\d+)/(\d+)',link['href'])[3])
if __name__ ==  '__main__':
    getlinks('https://www.ximalaya.com/renwenjp/15158548/')
    
