import time

from get__doc_detail import detail_spider
from get_doc_id_list import list_spider
from login import login

cookie = {'SESSION': str(login()[0][1])}

list_dict = list_spider(page=1, cookie=cookie)
result_count = int(list_dict["queryResult"]["resultCount"])
page_total = int(result_count/15) + 1
print("总共{}页".format(page_total))

for i in range(1, page_total+1):
    # 重试机制
    Attempts = 0
    Success = False
    while Attempts < 10 and not Success:
        try:
            # 查询第i页doc_id列表
            list_dict = list_spider(page=i, cookie=cookie)
            list_dict = list_dict["relWenshu"]
            Success = True
        except Exception as e:
            print(e)
            print("第{}页list_spider第{}次失败，正在重试~~~~~~".format(i, Attempts + 1))
            Attempts += 1
            if Attempts == 3:
                print("第{}页list_spider第{}次失败，不再重试~~~~~~".format(i, Attempts))
                break
    for doc_id in list_dict:
        # 重试机制
        attempts = 0
        success = False
        while attempts < 10 and not success:
            try:
                # 查询详情
                detail_spider(cookie=cookie, doc_id=doc_id)
                success = True
            except Exception as e:
                print(e)
                print("第{}次失败，正在重试~~~~~~".format(attempts+1))
                attempts += 1
                if attempts == 10:
                    print("第{}次失败，不再重试~~~~~~".format(attempts))
                    break
        print("sleep 10s")
        time.sleep(10)

