# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class DbPipeline:
    def __init__(self):
        self.conn=pymysql.connect( host="localhost",
                                    port=3306,
                                    user="root",
                                    password="123456",
                                    database="itheima",
                                    charset="utf8mb4",)
        #创建游标
        self.cursor=self.conn.cursor()
    def close_spider(self,spider):
        #关闭
        self.conn.commit()
        self.conn.close()
    def process_item(self, item, spider):
        name=item.get('name','')
        director=item.get('director','')
        year=item.get('year','')
        self.cursor.execute(
            'insert into hiemamovie (name,director,year) values (%s,%s,%s)',
            (name,director,year)
        )
        return item
