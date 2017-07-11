#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
	将转发器每天的接口访问量入库
"""
import requests
import re,time
import os,sys
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')
db_conn = mdb.connect('localhost','history_data','Yjy@history89','all_web_data_history',unix_socket='/tmp/mysql.sock')
cursor = db_conn.cursor()

data_url = 'http://10.46.174.223:888/yjy_req_status'

def get_data():
	data = requests.get(data_url)
	data.encoding = 'utf-8'
	return data

def make_data():
	# 去除decode编码
	data = get_data().text.encode('utf8').split('\n')
	return data

def save_data():
	data = make_data()
	# 表字段名称列表:
	columns = data[0]
	# 以日期命令创建每日历史数据表
	today = time.strftime('%Y_%m_%d',time.localtime(time.time()))
	table_name = today + "_history_data"
	create_data_sql = "CREATE TABLE if not exists`" + table_name + "` (`id`  int(200) NULL AUTO_INCREMENT,`zone_name` varchar(100) NULL,`key`  varchar(2000) NULL ,`max_active`  varchar(200) NULL ,`max_bw`  varchar(200) NULL ,`traffic`  varchar(200) NULL ,`requests`  varchar(200) NULL ,`active`  varchar(200) NULL ,`bandwidth`  varchar(200) NULL ,PRIMARY KEY (`id`))ENGINE=InnoDB DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
	try:
		cursor.execute(create_data_sql)
		db_conn.commit()
	except mdb.Error, e:
		print e

	# 插入sql值
	try:
		for d in range(1,len(data)):
			every_data = data[d].split('\t')
			insert_sql = "insert into " + table_name + " (`zone_name`,`key`,`max_active`,`max_bw`,`traffic`,`requests`,`active`,`bandwidth`) values " +  every_data.__str__().replace('[','(').replace(']',')')
			print insert_sql
			if len(every_data) == 8:
				cursor.execute(insert_sql)
				db_conn.commit()
			#sys.exit(1)
	except mdb.Error, e:
		print e

if __name__ == '__main__':
	save_data()
	db_conn.close()
