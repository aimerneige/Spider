#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  AimerNeige

from urllib.request import urlretrieve
import requests
import time
import re
import os

rootPath = "/home/aimerneige/spider/pixiv/"

page = 1
while True:
    mainUrl = "https://www.ciyuanjie.cn/tag/pixiv" if page == 1 else "https://www.ciyuanjie.cn/tag/pixiv/page_%d.html" % page
    responseMain = requests.get(mainUrl)
    if responseMain.status_code != 200:
        print("404 Page Not Found")
        exit()
    responseMain.encoding = 'utf-8'
    htmlMain = responseMain.text
    artSrcList = re.findall(r'<ul class="update_area_lists cl" id="index_ajax_list">.*?</ul>', htmlMain, re.S)
    if len(artSrcList) == 0:
        print("Can't find the artSrc")
        continue
    artSrc = artSrcList[0]
    artItemList = re.findall(r'<div class="kzpost-data"><a href=".*?" target="_blank" title=".*?">', artSrc, re.S)
    if len(artItemList) == 0:
        print("Can't find artItem")
        continue
    print("Page Prase success", mainUrl)
    for artItem in artItemList:
        artUrlList = re.findall(r'<div class="kzpost-data"><a href="(.*?)" target="_blank" title=".*?">', artItem)
        if len(artUrlList) != 1:
            print("Can't find artUrl")
            continue
        artUrl = artUrlList[0]
        artUrl = "https://www.ciyuanjie.cn%s" % artUrl
        print("Articl Parse Success", artUrl)
        responseArticle = requests.get(artUrl)
        if responseArticle.status_code != 200:
            print("404 Artical Not Found")
            continue
        responseArticle.encoding = 'utf-8'
        htmlArticle = responseArticle.text
        imgSrcList = re.findall(r'<div class="content" id="content">.*?<div class="guest_down" id="Post_Down_Bottom">', htmlArticle, re.S)
        if len(imgSrcList) != 1:
            print("Can't find imgSrc")
            continue
        imgSrc = imgSrcList[0]
        imgItemList = re.findall(r'<img.*?/>', imgSrc, re.S)
        if len(imgItemList) == 0:
            print("Can't find imgItem")
            continue
        for imgItem in imgItemList:
            imgUrlList = re.findall(r'src="(.*?)"', imgItem, re.S)
            if len(imgUrlList) == 0:
                print("Can't find imgUrlList")
                continue
            imgUrl = imgUrlList[0]
            if requests.get(imgUrl).status_code != 200:
                print("404 Picture Not Found")
                continue
            imgTitleList = re.findall(r'alt="(.*?)"', imgItem, re.S)
            if len(imgTitleList) == 0:
                print("Can't find imgTitle")
                continue
            imgTitle = imgTitleList[0]
            imgTitle = imgTitle.replace(' ', '_')
            print("Picture Parse Success!", imgUrl)
            imgName = imgTitle + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".jpg"
            filePath = os.path.join(rootPath, imgName)
            if os.path.isfile(filePath):
                print("There has already a file with same name")
                continue
            urlretrieve(imgUrl, filePath)
            print("Download success!")
    page = page + 1