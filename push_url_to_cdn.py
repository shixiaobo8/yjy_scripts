#!/usr/bin/env python
# -*- coding:utf8 -*-
# cdn 预热脚本
from aliyunsdkcore import client
from aliyunsdkcdn.request.v20141111 import DescribeUserDomainsRequest
from aliyunsdkcdn.request.v20141111 import DescribeUserDomainsRequest
import glob,os,sys,commands,datetime,re,requests,json,random,time
import MySQLdb as mdb
src_domain='media-src.letiku.net'
today = datetime.date.today()
get_ip_province_api='http://ip.taobao.com/service/getIpInfo.php?ip='
yesterday = today - datetime.timedelta(days=1)
UrlList = []
m3u8List = []
logUrls = []
comeback_ips = []
comebacks = dict()
log_path='/data/logs/'
db_conn = mdb

# request根据淘宝接口获取ip
def getIpProvince():
	try:
		db_conn = mdb.connect('10.51.79.194','count','count_user','app_count')
		db_conn.set_character_set('utf8')
		cursor = db_conn.cursor()
		table_name = str(yesterday) + '-video_comeback_count_ip'
		create_table_sql = " drop table if exists `" + table_name + "`;create table if not exists `" + table_name + "` (`id` int(254)  not null AUTO_INCREMENT, `country` varchar(100) default '', `country_id` varchar(100) default '', `area` varchar(100) default '', `area_id` varchar(100) default '', `region` varchar(100) default '', `region_id` varchar(100) default '', `city` varchar(100) default '',`city_id` varchar(100) default '', `county` varchar(100) default '', `county_id` varchar(100) default '', `isp` varchar(100) default '', `isp_id` varchar(100) default '', `ip` varchar(100) default '',primary key(`id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8;"
		cursor.execute(create_table_sql)
		# 库化回源ip数据
		# execute_many_args = []
		for ip in comeback_ips:
			url = get_ip_province_api + ip
			r = requests.get(url)
			data = json.loads(r.text)['data']
			insert_keys = "("
			insert_values = "("
			for d_k,d_v in data.items():
				insert_keys +=   d_k + ','
				insert_values += "'" + d_v + "'" + ','
			insert_keys = insert_keys[:-1]
			insert_values = insert_values[:-1]
			insert_keys +=  ")"
			insert_values +=  ")"
			#execute_many_args.append(insert_values)
		#insert_sql = "insert into `" + table_name + "`" + insert_keys + " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,$s,%s)"
			insert_sql = "insert into `" + table_name + "`" + insert_keys + ' values '  + insert_values;
			#print insert_sql
			cursor.fetchall()
			cursor.close()
			cursor=db_conn.cursor()
			cursor.execute(insert_sql)
		#print execute_many_args
		#cursor.executemany(insert_sql,execute_many_args)
		db_conn.commit()
	except mdb.Error,e:
		cursor.close()
		#db_conn.rollback()
		#db_conn.close()
		print e
	finally:
		cursor.close()
		db_conn.close()
		
	
#  获取m3u8文件和ts链接地址
def getAllTsFileList(media_path='/data/hls'):
	cmd1 = 'find ' + media_path + ' -name *.m3u8'
	m3u8List = commands.getstatusoutput(cmd1)[1].split('\n')
	for m3u8 in m3u8List:
		with open(m3u8) as f: 
			for line in f.readlines():
				if line.endswith('.ts\n'):
					UrlList.append(line.replace('\n',''))

# 处理ts和m3u8的链接
def getUrlByLog():
# 查找最近几天回源的ts和m3u8的链接
	 ips = []
	 Year = str(yesterday).split('-')[0]
	 Month = str(yesterday).split('-')[1]
	 Day = str(yesterday).split('-')[2]
	 logfile = log_path + Year + os.sep + Month + os.sep + 'upstream.' + src_domain + '.access_' + Year + Month + Day +  '.log'
	 with open(logfile) as f:
		content = f.readlines()
		for c in content:
			c1 = c.split(' ')
			for c2 in c1:
				# 获取回源url
				if 'ts' in c2 or 'm3u8' in c2:
					logUrls.append('http://m1.letiku.net'+c2)
				# 获取回源ip
				if c2.count('.') == 3 and re.match('(\d+\.)[3]',c2):
					ip = c2
					ips.append(ip)
	 ips = list(set(ips))
	 comeback_ips.extend(ips)
					
# 预热这些天回源的ts和m3u8的链接
	 #print len(logUrls)
	 #print len(list(set(logUrls)))
	 #for url in logUrls:
	 #	print url

def callsdk():
# 初始化api调用
	"""完整的url 调用示例:
	https://cdn.aliyuncs.com/?Format=xml&Version=2013-01-10&Signature=Pc5WB8gokVn0xfeu%2FZV%2BiNM1dgI%3D&SignatureMethod=HMAC-SHA1&SignatureNonce=15215528852396&SignatureVersion=1.0&AccessKeyId=key-test&TimeStamp=2012-06-01T12:00:00Z
	由于该api涉及的请求参数较多需要调用统计目录下的cdn.py 生成一个具有时效性的请求apiurl(包含 签名和请求参数等)
	"""
	# 由于目前需预热的url较多，因此每天随机预热1500个 剩余500个用于新上传的url刷新
	random_urls = [ UrlList[random.randint(0,len(UrlList))] for i in range(0,8000) ]
	for url in random_urls:
		cmd = 'python /root/scripts/cdn.py Action=PushObjectCache ObjectPath='+url+' ObjectType=File'
		pushCacheUrl = commands.getstatusoutput(cmd)[1]
		print pushCacheUrl
		r = requests.get(pushCacheUrl)
		print r.text
		time.sleep(5)

if __name__ == '__main__':
	getUrlByLog()
	getAllTsFileList()
	callsdk()
	#print len(UrlList)
	#getIpProvince()
	#print len(comeback_ips)
