import requests
import json
import io
import random
import time
import re
import pyDes
import base64
import uuid
import sys
import os
import hashlib
from Crypto.Cipher import AES


class DailyCP:
    def __init__(self, schoolName="安徽理工大学"):
        self.key = "ST83=@XV"  # dynamic when app update
        self.session = requests.session()
        self.host = ""
        self.loginUrl = ""
        self.isIAPLogin = True
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
            # "X-Requested-With": "XMLHttpRequest",
            "Pragma": "no-cache",
            "Accept": "application/json, text/plain, */*",
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            # "User-Agent": "okhttp/3.12.4"
        })
        extension = {"deviceId": str(uuid.uuid4()), "systemName": "未来操作系统", "userId": "5201314",
                     "appVersion": "8.1.13", "model": "红星一号量子计算机", "lon": 0.0, "systemVersion": "初号机", "lat": 0.0}
        self.session.headers.update(
            {"Cpdaily-Extension": self.encrypt(json.dumps(extension))})
        self.setHostBySchoolName(schoolName)

    def setHostBySchoolName(self, schoolName):
        ret = self.request(
            "https://static.campushoy.com/apicache/tenantListSort")
        school = [j for i in ret["data"]
                  for j in i["datas"] if j["name"] == schoolName]
        if len(school) == 0:
            print("不支持的学校或者学校名称错误,以下是支持的学校列表")
            print(ret)
            exit()
        ret = self.request(
            "https://mobile.campushoy.com/v6/config/guest/tenant/info?ids={ids}".format(ids=school[0]["id"]))
        self.loginUrl = ret["data"][0]["ampUrl"]
        if ret == "":
            print("学校并没有申请入驻今日校园平台")
            exit()
        print("{name}的登录地址{url}".format(name=schoolName, url=self.loginUrl))
        self.host = re.findall(r"//(.*?)/", self.loginUrl)[0]

    def encrypt(self, text):
        k = pyDes.des(self.key, pyDes.CBC, b"\x01\x02\x03\x04\x05\x06\x07\x08",
                      pad=None, padmode=pyDes.PAD_PKCS5)
        ret = k.encrypt(text)
        return base64.b64encode(ret).decode()

    def passwordEncrypt(self, text: str, key: str):
        def pad(s): return s + (len(key) - len(s) %
                                len(key)) * chr(len(key) - len(s) % len(key))

        def unpad(s): return s[:-ord(s[len(s) - 1:])]
        text = pad(
            "TdEEGazAXQMBzEAisrYaxRRax5kmnMJnpbKxcE6jxQfWRwP2J78adKYm8WzSkfXJ"+text).encode("utf-8")
        aes = AES.new(str.encode(key), AES.MODE_CBC,
                      str.encode("ya8C45aRrBEn8sZH"))
        return base64.b64encode(aes.encrypt(text))

    def request(self, url: str, body=None, parseJson=True, JsonBody=True, Referer=None):
        url = url.format(host=self.host)
        if Referer != None:
            self.session.headers.update({"Referer": Referer})
        if body == None:
            ret = self.session.get(url)
        else:
            self.session.headers.update(
                {"Content-Type": ("application/json" if JsonBody else "application/x-www-form-urlencoded")})
            ret = self.session.post(url, data=(
                json.dumps(body) if JsonBody else body))
        if parseJson:
            return json.loads(ret.text)
        else:
            return ret

    def decrypt(self, text):
        k = pyDes.des(self.key, pyDes.CBC, b"\x01\x02\x03\x04\x05\x06\x07\x08",
                      pad=None, padmode=pyDes.PAD_PKCS5)
        ret = k.decrypt(base64.b64decode(text))
        return ret.decode()

    def checkNeedCaptcha(self, username):
        url = "https://{host}/iap/checkNeedCaptcha?username={username}".format(
            host=self.host, username=username)
        ret = self.session.get(url)
        ret = json.loads(ret.text)
        return ret["needCaptcha"]

    def generateCaptcha(self):
        # url = "https://{host}/iap/generateCaptcha?ltId={client}&codeType=2".format(host=self.host,client=self.client)
        # ret = self.session.get(url)
        # return ret.content
        pass

    def getBasicInfo(self):
        return self.request("https://{host}/iap/tenant/basicInfo", "{}")

    def login(self, username, password, captcha=""):
        if "campusphere" in self.loginUrl:
            return self.loginIAP(username, password, captcha)
        else:
            return self.loginAuthserver(username, password, captcha)

    def loginIAP(self, username, password, captcha=""):
        self.session.headers.update({"X-Requested-With": "XMLHttpRequest"})

        ret = self.session.get(
            "https://{host}/iap/login?service=https://{host}/portal/login".format(host=self.host)).url
        client = ret[ret.find("=")+1:]
        ret = self.request("https://{host}/iap/security/lt",
                           "lt={client}".format(client=client), True, False)
        client = ret["result"]["_lt"]
        # self.encryptSalt = ret["result"]["_encryptSalt"]

        body = {
            "username": username,
            "password": password,
            "lt": client,
            "captcha": captcha,
            "rememberMe": "true",
            "dllt": "",
            "mobile": ""
        }
        ret = self.request("https://{host}/iap/doLogin", body, True, False)
        if ret["resultCode"] == "REDIRECT":
            self.session.get(ret["url"])
            return True
        else:
            return False

    def checkNeedCaptchaAuthServer(self, username):
        ret = self.request("http://{host}/authserver/needCaptcha.html?username={username}&pwdEncrypt2=pwdEncryptSalt".format(
            username=username), parseJson=False).text
        return ret == "true"

    def loginAuthserver(self, username, password, captcha=""):
        ret = self.request(self.loginUrl, parseJson=False)
        body = dict(re.findall(
            r'''<input type="hidden" name="(.*?)" value="(.*?)"''', ret.text))
        salt = dict(re.findall(
            r'''<input type="hidden" id="(.*?)" value="(.*?)"''', ret.text))
        body["username"] = username
        body["dllt"] = "userNamePasswordLogin"
        if "pwdDefaultEncryptSalt" in salt.keys():
            body["password"] = self.passwordEncrypt(
                password, salt["pwdDefaultEncryptSalt"])
        else:
            body["password"] = password
        ret = self.request(ret.url, body, False, False,
                           Referer=self.loginUrl).url
        print(self.session.cookies)
        print("本函数不一定能用。")
        return True

    def getCollectorList(self):
        body = {
            "pageSize": 10,
            "pageNumber": 1
        }
        ret = self.request(
            "https://{host}/wec-counselor-collector-apps/stu/collector/queryCollectorProcessingList", body)
        return ret["datas"]["rows"]

    def getNoticeList(self):
        body = {
            "pageSize": 10,
            "pageNumber": 1
        }
        ret = self.request(
            "https://{host}/wec-counselor-stu-apps/stu/notice/queryProcessingNoticeList", body)
        return ret["datas"]["rows"]

    def confirmNotice(self, wid):
        body = {
            "wid": wid
        }
        ret = self.request(
            "https://{host}/wec-counselor-stu-apps/stu/notice/confirmNotice", body)
        print(ret["message"])
        return ret["message"] == "SUCCESS"

    def getCollectorDetail(self, collectorWid):
        body = {
            "collectorWid": collectorWid
        }
        return self.request("https://{host}/wec-counselor-collector-apps/stu/collector/detailCollector", body)["datas"]

    def getCollectorFormFiled(self, formWid, collectorWid):
        body = {
            "pageSize": 50,
            "pageNumber": 1,
            "formWid": formWid,
            "collectorWid": collectorWid
        }
        return self.request("https://{host}/wec-counselor-collector-apps/stu/collector/getFormFields", body)["datas"]["rows"]

    def submitCollectorForm(self, formWid, collectWid, schoolTaskWid, rows, address):
        body = {
            "formWid": formWid,
            "collectWid": collectWid,
            "schoolTaskWid": schoolTaskWid,
            "form": rows,
            "address": address,
            "uaIsCpadaily": True
        }
        ret = self.request(
            "https://{host}/wec-counselor-collector-apps/stu/collector/submitForm", body)
        print(ret["message"])
        return ret["message"] == "SUCCESS"

    def autoFill(self, rows):
        for item in rows:
            index = 0
            while index < len(item["fieldItems"]):
                if item["fieldItems"][index]["isSelected"] == 1:
                    index = index + 1
                else:
                    item["fieldItems"].pop(index)

    def getFormCharac(self, detail):
        ret = self.request(detail["content"], parseJson=False, JsonBody=False)
        return hashlib.md5(ret.content).digest().hex()

    def autoComplete(self, address, dbpath):
        collectList = self.getCollectorList()
        print(collectList)
        for item in collectList:
            # if item["isHandled"] == True:continue
            detail = self.getCollectorDetail(item["wid"])
            form = self.getCollectorFormFiled(
                detail["collector"]["formWid"], detail["collector"]["wid"])

            formpath = "{dbpath}/{charac}.json".format(
                charac=self.getFormCharac(item), dbpath=dbpath)
            if os.path.exists(formpath):
                with open(formpath, "rb") as file:
                    def find(l, key_valueList: list):
                        for item in l:
                            b = True
                            for k_v in key_valueList:
                                if item[k_v[0]] != k_v[1]:
                                    b = False
                            if b:
                                return item
                        return None

                    newForm = form
                    form = json.loads(file.read().decode("utf-8"))
                    for item in newForm:
                        l = find(form, [['title', item['title']], [
                                 'description', item['description']]])
                        item['value'] = l['value']
                        for fieldItemsList in item['fieldItems']:
                            field = find(l['fieldItems'], [
                                ['content', fieldItemsList['content']]])
                            fieldItemsList['isSelected'] = field['isSelected']
                    form = newForm
                    self.autoFill(form)

                self.submitCollectorForm(detail["collector"]["formWid"], detail["collector"]
                                         ["wid"], detail["collector"]["schoolTaskWid"], form, address)
            else:
                with open(formpath, "wb") as file:
                    file.write(json.dumps(
                        form, ensure_ascii=False).encode("utf-8"))
                    print("请手动填写{formpath}，之后重新运行脚本".format(formpath=formpath))
                    exit()

        confirmList = self.getNoticeList()
        print(confirmList)
        for item in confirmList:
            self.confirmNotice(item["noticeWid"])


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("python3 DailyCp.py 学校全名 学号 密码 定位地址 formdb文件夹绝对路径")
        exit()
    app = DailyCP(sys.argv[1])
    if not app.login(sys.argv[2], sys.argv[3]):
        exit()
    app.autoComplete(sys.argv[4], sys.argv[5])

# Author:HuangXu,FengXinYang,ZhouYuYang.
# By:AUST HACKER

# 2020/5/20 重要更新：修复登录过程，移除验证码（不需要），优化代码格式，感谢giteee及时反馈。
# 2020/5/28 更改为使用自动获取学校URL的方式，更改为使用参数形式，添加另一种登录形式AuthServer的支持(已完成但未测试)。感谢柠火的反馈。
# 2020/6/1 修复BUG，发现AuthServer的登录方式每个学校都不一样。支持任意表单内容自定义（详情见输出信息和formdb/1129.json）。感谢涅灵的反馈。
# 2020/6/2 AuthServer的登录网址不再使用硬编码的方式，理论上能支持所有学校了吧？感谢涅灵的反馈。
# 2020/6/17 修复crontab使用中相对路径的问题。识别form特征。
# 2020/7/5 浪费别人的时间是一种可耻的行为。
