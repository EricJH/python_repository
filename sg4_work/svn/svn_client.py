# -*- coding: UTF-8 -*-

from svn.common import *
from sg4_work.common.constant import TA_SVN_ROOT_URL,DOMAIN_USER,DOMAIN_PWD

class SVN_CLIENT(object):
    def __init__(self,root_url,user,pwd):
        self.root_url = root_url
        self.user = user
        self.pwd = pwd
        print(self.root_url)

if __name__ == "__main__":
    s = SVN_CLIENT(TA_SVN_ROOT_URL,DOMAIN_USER,DOMAIN_PWD)
