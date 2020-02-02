# -*- coding: utf-8 -*-
import time,datetime
print(time.time())
print(datetime.datetime.today().year)
class NSB_DATE(object):
    def __init__(self):
        self.data = ""
        self.belong_week = ""
        self.belog_fb = ""
        self.yearindex = ""

class NSB_CALENDAR(object):
    def __init__(self):
        self.start_date = "2020.01.08"