# -*- coding:utf-8 -*-

import json
import os
import requests
import time

# open内第一个param放的是要识别的图片名称，把该图片放到项目根目录下
data = {
    'image': open("38a95e47314c8e328cb777595902b056.jpeg", 'rb')
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
# 地址中表明PC身份，否则返回的是提示下载百度APP的response
r = requests.post(
    'https://graph.baidu.com/upload?tn=pc&from=pc&image_source=PC_UPLOAD_IMAGE_MOVE&range={%22page_from%22:%20%22shituIndex%22}&extUiData%5bisLogoShow%5d=1',
    files=data, headers=headers).text
resp_json = json.loads(r)
# 目前标识在data中直接返回，如果未来被改掉，也可在data的url中找到
sign = resp_json["data"]["sign"]
resp = requests.get("https://graph.baidu.com/ajax/pcsimi?sign={}".format(sign)).text
resp_data_list = json.loads(resp)["data"]["list"]
# 保存到项目下的pictures文件夹下，没有的时候自动创建
if not os.path.exists("./pictures"):
    os.mkdir("./pictures")
# 防止文件覆盖，获取文件夹内总量，确定顺序
count = len(os.listdir('./pictures')) + 1

for info in resp_data_list:
    time.sleep(0.1)
    img_url = info["thumbUrl"]
    try:
        pic_info = requests.get(img_url, timeout=10)
        fp = open('pictures\\' + str(count) + '.jpg','wb')
        fp.write(pic_info.content)
        fp.close()
        print("目标图片+1,已有" + str(count) + "张目标图片")
        count += 1
    except Exception as e:
        print(e)
        print("下载图片错误，详情查看错误信息")
        continue
