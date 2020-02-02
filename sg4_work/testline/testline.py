# -*- coding: UTF-8 -*-
from sg4_work.common.constant import TESTLINE_USE,TESTLINE_PWD

class SVN_CLIENT(object):
    def __init__(self,testline_ip,user=TESTLINE_USE,pwd=TESTLINE_PWD):
        self.testline_ip = testline_ip
        self.user = user
        self.pwd = pwd


if __name__ == "__main__":
    pass
