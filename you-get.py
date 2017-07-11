#! /usr/bin/env python
# -*- coding:gbk -*-
"""
	you-get 爬虫脚本简单demo抓取yaf视频教程
	create table www_widuu_com (id int(11) not null auto_increment, video_url varchar(255) collate utf8_bin not null,primary key (id)) 
	ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;
	Ê¹ÓÃyou-get(»ùÓÚpython3.5¿ª·¢)ÅÀÈ¡Ä³¸öit½ÌÑ§ÊÓÆµÍøÕ¾ÉÏµÄÊÓÆµ
"""
import re,sys,os,requests
import pymysql.cursors
import pymysql as mdb

#reload(sys)
#sys.setdefaultencoding('utf-8')
storage_path='d:/video'
urls=[]
base_url="http://www.widuu.com/archives/"
html_contents=[]
table_name=base_url.split("/")[2].replace('.','_')
db_name="climb_data"
conn=mdb.connect( host='localhost',
                  user='root',
                  password='123456',
                  db=db_name,
                  charset='utf8mb4',
                  cursorclass=pymysql.cursors.DictCursor)

#re.compile('src=""')
for j in range(1,20):
	for i in range(1,1001):
		url = base_url + str(j) +"/"+str(i)+".html"
		print(url)
		req = requests.get(url)
		print(req)
		if req.status_code == 200:
			html_content = str(req.content)
			#if re.match("flashvars",html_content):
			if html_content.find("flashvars") != -1:
				html_contents.append(html_content)
				urls.append(url)
				os.chdir(storage_path)
				os.system("you-get " + url)
				#print(html_content)
print(urls)
print(len(html_contents))
