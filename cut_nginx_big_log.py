#! /usr/bin/env python
# -*- coding:utf8 -*-
""" 
	切分nginx 按照日期和文件大小切分日志文件
"""
from __future__ import division
import os,sys

big_file='/data/logs/media.net.error.log'

# 按照文件大小拆分
def split_by_filesize(fromfile,todir,chunksize=0):
	"""
		chunksize: 字节建议每100M一个独立的文件
		f.read(int byte字节)
		100(M) = 100 * 1024 * 1024 (b) = 104857600 (b)
	"""
	# 创建切分文件后的临时目录
	if not os.path.exists(todir):
		os.mkdir(todir)
	else:
		for fname in os.listdir(todir):
			os.remove(os.path.join(todir,fname))
	# 按文件大小计算可切分的文件个数(100m一个)
	partnums = os.path.getsize(fromfile) / chunksize
	# 打开文件
	
	partnum = 0
	with open(fromfile,'rb') as f:	
		while True:
			chunk = f.read(chunksize) # 每次读取100m
			if not chunk:
				break
			filename = os.path.join(todir,big_file.split('/')[-1] + '_part_'+str(partnum))
			with open(filename,'wb') as f1:
				print "正在写入第" + str(partnum) + "个文件" + filename
				f1.write(chunk)
				print "第"+ str(partnum) + "个文件写入完成" + filename
			partnum += 1

# 按照日志日期分割
def split_by_date(srcfile,todir):
	"""
		从源文件srcfile中读取,确定日期,然后将其写入到分片文件中
	"""	
	# 读取文件到内存中,利用generator 生成器
	with open(srcfile) as f:
		contents = f.readlines()
		c = [ line[0:10].strip() for line in contents ]
		date_l = sorted(set(c),key=c.index)
		for date in date_l:
			f_date = date.replace('/','_')
			filename = os.path.join(todir,srcfile.split('/')[-1] + '_'+ f_date)
			print "正在写入文件" + filename
			with open(filename,'wb') as f:
				for line in contents:
					d = line[0:10].strip()
					if d in line and d == date:
						f.write(line)
		
if __name__ == '__main__':
	# split_by_filesize(big_file,'/test/',chunksize=100*1024*1024)
	split_by_date(big_file,'/test/')
