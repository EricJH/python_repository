# -*- coding: utf-8 -*-

from requests import Session
from sg4_work.common.constant import DOMAIN_USER,DOMAIN_PWD,PR_ROOT_URL,PR_SSO_AUTH_URL

class PR_CLIENT(object):
    def __init__(self):
        self.session = Session()
        self.login_sso()

    def login_sso(self):
        login_data = {
            'PASSWORD': DOMAIN_PWD,
            'SMENC': 'ISO-8859-1',     # 编码格式
            'SMLOCALE': 'US-EN',
            'USER': DOMAIN_USER,
            'postpreservationdata': '',
            'smauthreason': '0',
            'target': "%s/"%PR_ROOT_URL,
            'x': '32',
            'y': '16',
        }
        resp = self.session.post(url=PR_SSO_AUTH_URL,data=login_data)
        if resp.url == "%s/home.html"%PR_ROOT_URL:
            print("---->Login pronto successfully !")
        else:
            print("---->Fail to login pronto,The directed url is '%s'."%resp.url)

if __name__ == "__main__":
    s = PR_CLIENT()
