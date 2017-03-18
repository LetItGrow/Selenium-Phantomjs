# -*-coding=utf-8-*-
__author__ = 'LiuJingYuan'
from DBs.SqlHelper import SqlHelper
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class MySqlHelper(SqlHelper):
    def __init__(self):
        self.database = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', connect_timeout=5,
                     compress=True, charset='utf8')
        self.cursor = self.database.cursor()
        self.dbname = 'tianyanchadb'
        self.tbname = 'tianyanchatb'
        self.dbstatus = True
        self.tbstatus = True
        try:
            self.cursor.execute('use %s' % self.dbname)
        except:
            self.dbstatus = False
        if self.dbstatus == False or self.showtb() == []:
            self.tbstatus = False

    def create_db_tb(self, keys):
        if self.dbstatus == False or self.tbstatus == False:
            keys = list(keys)
            self.cursor.execute('create database if not exists {0}'.format(self.dbname))
            self.database.select_db(self.dbname)
            self.cursor.execute('DROP TABLE IF EXISTS {0}'.format( self.tbname))
            sql = 'create table {0}(id int AUTO_INCREMENT,{1}, PRIMARY KEY(id))DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci;'.format( self.tbname, ' varchar(500),'.join(
                keys) + ' varchar(50),spider_time timestamp default CURRENT_TIMESTAMP')
            self.cursor.execute(sql)
            self.database.select_db(self.dbname)

    # todo: 批量插入
    def batch_insert(self, keys, values):
        try:
            sql = "INSERT INTO {0} ({1})VALUES({2});".format(self.tbname, ','.join(keys), 's,'.join('%' * len(keys)) + 's')
            print values
            self.cursor.executemany(sql,values)
            self.database.commit()
        except:
            sql = "INSERT INTO {0} ({1})VALUES({2});".format(self.tbname, ','.join(keys),  '"'+'","'.join(values)+'"')
            self.cursor.execute(sql)
            self.database.commit()

    # 关闭对象、数据库
    def close(self):
        self.cursor.close()
        self.database.close()

    def showtb(self):
        try:
            self.cursor.execute('show tables;')
            result = self.cursor.fetchall()
            return [tb[0] for tb in result]
        except:
            return []

if __name__ == "__main__":
    pass