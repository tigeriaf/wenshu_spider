import json
import requests
import execjs
import time

from DESUtils import TripleDesUtils
from mongo_util import MyMongoDB

d_time = time.strptime(time.ctime())
v = str(d_time.tm_year) + str(d_time.tm_mon).zfill(2) + str(d_time.tm_mday)

js_text = """
function cipher() {
    var info = {};
	var date = new Date();
	var timestamp = date.getTime().toString();
	var salt = rand_str(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth()).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()).toString();
	var iv = year + month + day;
	info["timestamp"] = timestamp
	info["salt"] = salt
	info["iv"] = iv
	info["date"] = date
	return info

function rand_str(size){
        var str = "",
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        for(var i=0; i<size; i++){
            str += arr[Math.round(Math.random() * (arr.length-1))];
        }
        return str;
    }
};

function strTobinary(str) {
	var result = [];
	var list = str.split("");
	for (var i = 0; i < list.length; i++) {
		if (i != 0) {
			result.push(" ");
		}
		var item = list[i];
		var binaryStr = item.charCodeAt().toString(2);
		result.push(binaryStr);
	};
	return result.join("");
}
"""

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
