# -*-coding=utf-8-*-
__author__ = 'LiuJingYuan'
'''
sql操作的基类
'''
class SqlHelper(object):

    def __init__(self):
        pass

    def insert(self, tableName,value):
        pass

    def batch_insert(self,values):
        pass

    def delete(self, tableName, condition):
        pass

    def batch_delete(self, tableName,values):
        pass

    def update(self, tableName,condition,value):
        pass

    def select(self, tableName,condition,count):
        pass

    def selectOne(self,tableName,condition,value):
        pass

    def close(self):
        pass