# -*- coding: UTF-8 -*-

from requests import Session
from base64 import b64encode
from sg4_work.common.constant import *
from sg4_work.qc.qc_xml_parse import QC_REST_XML

class QC_REST_CLIENT(object):
    def __init__(self):
        self.auth = b64encode("{}:{}".format(DOMAIN_USER,DOMAIN_PWD).encode(encoding='utf-8')).decode()
        self.header = {
            "Accept":          "*/*",
            "Content-Type":    "application/json",
            "Authorization":   "Basic %s"%self.auth
        }
        self.login_qc()

    def login_qc(self):
        self.session = Session()
        resp = self.session.get(url="https://qc12-prod.int.net.nokia.com/qcbin/api/authentication/sign-in",headers=self.header,proxies=NOKIA_PROXY)
        if resp.status_code == 200:
            # print(self.session.cookies)里面有ALM_USER, LWSSO_COOKIE_KEY, QCSESSION, XSRF-TOKEN
            # 接下来直接Request,服务器会把"JSESSIONID"下发到cookie里的,以后每次request都会带上这5个必须的参数
            print("---->登录QC REST API成功")

    def logout(self):
        resp = self.session.get(url="https://qc12-prod.int.net.nokia.com/qcbin/api/authentication/sign-out",headers=self.header,proxies=NOKIA_PROXY)
        if resp.status_code == 200:
            print("---->退出QC REST API成功")

    # 获取一个TestSet下的所有TestCase的一些信息:
    #   参数内容            举例值                             对应的QC返回resp里XML的"Field"节点的属性Name值
    #------------------------------------------------------------------------------------------------------
    #   QC_ID               3037687                           id
    #   Testcase_Name       2430_I_001_06_xxx                 name
    #   Latest_PASS_Build   SBTS20A_ENB_0000_000177_000000    user-03
    #   Status              Passed                            status
    #   Platform            Airscale/FSIH                     user-59            R3还是R4的
    #   Requirements        LTE_CP_50607                      user-80            可能不止一个
    #   Test_Subarea        FDD specific/TDD specific         user-06            TDD的还是FDD的
    #   Feature             LTE2430                           user-13            可能不止一个
    #   Test_Config_ID      149931                            test-config-id
    #   Testset_ID          405711                            cycle-id
    #   Test_ID             147640                            test-id
    #   Type                CIT                               user-69
    def get_all_testcase_info_under_testset(self,testset_id,testset_name='test-instance',fileds=['id','name','user-03','status','user-59','user-80','user-06','user-13','test-config-id','cycle-id','test-id','user-69']):
        params = {
            "query": "{contains-test-set.id[%d]}"%testset_id,
            "fileds": "test-id,name"
        }
        resp = self.session.get(url="https://qc12-prod.int.net.nokia.com/qcbin/rest/domains/MN_LTE/projects/FDD_LTE/test-instances",headers=self.header,params=params,proxies=NOKIA_PROXY)
        if resp.status_code == 200:
            instance = QC_REST_XML(resp.text)
            return instance.get_all_entity_fields(testset_name,fileds)
        else:
            return resp

    def get_trunk_cit(self):
        total_res = []
        r3_tdd = []
        r4_tdd = []
        r4_fdd = []
        for num in QC_TRUNK_CIT_TESTSET_ID:
            total_res = total_res + self.get_all_testcase_info_under_testset(num)
        for i in total_res:
            if i['user-59'] == "FSIH" and i['user-06'] == "TDD specific":
                r3_tdd.append(i)
            elif i['user-59'] == "Airscale" and i['user-06'] == "TDD specific":
                r4_tdd.append(i)
            elif i['user-59'] == "Airscale" and i['user-06'] == "FDD specific":
                r4_fdd.append(i)

        print("====>  QC_Trunk_CIT_R3_TDD:  Total:%d"%len(r3_tdd))
        for i in r3_tdd:
            print("%s    %s    %s    %s"%(i['status'],i['user-03'],i['id'],i['name']))
        print("====>  QC_Trunk_CIT_R4_TDD:  Total:%d"%len(r4_tdd))
        for i in r4_tdd:
            print("%s    %s    %s    %s"%(i['status'],i['user-03'],i['id'],i['name']))
        print("====>  QC_Trunk_CIT_R4_FDD:  Total:%d"%len(r4_fdd))
        for i in r4_fdd:
            print("%s    %s    %s    %s"%(i['status'],i['user-03'],i['id'],i['name']))

    def get_sran20A_cit(self):
        total_res = []
        r3_tdd = []
        r4_tdd = []
        r4_fdd = []
        for num in QC_SRAN20A_CIT_TESTSET_ID:
            total_res = total_res + self.get_all_testcase_info_under_testset(num)
        for i in total_res:
            if i['user-59'] == "FSIH" and i['user-06'] == "TDD specific":
                r3_tdd.append(i)
            elif i['user-59'] == "Airscale" and i['user-06'] == "TDD specific":
                r4_tdd.append(i)
            elif i['user-59'] == "Airscale" and i['user-06'] == "FDD specific":
                r4_fdd.append(i)

        print("====>  QC_SRAN20A_CIT_R3_TDD:  Total:%d"%len(r3_tdd))
        for i in r3_tdd:
            print("%s    %s    %s    %s"%(i['status'],i['user-03'],i['id'],i['name']))
        print("====>  QC_SRAN20A_CIT_R4_TDD:  Total:%d"%len(r4_tdd))
        for i in r4_tdd:
            print("%s    %s    %s    %s"%(i['status'],i['user-03'],i['id'],i['name']))
        print("====>  QC_SRAN20A_CIT_R4_FDD:  Total:%d"%len(r4_fdd))
        for i in r4_fdd:
            print("%s    %s    %s    %s"%(i['status'],i['user-03'],i['id'],i['name']))

if __name__ == "__main__":
    S = QC_REST_CLIENT()
    S.get_trunk_cit()



