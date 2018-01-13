# import requests
# import codecs
# import json
# f1 = codecs.open('/home/astha/lang_research/data/prod_keyword', 'r', 'utf-8')
# lines = f1.readlines()
# keyword = []
# for line in lines :
#     keyword.append(line.strip())
#
#
# url = "http://0.0.0.0:8080/keywords/"
#
# payload = "{ \"keywords\" : %s ,\n  \"Asin\" : \"hdhv\",\n  \"title\": \"Vintorio Wine Aerator Pourer - Premium Aerating Pourer and Decanter Spout (Black)\",\n  \"sort\" :  true\t\t\n}  " % json.dumps(keyword)
# headers = {
#     'Content-Type': "application/json",
#     'Cache-Control': "no-cache",
#     'Postman-Token': "6fadc267-a448-95a4-177e-3fd42c34afc8"
#     }
#
# response = requests.request("POST", url, data=payload, headers=headers)
#
# print(response.text)