#! /usr/bin/env python
# -*- coding:utf-8 -*-
# 导入指定数据
import requests
import re,time
import os,sys,xlrd
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')
db_conn = mdb.connect('localhost','root','abcxxx123','yjy_xiyizonghe',unix_socket='/tmp/mysql.sock')
cursor = db_conn.cursor()
db_conn.set_character_set('utf8')
# 读取excel
data = xlrd.open_workbook("/root/scripts/passport.xls")
# 获取sheet名称
table_name = 'yjy_user_1'
table = data.sheet_by_name(u''+table_name)
#tables = data.sheets()
#for table in tables:
#	print table
# 读取行数,列数
nrows = table.nrows
print "一共有行数:",nrows
ncols = table.ncols
print "一共有列数:",ncols
time.sleep(3)
print "开始导入数据"
columns = table.row_values(0)
sql = "insert into " + table_name + "("
# 获取字段名称
for j in range(0,ncols):
	sql += table.cell(0,j).value + ","
sql = sql[:-1]
sql += ") values("
sqls = []
# 单元格数据
for i in range(1,nrows):
	sql1 = sql
	rows_values = table.row_values(i)
	for row in rows_values:
		#print type(row)
		if type(row) is float:
			row = int(row)
			sql1 += str(row) + ","
		elif type(row) == unicode:
			sql1 += "'" + row + "'" + ","
	sql1 = sql1[:-1]
	sql1 += ");"
	sqls.append(sql1)

# 写入数据库
for sql in sqls:
	try:
		print sql
		cursor.execute(sql)
		data = cursor.fetchall()
		db_conn.commit()
	except mdb.Error, e:
		print e
