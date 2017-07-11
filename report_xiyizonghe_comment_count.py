#!/usr/bin/env python
# -*- coding:utf8 -*-
# 导出指定时间内评论计数到excel
import xlrd,os,sys,xlwt
import time
import MySQLdb as mdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class oldData(object):
	
	def __init__(self,xls_name):
		try:
			self.xls_name = xls_name
			data = xlrd.open_workbook('/tmp/demo.xls')
			table = data.sheets()[0]
			self.titles = table.row_values(0)
			# 文章id
			self.ids = table.col_values(0)[1:]
			# 作者id
			self.author_ids = table.col_values(1)[1:]
			# 文章标题
			self.titiles = table.col_values(2)[1:]
			# 评论总数(不包含作者)
			self.comment_counts = table.col_values(3)[1:]
			# 通过文章id 设置count
			self.old_comment_counts = dict()
			self.row_datas = [ table.row_values(i) for i in range(table.nrows) ]
			for i in range(0,table.nrows):
				#print table.row_values(i)
				self.old_comment_counts[table.row_values(i)[0]] = dict()
				self.old_comment_counts[table.row_values(i)[0]] = table.row_values(i)[3]
		except Exception,e:
			print e

	# 获取指定数据的数据
	# 时间格式2017-05-10 00:00:00
	def getData(self,start_id,start_date,end_date):
		start_date_stamp = time.mktime(time.strptime(start_date,"%Y-%m-%d %H:%M:%S"))
		end_date_stamp = time.mktime(time.strptime(end_date,"%Y-%m-%d %H:%M:%S"))
		try:
			db_conn = mdb.connect('localhost','root','abcxxx123','recite')
			cursor = db_conn.cursor()
			sql = 'select `id`,`author_id`,`title`,`comment_count` from yjy_xiyizonghe_1861_article_attr'
			cursor.execute(sql)
			data1 = cursor.fetchall()
			tmp_data1 = [ list(d) for d in list(data1) ]
			db_conn.commit()
			for i in range(0,len(tmp_data1)):
				author_id = tmp_data1[i][1]
				id = tmp_data1[i][0]
				articlet_id = id
				sql1 = 'select count(distinct user_id) from yjy_xiyizonghe_1861_articlet_comment where articlet_id='+ str(articlet_id) + ' and user_id!= ' + str(author_id) +' and ctime > ' + str(start_date_stamp) + ' and ctime < ' + str(end_date_stamp)
				cursor.execute(sql1)
				count = cursor.fetchall()
				db_conn.commit()
				tmp_data1[i][3] = count
			f = xlwt.Workbook()
			sheetname = start_date[0:10].replace('-','') + '-' + end_date[0:10].replace('-','')
			# 创建表单1
			newsheet1 = f.add_sheet(sheetname,cell_overwrite_ok=True)
			# 开始写入标题到sheet1
			for i in range(0,len(self.titles)):
				newsheet1.write(0,i,self.titles[i])
			# 开始填充数据到sheet1
			for i in range(1,len(tmp_data1)):
				newsheet1.write(i,0,tmp_data1[i][0])
				newsheet1.write(i,1,tmp_data1[i][1])
				newsheet1.write(i,2,u''+tmp_data1[i][2])
				newsheet1.write(i,3,int(tmp_data1[i][3][0][0]))
			# 开始处理指定数据
			db_conn = mdb.connect('localhost','root','abcxxx123','recite')
			cursor = db_conn.cursor()
			sql2 = 'select `id`,`author_id`,`title`,`comment_count` from yjy_xiyizonghe_1861_article_attr where id > ' + str(start_id)
			cursor.execute(sql2)
			data = cursor.fetchall()
			db_conn.commit()
			tmp_data = [ list(d) for d in list(data) ]
			for i in range(0,len(tmp_data)):
				id = tmp_data[i][0]
				author_id = tmp_data[i][1]
				articlet_id = id
				#sql3 = 'select count(*) from yjy_xiyizonghe_1861_articlet_comment where articlet_id='+ str(articlet_id) +' and ctime > ' + str(start_date_stamp) + ' and ctime < ' + str(end_date_stamp)
				sql3 = 'select count(distinct user_id) from yjy_xiyizonghe_1861_articlet_comment where articlet_id='+ str(articlet_id) + ' and user_id!= ' + str(author_id)
				cursor.execute(sql3)
				count = cursor.fetchall()
				db_conn.commit()
				tmp_data[i][3] = count
			# 创建表单2
			newsheet2 = f.add_sheet(str(start_id + 2)+u'之后的评论数',cell_overwrite_ok=True)
			# 开始写入标题到sheet2
			for i in range(0,len(self.titles)):
				newsheet2.write(0,i,self.titles[i])
			# 开始填充数据到sheet2
			for i in range(1,len(tmp_data)):
				newsheet2.write(i,0,tmp_data[i][0])
				newsheet2.write(i,1,tmp_data[i][1])
				newsheet2.write(i,2,u''+tmp_data[i][2])
				newsheet2.write(i,3,int(tmp_data[i][3][0][0]))
			f.save(self.xls_name)
		except mdb.Error,e:
			print e
		db_conn.close()			

#	def makeNewExcel(self):
#		# 获取最新的表格数据
#		try:
#			db_conn = mdb.connect('localhost','root','abcxxx123','recite')
#			cursor = db_conn.cursor()
#			sql = 'select `id`,`author_id`,`title`,`comment_count` from yjy_xiyizonghe_1861_article_attr'
#			cursor.execute(sql)
#			data = cursor.fetchall()
#			tmp_data = [ list(d) for d in list(data) ]
#			#print len(data)
#			# 开始写入excel表单
#			f = xlwt.Workbook()
#			newsheet = f.add_sheet(u'新数据',cell_overwrite_ok=True)
#			# 处理评论总数
#			for i in range(0,len(tmp_data)):
#				d = list(tmp_data[i])
#				id = d[0]
#				now_count = d[3] 
				#print now_count
#				if self.old_comment_counts.has_key(id):
#					tmp_data[i][3] = now_count - self.old_comment_counts[id] - 1
			#for d in tmp_data:
			#	print d[0],d[3]
			#print self.old_comment_counts[103]
			# 开始写入标题excel
			#for i in range(0,len(self.titles)):
			#	newsheet.write(0,i,self.titles[i])
			#for i in range(1,len(data)):
			#	newsheet.write(0,i,self.titles[i])
			#f.save('/tmp/demo1.xls')
			# 开始写入数据excel
			#for i in range(0,len(data)+1):
			#	newsheet.write()
#		except mdb.Error,e:
#			print e
#		db_conn.close()			
		

if __name__ == '__main__':
	od = oldData('/tmp/new.xls')
	start='2017-06-11 00:00:00'
	end='2017-07-11 00:00:00'
	od.getData(240,start,end)
	#od.makeNewExcel()
	
