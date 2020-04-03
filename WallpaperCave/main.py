#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  AimerNeige

import requests
import re
import os

def search(keyword:'str') -> 'list':
    """
    :param keyword: 搜索关键词
    :return: 搜索结果，包含壁纸合集的信息，格式为字典列表
        '''
        "url": 壁纸合集链接
        "title": 壁纸合集标题
        "cover": 壁纸合集封面链接
        "number": 壁纸合集壁纸数
        '''
    """
    ret = []
    url = "https://wallpapercave.com/search?q={kw}".format(kw=keyword)
    response = requests.get(url)
    response.encoding='utf-8'
    html = response.text
    data_list = re.findall(r'<div id="popular">.*?<div id="footerc">', html, re.S)
    if len(data_list) != 1:
        print("Can't find the data, may the website has been changed.")
        return ret
    else:
        data = data_list[0]
    a_list = re.findall(r'<a.*?</a>', data, re.S)
    if len(a_list) <= 0:
        print("Can't find the a, you can try other keyword.")
        return ret
    for a in a_list:
        adict = {}
        # get the url
        url_list = re.findall(r'href="(.*?)"', a, re.S)
        if len(url_list) == 0:
            print("Can't find the url, may the website has been changed.")
            adict['url'] = ""
        else:
            url = url_list[0] # 通常会匹配到俩个，但是内容相同，直接取其中一个就好了
            url = "https://wallpapercave.com%s" % url
            adict['url'] = url
        # get the title
        title_list = re.findall(r'title="(.*?)"', a, re.S)
        if len(title_list) == 0:
            print("Can't find the title, may the website has been changed.")
            adict['title'] = ""
        else:
            title = title_list[2] # 通常会匹配到三个，前俩个内容相同，这里取第三个
            adict['title'] = title
        # get the cover
        cover_list = re.findall(r'src="(.*?)"', a, re.S)
        if len(cover_list) == 0:
            print("Can't find the cover, may the website has been changed.")
            adict['cover'] = ""
        else:
            cover = cover_list[0] # 通常只会匹配到一个
            adict['cover'] = cover
        # get the number
        number_list = re.findall(r'photos="(.*?)"', a, re.S)
        if len(number_list) == 0:
            print("Can't find the number, may the website has been changed.")
            adict['number'] = 0
        else:
            number = int(number_list[0])
            adict['number'] = number
        # add to ret
        ret.append(adict)
    return ret


def wallpaper_link(url:'str') -> 'list':
    """
    :param url: 壁纸合集的链接
    :return: 图片下载地址的信息构成的列表
        '''
        "download_link": 下载地址
        "src": 图片封面，分辨率较小
        '''
    """
    ret = []
    response = requests.get(url)
    response.encoding='utf-8'
    html = response.text
    data_list = re.findall(r'<div id="albumwp">.*?<div id="sidebar">', html, re.S)
    if len(data_list) != 1:
        print("Can't find the data, may the website has been changed.")
        return ret
    else:
        data = data_list[0]
    wallpaper_list = re.findall(r'<a class="download".*?class="wpimg"', data, re.S)
    if len(wallpaper_list) <= 0:
        print("Can't find the wallpaper, may the website has been changed.")
        return ret
    for wallpaper in wallpaper_list:
        wall_data = {}
        # get the download_link
        download_link_list = re.findall(r'<a class="download" href="(.*?)">', wallpaper, re.S)
        if len(download_link_list) != 1:
            print("Can't find the download, may the website has been changed.")
            wall_data['download'] = ""
        else:
            download_link = download_link_list[0]
            download_link = "https://wallpapercave.com%s" % download_link
            wall_data['download'] = download_link
        # get the src
        src_list = re.findall(r'src="(.*?)".*class="wpimg"', wallpaper, re.S)
        if len(src_list) != 1:
            print("Can't find the download, may the website has been changed.")
            wall_data['src'] = ""
        else:
            src = src_list[0]
            src = "https://wallpapercave.com%s" % src
            wall_data['src'] = src
        # add to ret
        ret.append(wall_data)
    return ret