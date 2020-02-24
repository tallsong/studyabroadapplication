# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
import sys
sys.path.append('D:\\OneDrive\\github\\studyabroadapplication')
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyabroadapplication.settings')
django.setup()
from universitylist.models import University_more,University_indicator_and_subject_rankings,University

#user = User.objects.create_user(username, email, password)
#user.save()
class SaamisPipeline(object):
    def __init__(self):
        pass
    def process_item(self, item, spider):
        if(spider.name=='universitylist'):
            university=University()
            university.name=item['Name']
            university.latest_rank=item['GlobalRank']
            university.city=item['City']
            university.country=item['Country']
            university.address=item['Address']
            university.website=item['Website']
            university.summary=item['Summary']
            university.longitude=item['data_long']
            university.latitude=item['data_lat']
            university.date_url=item['data_url']
            university.save()
            print(item['Name'])
        return item
        if(spider.name=='university_more'):
            for i in item['subject_rankings']:
                if(item['subject_rankings'][i] is not None and item['subject_rankings'][i] !=""):
                    if(item['subject_rankings'][i][0]=='#'):                       
                        rankings=University_indicator_and_subject_rankings()
                        rankings.name=item['Name']
                        rankings.key=i
                        rankings.value=int(item['subject_rankings'][i].replace('\n', '').replace('#', '').replace('\r', ''))
                        rankings.save()
                    else:
                        if('.' not in item['subject_rankings'][i]):
                            university=University_more()
                            university.name=item['Name']
                            university.key=i
                            university.value=int(item['subject_rankings'][i].replace(',', ''))
                            university.save()
                        else:
                            university=University_more()
                            university.name=item['Name']
                            university.key=i
                            university.value=float(item['subject_rankings'][i])
                            university.save()

            return item
    def open_spider(self, spider):
        # spider (Spider 对象) – 被开启的spider
        # 可选实现，当spider被开启时，这个方法被调用。
        #connection = pymysql.connect(host='localhost',  user='root',  password='123456', db='studyabroadapplication',    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        db = spider.settings.get('MYSQL_DB_NAME')
        host = spider.settings.get('MYSQL_HOST')
        port = spider.settings.get('MYSQL_PORT')
        user = spider.settings.get('MYSQL_USER')
        passwd = spider.settings.get('MYSQL_PASSWORD')

        self.db_conn =pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()
    def close_spider(self, spider):
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用
        
        
        self.db_conn.close()