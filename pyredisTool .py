#!/usr/bin/env python
# -*- coding:utf8 -*-
# __author__ : 史怡国
# time : 20170711
"""
	医教园redis服务器配置工具脚本：
	1.支持查询key.getkey,删除key
	2.测试连接,redis性能监控
"""
from redis import Redis
import sys

class MyRedis():
	
	def __init__(self):
		redis = Redis(host='10.47.138.152',port='18669',password='E34g!t4f^f3s$dfp4f')
		self.redis = redis
		self.info = {
			"\033[1;35m --help \033[0m":"查看帮助手册",
			"\033[1;35m  keys \033[0m":"指定要查询的key",
			"\033[1;35m delKeys \033[0m":"指定要删除的key",
			"\033[1;35m info \033[0m":"测试redis连接信息"
		}
	
	# 查询key
	def keys(self,keys=None):
		if keys == None:
			print "请传入key的匹配值"
			sys.exit(1)
		else:
			rs = self.redis.keys(keys)
			print rs

	# 删除key
	def delKeys(self,keys=None):
		k = self.redis.keys(keys)
		if k != None:
			print k
			for k1 in k: 
				self.redis.delete(k1)
			rs = self.keys(keys)		
			if rs == None:
				print "".join(keys)+"已清理完毕"
			else:
				raise "程序异常"	
		else:
			print "未找到改key值"
			sys.exit(1)
	
	# redis 连接测试
	def testInfo(self):
		print self.redis.info()
	
	# 关闭redis连接池					
	#def __del__(self):
	#	self.redis.disconnect()

	# 帮助手册
	def help(self):
		for k,v in self.info.items():
			print k,v

if __name__ == '__main__':
	rd = MyRedis()
	if len(sys.argv) == 2 and sys.argv[1] == 'info':
		rd.testInfo()
	elif len(sys.argv) == 3:
		command_arg1 = sys.argv[1]
		command_arg2 = sys.argv[2]
		if command_arg1 == 'keys':
			rd.keys(keys=command_arg2)
		elif command_arg1 == 'delKeys':
			rd.delKeys(keys=command_arg2)
		else:
			rd.help()
	else:
		rd.help()	
