# -*- coding: utf-8 -*-

from http.cookiejar import CookieJar
from urllib.request import Request,HTTPCookieProcessor,build_opener
from sg4_work.common.constant import *

class CLOUD_SPIDER(object):
    def __init__(self):
        self.login_url = CLOUD_LOGIN_URL
        self.cloud_root_url = CLOUD_ROOT_URL
        self.login_user = QC_USER
        self.login_pwd = QC_PWD

        self.login()

    def login(self):
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip,deflate,br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }

        self.cookiejar = CookieJar()
        self.cookie_handler = HTTPCookieProcessor(self.cookiejar)
        self.opener = build_opener(self.cookie_handler)
        self.opener.add_handler(self.cookie_handler)

        self.opener.open(Request(url=self.login_url))
        print(self.cookiejar._cookies["cloud.ute.nsn-rdnet.net"]["/"]["csrftoken"])

s = CLOUD_SPIDER()
