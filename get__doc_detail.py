import json
import requests
import execjs
import time

from DESUtils import TripleDesUtils
from mongo_util import MyMongoDB

d_time = time.strptime(time.ctime())
v = str(d_time.tm_year) + str(d_time.tm_mon).zfill(2) + str(d_time.tm_mday)

with open("cipher.js") as f:
    js_text = f.read()

DES3 = TripleDesUtils()


def cipher():
    js_var = execjs.compile(js_text)
    ss = js_var.call('cipher')
    print(ss)
    enc = DES3.encryption(ss['timestamp'], ss['salt'], v)
    print(enc)
    dd_str = ss['salt'] + v + enc
    ciphertext = js_var.call('strTobinary', dd_str)
    print(ciphertext)
    return ciphertext, ss


def detail_spider(cookie, doc_id):
    mongo = MyMongoDB()
    if mongo.dbfind({"s5": doc_id}):
        print("{}已存在mongo".format(doc_id))
        return

    print("正在获取详情doc_id:", doc_id)
    url = "https://wenshu.court.gov.cn/website/parse/rest.q4w"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://wenshu.court.gov.cn',
        'Host': 'wenshu.court.gov.cn',
    }

    ciphertext, ss = cipher()
    post_data = {
        "docId": f"{doc_id}",
        "ciphertext": ciphertext,
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
        "__RequestVerificationToken": ss['salt'],
    }
    response = requests.post(url, headers=headers, data=post_data, cookies=cookie)
    if 'HTTP Status 503' in response.text:
        print('【服务器繁忙】,请重试')
        exit()
    data = json.loads(response.text)
    content = data.get('result')
    key = data.get('secretKey')
    iv = v
    res = DES3.decrypt(content, key, iv)
    print("结果:", res)

    mongo.insert(eval(res))
