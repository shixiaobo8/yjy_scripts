#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
    视频点播url cdn预热
"""
from aliyunsdkvod.request.v20170321 import PreloadVodObjectCachesRequest
from aliyunsdkvod.request.v20170321 import DescribeVodRefreshQuotaRequest
from aliyunsdkvod.request.v20170321 import GetVideoInfoRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkvod.request.v20170321 import GetPlayInfoRequest
import pymysql
import traceback
import json
import logging
import time
import sys
import requests


# 日志记录器
logfile = "/tmp/vod_cdn_preload_" + time.strftime('%Y-%m-%d',time.localtime()) + ".log"
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s"
#配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '
#配置输出时间的格式，注意月份和天数不要搞乱了
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename=logfile,filemode='a')


# 初始化客户端
def init_vod_client(accessKeyId, accessKeySecret):
    regionId = 'xxxxxxxxxxxx'   # 点播服务接入区域
    connectTimeout = 3         # 连接超时，单位为秒
    return AcsClient(accessKeyId, accessKeySecret, regionId,auto_retry=True, max_retry_time=3, timeout=connectTimeout)


# 使用ak构造clt
def make_clt_client():
    access_key = "xxxxxxxxxxxxxxx"
    secret = "xxxxxxxxxxxxxxxxxxxx"
    clt_client = init_vod_client(access_key, secret)
    return clt_client


# url预热缓存
def preload_object_caches(clt,url):
    request = PreloadVodObjectCachesRequest.PreloadVodObjectCachesRequest()
    objectPath = [url]
    request.set_ObjectPath("\n".join(objectPath))
    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response


# 查询预热剩余次数
def describe_refresh_quota(clt):
    request = DescribeVodRefreshQuotaRequest.DescribeVodRefreshQuotaRequest()
    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response


# 发起api请求
def start_action(action):
    try:
        clt = make_clt()
        res = describe_refresh_quota(clt)
        print(json.dumps(res, ensure_ascii=False,indent=4))
        logging.info(json.dumps(res, ensure_ascii=False,indent=4))
    except Exception as e:
        print(e)
        logging.info(e)
        print(traceback.format_exc())
        logging.info(traceback.format_exc())


# 执行sql语句
def execute_sql(sql):
    user='xxxxxxxxxxxxxxxx'
    pwd='xxxxxxxxxxxxxxxxxx'
    host='xxxxxxxxxxxxxxxxx'
    db_name = "xxxxxx"
    try:
        db = pymysql.connect(host,user,pwd,db_name)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()
        #print(str(data))
        logging.info(str(data))
        return data
    except Exception as e:
        logging.info(str(e))
        print(e)
    finally:
        # 关闭数据库连接
        db.close()


# 获取视频信息
def get_video_info(clt, videoId):
    request = GetVideoInfoRequest.GetVideoInfoRequest()
    request.set_accept_format('JSON')
    request.set_VideoId(videoId)
    response = json.loads(clt.do_action_with_exception(request))
    return response


# 获取播放地址
def get_play_info(clt, videoId):
    request = GetPlayInfoRequest.GetPlayInfoRequest()
    request.set_accept_format('JSON')
    request.set_VideoId(videoId)
    request.set_AuthTimeout(3600*5)
    response = json.loads(clt.do_action_with_exception(request))
    return response


# 获取m3u8文件中的ts地址
def get_ts_url(auth_m3u8_url):
    m3u8_url = auth_m3u8_url.split("?")[0]
    ts_url_prefix = m3u8_url.split("?")[0].replace(m3u8_url.split("/")[-1],"")
    ts_datas = requests.get(auth_m3u8_url).text
    ts_urls =[ ts_url_prefix + ts_data.split("?")[0] for ts_data in ts_datas.split("\n") if "ts?auth_key" in ts_data ]
    return ts_urls


# 从数据库视频源地址
def get_video_source_url(clt):
    sql = "select `vid` from yjy_10_im_course;"
    course_vids = execute_sql(sql)
    for vid in course_vids:
        try:
            playurls = get_play_info(clt,vid[0])['PlayInfoList']['PlayInfo']
            for playurl in playurls:
                video_type = playurl['Definition']
                video_format = playurl['Format']
                auth_url = playurl['PlayURL']
                url = auth_url.split("?")[0]
                # 预热ts文件,api调用此时受限暂不调用
                if url.endswith('.m3u8'):
                    pass
                    #ts_urls = get_ts_url(auth_url)
                    #for ts_url in ts_urls:
                    #    preload_object_caches(clt,ts_url)
                    #    logging.info("正在预热ts url: "+ ts_url + "   清晰度:" + video_type + "格式:" + video_format)
                    #    time.sleep(1)
                else:
                    preload_object_caches(clt,url)
                    logging.info("正在预热url: "+ url + "   清晰度:" + video_type + "格式:" + video_format)
                    time.sleep(1)
        except Exception as e:
            print(str(e))
            logging.info(str(e))
            

if __name__ == "__main__":
    clt = make_clt_client()
    # 剩余查询次数
    remaining_count = describe_refresh_quota(clt)
    logging.info(remaining_count)
    get_video_source_url(clt)
