#! /usr/bin/env python
# -*- coding:utf8 -*-
import os,sys,time
#! /usr/bin/env python
# -*- coding:utf8 -*-
import MySQLdb as mdb 
import paramiko as pmk

class changeMediaRes(object):
	def __init__(self,dbname):
		# 初始化数据库链接
		self.conn=mdb.connect(host="localhost",user='root',passwd='abcxxx123',db=dbname,unix_socket='/tmp/mysql.sock')
		self.cursor=self.conn.cursor()
		# 初始化视频服务器连接
		self.ssh = pmk.SSHClient()
		self.ssh.set_missing_host_key_policy(pmk.AutoAddPolicy())
		self.ssh.connect('10.46.180.21',2282,'root')
		# 初始化aes生成记录文件
		#rs_txt = datetime.datetime.now().striftime('%Y_%m_%d') + '.txt'
		self.rs_txt = '/rs.txt'
		#res = {'conn':conn,'cursor':cursor,'ssh':ssh,'rs_txt':rs_txt}
		
	# 解决media_url 不为空但是不是aes的url问题
	def change_media_url(self):
		try:
			self.cursor.execute("select `id`,`media_url` from yjy_im_chat_aes where media_url not like '%aes%' and media_url!='';")
			datas = self.cursor.fetchall()
			dates = []
			for data in datas:
				url=data[1]
				mu_38 = (url.split('/')[-1]).split('.')[0] + '_aes' + '.m3u8'
				mu_38 = (url.split('/')[-1]).split('.')[0] + '_aes' + '.m3u8'
				aes_u = 'aes_' + (url.split('/')[-2]) 
				new_url = '/'.join(url.split('/')[:-2]) + '/' + aes_u + '/' +  mu_38
				sql="update yjy_im_chat_aes set media_url = '%s' where id=%d;"%(new_url,data[0])
				self.cursor.execute(sql)
				self.conn.commit()
		except mdb.Error,e:
			print e
			self.conn.rollback()
   			self.conn.close()

	# 解决media_url链接正确但是file_size不正确或者404问题
	def change_file_size(self):
		try:
			self.cursor.execute("select `id`,`media_url`,`file_size` from yjy_im_chat_aes where file_size='' and media_url!='';")
			datas = self.cursor.fetchall()
			dates = []
			for data in datas:
				id=data[0]
				url=data[1].strip(',')
				server_file_path=url.replace('http://m1.letiku.net','/data/hls').replace('http://media.yijiaoyuan.net:9999','/data/hls')
				stdin,stdout,stderr = self.ssh.exec_command('ls ' + '/'.join(server_file_path.split('/')[:-1]))
				file = stdout.readlines()
				# 如果没有aes加密视频则生成加密视频
				if not file:
					file = ''.join(server_file_path).replace('_aes','').replace('aes_','')
					stdin,stdout,stderr = self.ssh.exec_command('echo '  + '>' + rs_txt)
					stdin,stdout,stderr = self.ssh.exec_command('echo ' + file + '>> ' + rs_txt)
					stdin,stdout,stderr = self.ssh.exec_command('sh /get_aes.sh')
					result = stdout.readlines()
					if not result:
						print file
				#开始获取文件大小并替换数据
				stdin,stdout,stderr = self.ssh.exec_command('du -sh ' + '/'.join(server_file_path.split('/')[:-1]))
				file_size = stdout.readlines()
				file_size = file_size[0].split('\t')[0].strip('M')
				sql="update yjy_im_chat_aes set file_size = '%s' where id=%d;"%(file_size,data[0])
				print sql
				self.cursor.execute(sql)
				self.conn.commit()
		except mdb.Error,e:
			print e
			self.conn.rollback()
   			self.conn.close()


if __name__ == '__main__':
	dbnames=('tcmsq','yjy_xiyizonghe','yjy_xiyizhiyeyishi','yjy_zhongyizonghe','yjy_kouqiangzyys')
	for dbname in dbnames:
		cmr = changeMediaRes(dbname)
		#print cmr.__dict__.items()
		cmr.change_media_url()
		cmr.change_file_size()
