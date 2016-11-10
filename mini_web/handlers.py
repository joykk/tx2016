#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
from tornado.web import RequestHandler
import time
import json
from tornado_mysql import pools

MYSQL_POLL = pools.Pool(dict(host='119.29.21.95', port=3306, user='root', passwd='joy123', db='summermini', charset='utf8'),max_idle_connections=10, max_recycle_sec=10)


#获取时间解析(分钟)
def parse_time(ctime=None):
    print ctime
    if not ctime:
        ctime=time.strftime("%H%M")
    temp = ctime[:2]+":"+ctime[2:]
    ttime = temp[:5]+":" + "00"
    current_time = "2016-07-12 "+str(ttime)
    return current_time


#获取时间解析(秒钟)
def parse_sec_time(ctime=None):
    print ctime
    if not ctime:
        ctime=time.strftime("%H%M%S")
    temp = ctime[:2]+":"+ctime[2:]
    ttime = temp[:5]+":" + temp[5:]
    current_time = "2016-07-12 "+str(ttime)
    return current_time


#判断city是否已经在字典中统计过
def hasCity(datalist, city):
    d_size = len(datalist)
    for i in range(d_size):
        if datalist[i]['name'] == city:
            return i
    return None


#全国实时总点击数(秒)
class ChinaSecondSumHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime=None):
        if not ctime:
            ctime = time.strftime("%H%M%S")
        temp = ctime[:2]+":"+ctime[2:]
        ttime = temp[:5]+":" + temp[5:]
        current_time = "2016-07-12 "+str(ttime)

        query_sum_sql = "select number from t_china_sec where time_sec = '%s'" % (current_time)
        cur_sum = yield MYSQL_POLL.execute(query_sum_sql)
        result = {'code': 0,'time':current_time,'body':{}}
        for row_sum in cur_sum:
            if "all_sum" not in result['body'].keys():
                result['body']['all_sum'] = row_sum[0]

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result ,ensure_ascii=False))
        self.finish()

#全国实时总点击数(分钟)
class ChinaMinSumHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime=None):
        if not ctime:
            ctime = time.strftime("%H%M%S")
        temp = ctime[:2]+":"+ctime[2:]
        ttime = temp[:5]+":" + "00"
        current_time = "2016-07-12 "+str(ttime)

        query_sum_sql = "select number from t_china_min where time_min = '%s'" % (current_time)
        cur_sum = yield MYSQL_POLL.execute(query_sum_sql)
        result = {'code': 0,'time':current_time,'body':{}}
        result['body']['all_sum'] = 0
        for row_sum in cur_sum:
            result['body']['all_sum'] += row_sum[0]

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result ,ensure_ascii=False))
        self.finish()

# 查看全国的分布
'''
class ChinaHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime=None):
        current_time = parse_time(ctime)
        query_sql = "select id_city, city, number from t_china_min, t_city_dic where time_min='%s' and t_city_dic.id = t_china_min.id_city;" % (current_time)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        result = {'code': 0,'time':current_time,'body':{}}
        for row in cur:
            if row[1] not in result['body'].keys():
                result['body'][row[1]] = row[2]
            else:
                result['body'][row[1]] += row[2]

        self.write(json.dumps(result ,ensure_ascii=False))
        self.finish()
'''

class ChinaHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime=None):
        current_time = parse_time(ctime)
        query_sql = "select id_city, city, number from t_china_min, t_city_dic where time_min='%s' and t_city_dic.id = t_china_min.id_city;" % (current_time)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        result = {'code': 0,'time':current_time,'body':[]}
        for row in cur:
            datalist = result['body']
            flag = hasCity(datalist,row[1])
            if flag == None:
                temp = {}
                temp['name'] = row[1]
                temp['value'] = row[2]
                result['body'].append(temp)
            else:
                result['body'][flag]['value']+=row[2]
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result ,ensure_ascii=False))
        self.finish()


# 查看全国的分布(秒)
class ChinaSecHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime=None):
        current_time = parse_sec_time(ctime)
        query_sql = "select id_city, city, number from t_city_sec_num, t_city_dic where time_sec='%s' and t_city_dic.id = t_city_sec_num.id_city;" % (current_time)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        result = {'code': 0,'time':current_time,'body':[]}
        for row in cur:
            datalist = result['body']
            flag = hasCity(datalist,row[1])
            if flag == None:
                temp = {}
                temp['name'] = row[1]
                temp['value'] = row[2]
                result['body'].append(temp)
            else:
                result['body'][flag]['value']+=row[2]
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result ,ensure_ascii=False))
        self.finish()


