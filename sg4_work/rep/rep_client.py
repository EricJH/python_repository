# -*- coding: UTF-8 -*-

from requests import Session
from sg4_work.common.constant import REP_ROOT_URL,DOMAIN_USER,DOMAIN_PWD
__all__ = ['REP_CLIENT']

class REP_CLIENT(object):
    def __init__(self):
        self.root_url = REP_ROOT_URL
        self.login()

    def login(self):
        self.session = Session()
        resp = self.session.get(self.root_url)
        self.login_csrftoken = self.session.cookies.get_dict()['csrftoken']  # 第一次访问没登录会被重定向到登录页面"https://4g-rep-portal.wroclaw.nsn-rdnet.net/login/?next=/%3Ffs%3D4g"
        login_data = {
                'csrfmiddlewaretoken': self.login_csrftoken,
                'username': DOMAIN_USER,
                'password': DOMAIN_PWD,
                'sign_in': 'Log in'
        }
        resp = self.session.post(url=resp.url,data=login_data)
        if resp.url.startswith("%s/%s"%(self.root_url,"dashboard/main/")):   # REP登录成功后第一个显示的页面是"https://4g-rep-portal.wroclaw.nsn-rdnet.net/dashboard/main/"
            print('---->Login REP Successfully')
        else:
            print('---->Login REP Failed')

if __name__ == "__main__":
    OBJ = REP_CLIENT()
