# -*- coding:utf-8 -*-
'''
定义对mysql数据库基本操作的封装
1.包括基本的单条语句操作，删除、修改、更新
2.独立查询单条、查询多条数据
3.独立添加多条数据
'''

import pymysql
import logging
import os,json

class OperationDbInterface(object):

    def __init__(self):
        self.dbary = ['ams', 'ims', 'mms', 'cms']
        self.db_conn = {} #连接的对应字典
        for db in self.dbary:
            # host='ams.starschina.com',正式跑的时候要连正式服
            self.conn = pymysql.connect(host='test.ams.starschina.com',
                                        user='root',
                                        password='78dx4AMS',
                                        db=db,
                                        port=3306,
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)  # 创建数据库连接
            self.cur = self.conn.cursor()  # 创建游标
            self.conn_cur= {} # 连接-库的对应字典
            self.conn_cur[self.conn] = self.cur
            self.db_conn[db] = self.conn_cur

    # 定义单条数据操作，增删改
    def op_sql(self, params):
        try:
            self.cur.execute(params)  # 执行sql语句
            self.conn.commit()
            return True
        except pymysql.Error as e:
            print("MySQL Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), './log.txt'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levekname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return False

    # 查询表中单条数据
    def select_one(self, condition):
        try:
            self.cur.execute(condition)
            results = self.cur.fetchone()  # 获取一条结果
        except pymysql.Error as e:
            results = 'sql0001'  # 数据库执行失败
            print("MySQL Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), './log.txt'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        finally:
            return results

    # 查询表中所有数据
    def select_all(self, condition):
        try:
            self.cur.execute(condition)
            self.cur.scroll(0,  mode='absolute')  # 光标回到初始位置
            results = self.cur.fetchall()  # 返回游标中所有结果
        except pymysql.Error as e:
            results = 'sql0001'  # 数据库执行失败
            print("MySQL Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), './log.txt'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        finally:
            return results

    # 定义更多数据操作（插入数据，更新数据，删除数据）
    def operate_more(self, condition, params):
        try:
            self.cur.executemany(condition, params)
            self.conn.commit()
            return True
        except pymysql.Error as e:
            results = 'sql0001'  # 数据库执行失败
            print("MySQL Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), './log.txt'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levekname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return results

    # 数据库关闭
    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()


# if __name__ == "__main__":
#     test = OperationDbInterface()  # 实例化类
#     result_1 = test.select_one('select*from video where id = 1014874')  # 查询一条数据
#     print(result_1)
#
#     result_2 = test.select_all('select*from video where score>9.5')  # 查询所有数据
#     result_2 = test.select_one('select video_id FROM episode where status = 2 ORDER BY RAND() LIMIT 1;')
#     print(result_2)


    # result_3 = test.operate_more('insert into persons  values (%s, %s, %s)', (4, '付千', '兰州'))  # 插入一条数据
    # print(result_3)
    # # tmp = ((4, '付千', '兰州'), (5, '韩以', '温州'), (6, '曹七', '丽水'))
    # # result_4 = test.operate_more("insert into persons  values (%s, %s, %s)", tmp)  # 插入三条数据
    # # print(result_4)
    # result_5 = test.operate_more('delete from persons where NAME = %s', ('李阳'))  # 删除一条数据
    # print(result_5)
    # result_6 = test.operate_more('update persons set NAME = %s where NAME = %s', ('陈浩', '陈昊'))  # 修改一条数据
    # print(result_6)