#查看每个省的分布
'''
class ProviceHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, cprovince):
        current_time = parse_time()
        query_sql = "select distinct c.city,a.number from t_china_min as a left join t_province_city_dic as b on a.id_city = b.id_city left join t_city_dic as c on c.id=a.id_city where b.id_province='%s' and a.time_min='%s'" % (cprovince,current_time)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        query_sql_province = "select province from t_province_dic where id = '%s'" % (cprovince)
        print query_sql_province
        province_cur = yield  MYSQL_POLL.execute(query_sql_province)
        province_name = ""
        for row in province_cur:
            province_name = row[0]
        result = {'code': 0,'time':current_time,'body':{province_name:{}}}
        for row in cur:
            if row[0] not in result['body'][province_name]:
                result['body'][province_name][row[0]] = row[1]
            else:
                result['body'][province_name][row[0]] += row[1]
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()
'''
class ProviceHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, cprovince):
        current_time = parse_time()
        query_sql = "select c.city,a.number from t_china_min as a left join t_province_city_dic as b on a.id_city = b.id_city left join t_city_dic as c on c.id=a.id_city where b.id_province='%s' and a.time_min='%s'" % (cprovince,current_time)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        query_sql_province = "select province from t_province_dic where id = '%s'" % (cprovince)
        print query_sql_province
        province_cur = yield  MYSQL_POLL.execute(query_sql_province)
        province_name = ""
        for row in province_cur:
            province_name = row[0]
        result = {'code': 0,'time':current_time,'body':{province_name:[]}}

        for row in cur:
            datalist = result['body'][province_name]
            flag = hasCity(datalist,row[0])
            if flag == None:
                temp = {}
                temp['name'] = row[0]
                temp['value'] = row[1]
                result['body'][province_name].append(temp)
            else:
                result['body'][province_name][flag]['value']+=row[1]

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()


#查看每个省的总点击(秒)
class ProviceSumHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, cprovince,ctime=None):
        current_time = parse_sec_time(ctime)
        query_sql = "select SUM(number) FROM t_city_sec_num WHERE time_sec = '%s' and id_city in (select id_city from t_province_city_dic WHERE id_province='%s')" % (current_time,cprovince)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        result = {'code': 0,'time':current_time,'body':{}}
        for row in cur:
            result['body']['all_sum'] = int(row[0])

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()


#查看全国top3
class Top3Handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime):
        current_time = parse_time(ctime)
        query_sql = "select char_video_top1,video_top1_number,char_video_top2,video_top2_number,char_video_top3,video_top3_number from t_top3 where time_min = '%s'" % (current_time)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        result = {'code': 0,'time':current_time,'body':{}}
        #tresult = result
        for row in cur:
            video_query_1 = "select name_video from t_char_video_name_video_dic where id = '%s'" % (row[0])
            print video_query_1
            cur_1 = yield MYSQL_POLL.execute(video_query_1)
            result['body']['1'] = {}
            for row_1 in cur_1:
                result['body']['1']['video'] = row_1[0]
                result['body']['1']['num'] = row[1]
            video_query_2 = "select name_video from t_char_video_name_video_dic where id = '%s'" % (row[2])
            print video_query_2
            cur_2 = yield MYSQL_POLL.execute(video_query_2)
            result['body']['2'] = {}
            for row_2 in cur_2:
                result['body']['2']['video'] = row_2[0]
                result['body']['2']['num'] = row[3]
            video_query_3 = "select name_video from t_char_video_name_video_dic where id = '%s'" % (row[4])
            print video_query_3
            cur_3 = yield MYSQL_POLL.execute(video_query_3)
            result['body']['3'] = {}
            for row_3 in cur_3:
                result['body']['3']['video'] = row_3[0]
                result['body']['3']['num'] = row[5]
            #result = sorted(result['body'].iteritems(),key=lambda d:d[1],reverse=True)

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()


#top3 全国分布
'''
class Top3DetailHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,video_id):
        current_time = parse_time()
        query_sql_id = "select char_video_top1,char_video_top2,char_video_top3 from t_top3 where time_min = '%s'" % (current_time)
        print query_sql_id
        cur_id = yield MYSQL_POLL.execute(query_sql_id)
        result={'code':0,'time':current_time,'body':{}}
        for row_t in cur_id:
            id_list = [row_t[0],row_t[1],row_t[2]]
            for v_id in id_list:
                query_sql = "select c.city,t.number from t_detail_top as t left join t_city_dic as c on c.id = t.id_city where time_min='%s' and t.id_video = '%s'" % (current_time,v_id)
                print query_sql
                cur = yield MYSQL_POLL.execute(query_sql)
                query_sql_video = "select name_video from t_char_video_name_video_dic where id = '%s'" % (v_id)
                print query_sql_video
                cur_video = yield MYSQL_POLL.execute(query_sql_video)
                video_name = ""
                for row in cur_video:
                    video_name = row[0]
                result['body'][video_name] = {}
                for row in cur:
                    if row[0] not in result['body'][video_name]:
                        result['body'][video_name][row[0]] = row[1]
                    else:
                        result['body'][video_name][row[0]] += row[1]

        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()
'''

