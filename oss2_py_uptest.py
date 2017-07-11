#! /usr/bin/env python
#! -*- coding:utf8 -*-
""" aliyujn oss2 python sdk 上传测试测试!!"""
from __future__ import print_function
import oss2
import os,sys,commands

# 初始化oss登录验证
auth = oss2.Auth('LTAIYj7b9Fm1rrH2', '6rWkgQX8yiIDrOY70vcy19EUuHvjW2')

# bucket地区服务对象,可用于线上该地区的bucket列表
#service = oss2.Service(auth,'oss-cn-beijing-internal.aliyuncs.com')


# 所有ts视频bucket
videos_bucket = oss2.Bucket(auth, 'oss-cn-beijing-internal.aliyuncs.com', 'yjy-media')

# 获取oss的版本控制
#print([b.name for b in oss2.BucketIterator(service)])

# 获取bucket的权限控制
#print(videos_bucket.get_bucket_acl().acl)

###############################
##     以上是初始化程序      ## 
##---------------------------##            
##   以下是oss bucket操作    ##
###############################

# 本地资源路径初始化

videos_bucket_dirs = []
videos_bucket_files = []
local_res_files= []
uploads_dirs = ['/data/hls']
local_res_files= []

# 获取bucket上的文件和目录资源,因为bucket上没有文件夹的概念
def get_res_on_bucket():
	for obj in oss2.ObjectIterator(videos_bucket,delimiter="/"):
		if obj.is_prefix():
			videos_bucket_dirs.end(obj)
		else:
			videos_bucket_files.end(obj)

# 获取要上传的ts视频的本地res的所有文件的绝对路径
# 文件归类
def getLocalFiles(dir):
	#print(dir)
	if os.path.exists(dir):
		for res in os.listdir(dir):
			#print(res)
			ab_dir = dir+os.sep+res
			#print(ab_dir)
			if os.path.isfile(ab_dir):
				if ab_dir.endswith('.ts') or ab_dir.endswith('.m3u8'):
					local_res_files.append(ab_dir)
			if os.path.isdir(ab_dir):
				getLocalFiles(ab_dir)

# 上传文件
def putFileToBucket():
    for file in local_res_files:
        # key: bucket上的名称
		key = file.replace('/data/hls/','').replace('//','/')
		path = os.path.dirname(os.path.dirname(file))
		os.chdir(path)
		rm_cmd = ' find ./ -name *_ali_ali* | xargs rm -rf '
		rs = commands.getstatusoutput(rm_cmd)
		if 'm3u8' in file:
			print(file)
			ali_file = file[:]
			cp_cmd = ' cp ' + ali_file +  ' ' + ali_file[:-5] + '_ali.m3u8'
			rs2 = commands.getstatusoutput(cp_cmd)
			ali_file = ali_file[:-5] + '_ali.m3u8'
			edit_cmd1 = " sed -i " + "'s/\/\//\//g' " +  ali_file
			rs3 = commands.getstatusoutput(edit_cmd1)
			edit_cmd2 = " sed -i " + "'s/http:\/m1\.letiku\.net/https:\/\/yjy-media\.oss-cn-beijing\.aliyuncs\.com/g' " +  ali_file 
			rs4 = commands.getstatusoutput(edit_cmd2)
			ali_key = ali_file.replace('/data/hls/','').replace('//','/')
			result = videos_bucket.put_object_from_file(ali_key,ali_file,progress_callback=percentage)
			print(result)
		result = videos_bucket.put_object_from_file(key,file,progress_callback=percentage)

# 起始程序
def start(dir):
	for dir in uploads_dirs:
		getLocalFiles(dir)

# 进度条功能
def percentage(consumed_bytes, total_bytes):
	if total_bytes:
		rate = int(100* (float(consumed_bytes)) / (float(total_bytes)))
		print ('\r{0}%'.format(rate),end='')
		sys.stdout.flush()

if __name__ == "__main__":
	#get_res_on_bucket()
	start(uploads_dirs)
	#print(local_res_files)
	putFileToBucket()
