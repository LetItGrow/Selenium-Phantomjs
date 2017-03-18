# -*-coding=utf-8-*-
__author__ = 'LiuJingYuan'
from CONGs.config import Keywords
import threading
from SPIDERs.JSspider import jsspider
from PARSERs.parser import lxmlparser
from DBs.MYSQLHelper import MySqlHelper
class Mythread(threading.Thread):
    def __init__(self,func,args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        apply(self.func,self.args)

def start(keyword,lock):
    jsspiders = jsspider()
    MySqlHelpers = MySqlHelper()
    lxmlparsers = lxmlparser()
    html, gsurl = jsspiders.get_req(keyword)
    data = lxmlparsers.JSparser(html, gsurl)
    jsspiders.close()
    keys = [key for key, value in data.items()]
    MySqlHelpers.create_db_tb(keys)
    data = [value for key, value in data.items()]
    MySqlHelpers.batch_insert(keys,data)

def main():
    keywordlist = Keywords
    lock = threading.Lock()
    mythreads = []
    for keyword in keywordlist:
        t = Mythread(start,(keyword,lock))
        mythreads.append(t)

    for mythread in mythreads:
        mythread.start()

    for i in mythreads:
        i.join(10)

if __name__ == '__main__':
    main()