class Top3DetailHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,video_id):
        current_time = parse_time()
        query_sql_id = "select char_video_top1,char_video_top2,char_video_top3 from t_top3 where time_min = '%s'" % (current_time)
        print query_sql_id
        cur_id = yield MYSQL_POLL.execute(query_sql_id)
        result={'code':0,'time':current_time,'body':{}}
        for row_t in cur_id:
            id_list = [row_t[0],row_t[1],row_t[2]]
            for v_id in id_list:
                query_sql = "select c.city,t.number from t_detail_top as t left join t_city_dic as c on c.id = t.id_city where time_min='%s' and t.id_video = '%s'" % (current_time,v_id)
                print query_sql
                cur = yield MYSQL_POLL.execute(query_sql)
                query_sql_video = "select name_video from t_char_video_name_video_dic where id = '%s'" % (v_id)
                print query_sql_video
                cur_video = yield MYSQL_POLL.execute(query_sql_video)
                video_name = ""
                for row in cur_video:
                    video_name = row[0]
                result['body'][video_name] = []

                for row in cur:
                    datalist = result['body'][video_name]
                    flag = hasCity(datalist,row[0])
                    if flag == None:
                        temp = {}
                        temp['name'] = row[0]
                        temp['value'] = row[1]
                        result['body'][video_name].append(temp)
                    else:
                        result['body'][video_name][flag]['value']+=row[1]

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()


#累计到当前的全国总点击量
class ChinaCurrentSumHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime):
        current_time = parse_sec_time(ctime)
        query_sql_id = "select sum(number) from t_china_sec where time_sec <= '%s'" % (current_time)
        print query_sql_id
        cur_id = yield MYSQL_POLL.execute(query_sql_id)
        result={'code':0,'time':current_time,'body':{}}
        for row in cur_id:
            result['body']['all_sum'] = str(row[0])

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()


#到当前每一秒的总数都返回，用于拖放功能
class ChinarealSumHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime):
        current_time = parse_sec_time(ctime)
        query_sql_id = "select time_sec,number from t_china_sec where time_sec <= '%s'" % (current_time)
        print query_sql_id
        cur_id = yield MYSQL_POLL.execute(query_sql_id)
        result={'code':0,'time':current_time,'body':[]}
        for row in cur_id:
            temp = {}
            temp['time'] = str(row[0])
            temp['sum'] = row[1]
            result['body'].append(temp)

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()

class ChinaAllSecHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime):
        current_time = parse_sec_time(ctime)
        min = '2016-07-12 00:00:00'
        max = current_time
        result={'code':0,'time':current_time}
        data = ""
        timeArray = time.strptime(min,"%Y-%m-%d %H:%M:%S")
        startStamp = int(time.mktime(timeArray))
        timeArray = time.strptime(max,"%Y-%m-%d %H:%M:%S")
        endStamp= int(time.mktime(timeArray))
        t1 = startStamp
        t2 = endStamp
        while t1<=t2:
            tt = time.strftime("%H:%M:%S",time.localtime(t1))
            data+=tt
            data+=","
            t1+=1
        data=data[:-1]
        result['body'] = data

        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()


#返回当下热门前10视频，时间间隔10mins
class ChinaTop20Handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,ctime):
        current_time = parse_time(ctime)
        query_sql = "select char_video_top1,char_video_top2,char_video_top3,char_video_top4,char_video_top5,char_video_top6,char_video_top7,char_video_top8,char_video_top9,char_video_top10, video_top1_number, video_top2_number, video_top3_number, video_top4_number, video_top5_number, video_top6_number, video_top7_number, video_top8_number, video_top9_number, video_top10_number from t_top20 where time_min = '%s'" % (current_time)
        print query_sql
        cur = yield MYSQL_POLL.execute(query_sql)
        result={'code':0,'time':current_time,'body':[]}
        vid_num_dic = {}
        for row in cur:
            for i in range(10):
                vid_num_dic[row[i]] = row[i+10]

        print vid_num_dic
        vid_num_dic = sorted(vid_num_dic.items(),key=lambda e:e[1],reverse=True)
        count = 0
        for vid_num in vid_num_dic:
            query_video = "select name_video from t_char_video_name_video_dic where id = %s " % (vid_num[0])
            print query_video
            cur_video = yield MYSQL_POLL.execute(query_video)
            count+=1
            for row in cur_video:
                temp = {'name':row[0],'value':vid_num[1]}
                result['body'].append(temp)

        #result['body'] = sorted(result['body'].items(),key=lambda e:e[1],reverse=True)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result,ensure_ascii=False))
        self.finish()

