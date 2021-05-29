# -*- coding:utf-8 -*-

import json
import os
import requests
import time

# 根据提供的批量模板图片，获取爬取结果


class Crawler:
    def __init__(self, t=0.1):
        self.time_sleep = t
    # 开始获取
    @staticmethod
    def get_images():
        img_url_list = []
        # 填写存放模板图片的文件夹名，文件夹放到根目录下
        path = './template'
        pictures = os.listdir(path)
        for picture in pictures:
            time.sleep(0.1)
            data = {
                'image': open(path + '/' + picture, 'rb')
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
            for info in resp_data_list:
                img_url = info["thumbUrl"]
                img_url_list.append(img_url)
        return img_url_list

    # 开始获取
    @staticmethod
    def save_images(img_urls):
        # 保存到项目下的pictures文件夹下，没有的时候自动创建
        if not os.path.exists("./pictures"):
            os.mkdir("./pictures")
        # 防止文件覆盖，获取文件夹内总量，确定顺序
        count = len(os.listdir('./pictures')) + 1
        for url in img_urls:
            time.sleep(0.1)
            try:
                pic_info = requests.get(url, timeout=10)
                fp = open('pictures\\' + str(count) + '.jpg','wb')
                fp.write(pic_info.content)
                fp.close()
                print("目标图片+1,已有" + str(count) + "张目标图片")
                count += 1
            except Exception as e:
                print(e)
                print("下载图片错误，详情查看错误信息")
                continue

        return

    def start(self):
        img_urls = self.get_images()
        self.save_images(img_urls)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.start()
