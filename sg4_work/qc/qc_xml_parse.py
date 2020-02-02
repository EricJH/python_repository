# -*- coding: UTF-8 -*-

from xml.etree.ElementTree import fromstring

class QC_REST_XML(object):
    def __init__(self,text):
        self.root = fromstring(text)

    def get_all_entity_fields(self,entity_type_name,fields_name_list):
        type_list = []
        res_list = []
        for i in self.root.findall('Entity'):
            if i.get('Type') == entity_type_name:
                type_list.append(i)
        for i in type_list:
            tmp = {}
            for j in fields_name_list:
                 for k in i.find('Fields').findall('Field'):
                     if k.get('Name') == j:
                         try:
                             res = k.findall('Value')
                             if len(res) == 1:
                                 tmp[j] = res[0].text
                             elif len(res) > 1:
                                 tmp[j] = []
                                 for m in res:
                                     tmp[j].append(m.text)
                         except Exception as e:
                             tmp[j] = ""
            res_list.append(tmp)
        return res_list



