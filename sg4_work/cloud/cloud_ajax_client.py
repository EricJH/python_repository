# -*- coding: utf-8 -*-

from sg4_work.common.constant import CLOUD_LOGIN_URL,CLOUD_ROOT_URL
from requests import Session

class CLOUD_CLIENT(object):
    def __init__(self):
        self.session = Session()

    def login_cloud(self):
        pass

