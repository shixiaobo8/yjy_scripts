#!/usr/bin/env python
# -*- coding:utf8 -*-
import MySQLdb as mdb
import os,sys,datetime,commands

class updateDbTool:
# 构造器
	def __init__(self,dbname):
		self.dbname = dbname
		try:
			self.sandbox_conn = mdb.connect('localhost',user='root',passwd='abcxxx123',db=dbname,unix_socket='/tmp/mysql.sock')
			self.sandbox_cursor = self.sandbox_conn.cursor()
			self.online_conn = mdb.connect('10.24.203.239',user='root',passwd='abcxxx123',db=dbname,unix_socket='/tmp/mysql.sock')
			self.online_cursor = self.online_conn.cursor()
		except mdb.Error,e:
			print e

# 析构器
	def __del__(self):
		self.sanbox_conn.close()
		self.online_conn.close()
		
# 数据检查方法
	def get_mysql_data(self,cursor):
		"""
		cursor: 传入一个数据库游标
		"""
		data = ''
		try:
			sql = 'select * from yjy_im_chat_aes;'
			cursor.execute(sql)
			data = cursor.fetchall()
			self.sandbox_conn.commit()
			self.online_conn.commit()
		except mdb.Error,e:
			print "请出入正确的数据库信息",e
		return data


# 同步线上的最新数据到沙盒数据库
	def rsync_mysql_data(self,sandbox_data,online_data):
		sandbox_data = self.get_mysql_data(self.sandbox_cursor)
		print sandbox_data
		online_data = self.get_mysql_data(self.online_cursor)
		print online_data
		# 测试数据的不一致性
		#for i in range(0,len(sandbox_data)):
		#	if sandbox_data[i] != online_data[i]:
		#		print sandbox_data[i]
		#		print '\n'
		#		print online_data[i]
				#sys.exit(1)
		try:
			cmd = 'mysqldump -h 10.24.203.239 -uroot -pabcxxx123 --default-character-set=utf8 '+self.dbname + ' yjy_im_chat_aes' +' > /root/' + self.dbname + '_aes.sql'
			print cmd
			print commands.getstatusoutput(cmd)
			cmd1 = 'mysql -uroot -pabcxxx123 --default-character-set=utf8 ' + self.dbname + ' < /root/' + self.dbname + '_aes.sql'
			print cmd1
			print commands.getstatusoutput(cmd1)
			cmd2 = 'mysqldump -h 10.24.203.239 -uroot -pabcxxx123 --default-character-set=utf8 '+self.dbname + ' yjy_im_chat ' +' > /root/' + self.dbname + '_notaes.sql'
			print cmd2
			print commands.getstatusoutput(cmd2)
			cmd3 = 'mysql -uroot -pabcxxx123 --default-character-set=utf8 ' + self.dbname + ' < /root/' + self.dbname + '_notaes.sql'
			print cmd3
			print commands.getstatusoutput(cmd3)
			print "数据同步完成"
			self.get_diff()
		except Exception,e:
			print "数据存在不明确的完整性错误!!请手动检查"

# 数据比较和处理方法
	def get_diff(self):
		sandbox_data = self.get_mysql_data(self.sandbox_cursor)
		online_data = self.get_mysql_data(self.online_cursor)
		# 测试数据的不一致性
		#for i in range(0,len(sandbox_data)):
		#	if sandbox_data[i] != online_data[i]:
		#		print sandbox_data[i]
		#		print '\n'
		#		print online_data[i]
		if sandbox_data == online_data:
			print "恭喜,数据库信息一致！！不需要同步"
		elif len(sandbox_data) > len(online_data):
			print "检测到预上线的新数据,即将开始同步到线上"
			self.update_to_online()
		elif len(sandbox_data) < len(online_data):
			print "检测到沙盒数据不完整,即将开始同步到沙盒"
			print "即将重新从新上数据库同步数据！！"
			self.rsync_mysql_data(sandbox_data,online_data)
		else:
			print "数据存在不明确的完整性错误!!请手动检查"
			sys.exit(1)

# 同步sandbox的最新数据到online数据库
	def update_to_online(self):
		sandbox_data = self.get_mysql_data(self.sandbox_cursor)
		online_data = self.get_mysql_data(self.online_cursor)
		try:
			cmd = 'mysqldump -uroot -pabcxxx123 --default-character-set=utf8 '+self.dbname + ' yjy_im_chat_aes ' + ' > /root/toonline' + self.dbname + '_aes.sql'
			print cmd
			print commands.getstatusoutput(cmd)
			cmd1 = 'mysql -uroot -pabcxxx123 -h 10.24.203.239 --default-character-set=utf8 ' + self.dbname + ' < /root/toonline' + self.dbname + '_aes.sql'
			print cmd1
			print commands.getstatusoutput(cmd1)
			cmd2 = 'mysqldump -uroot -pabcxxx123 --default-character-set=utf8 '+self.dbname + ' yjy_im_chat ' + ' > /root/toonline' + self.dbname + '_notaes.sql'
			print cmd2
			print commands.getstatusoutput(cmd2)
			cmd3 = 'mysql -uroot -pabcxxx123 -h 10.24.203.239 --default-character-set=utf8 ' + self.dbname + ' < /root/toonline' + self.dbname + '_notaes.sql'
			print cmd3
			print commands.getstatusoutput(cmd3)
			print "恭喜,数据同步完成"
			self.get_diff()
		except Exception,e:
			print "同步出错!",e
		

if __name__ == '__main__':
	dbt = updateDbTool('yjy_xiyizhiyeyishi')
	dbt.get_diff()
