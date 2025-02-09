#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:懒得优化这一块
@Date       :2020/12/28 13:14:29
@Author     :JohnserfSeed
@version    :1.0
@License    :(C)Copyright 2017-2020, Liugroup-NLPR-CASIA
@Mail       :johnserfseed@gmail.com
'''

import re
import sys
import json
import Util
import getopt
import requests

# from retrying import retry


def printUsage():
    print('''
        使用方法: 1、添加为环境变量 2、输入命令
        -u<url 抖音复制的链接:https://v.douyin.com/JtcjTwo/>
        -m<music 是否下载音频,默认为yes可选no>
        -n<name 用于自定义视频文件名，默认不设置>

        例如：TikTokDownload.exe -u https://v.douyin.com/JtcjTwo/ -m yes -n 下载1

    ''')
# TikTokDownLoad.exe --url=<抖音复制的链接> --music=<是否下载音频,默认为yes可选no> --name=<用于自定义视频文件名，默认不设置>


def Find(string):
    # findall() 查找匹配正则表达式的字符串
    url = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url

def main():
    url = ""
    music = "yes"
    name = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:u:m:n:", [
                                    "url=", "music=", "name="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(-1)
    try:
        if opts == []:
            printUsage()
            url = str(input("请输入抖音链接:"))
            return url, music, name
    except:
        pass
    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            sys.exit(-1)
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-m", "--music"):
            music = arg
        elif opt in ("-n", "--name"):
            name = arg
    return url, music, name


# @retry(stop_max_attempt_number=3)
def download(video_url, music_url, video_title, music_title, headers, music, name):
    video_path = None
    music_path = None
    # 视频下载
    if video_url == '':
        print('[  提示  ]:该视频可能无法下载哦~\r')
        return
    else:
        try:
            r = requests.get(url=video_url, headers=headers)
        except Exception as e:
            print(f"下载链接异常，{url}",flush=True)
            return video_path,music_path
            pass
        if not Util.Status_Code(r.status_code):
            if video_title == '':
                video_title = '[  提示  ]:此视频没有文案_%s\r' % music_title
            video_title = Util.replaceT(video_title)
            music_title = Util.replaceT(music_title)
            if name == "":
                name = video_title
                pass
            video_path = f'{name}.mp4'
            with open(video_path, 'wb') as f:
                f.write(r.content)
                f.flush()
                print('[  视频  ]:%s.mp4 下载完成\r' % name,flush=True)
                pass

    if music_url == '':
        print('[  提示  ]:视频原声链接为空\r')
        # return
    else:
        # 原声下载
        if music != 'yes':
            print('[  提示  ]:不下载%s视频原声\r' % video_title)
            # return
        else:
            r = requests.get(url=music_url, headers=headers)
            music_path = f'{music_title}.mp3'
            with open(music_path, 'wb') as f:
                f.write(r.content)
                f.flush()
                print('[  音频  ]:%s.mp3 下载完成\r' % music_title)
    return video_path,music_path


def video_download(url, music, name, headers):
    try:
        r = requests.get(url=Find(url)[0])
        key = re.findall('video/(\d+)?', str(r.url))[0]
    except:
        print(f"视频链接不可用{url}",flush=True)
        return None,None
    # 官方接口
    # 旧接口22/12/23失效
    # jx_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={self.aweme_id[i]}'
    # 23/01/11
    # 此ies domian暂时不需要xg参数
    # 单作品接口 'aweme_detail'
    # 主页作品 'aweme_list'
    jx_url = Util.Urls().POST_DETAIL + Util.XBogus(
        f'aweme_id={key}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333').params

    js = Util.json.loads(Util.requests.get(
        url=jx_url, headers=headers).text)

    if js == '':
        input('[  提示  ]:获取视频数据失败，请从web端获取新ttwid填入配置文件填入配置文件\r')
        exit()

    try:
        video_url = str(js['aweme_detail']['video']['play_addr']
                        ['url_list'][2])  # .replace('playwm', 'play')  # 去水印后链接
    except:
        print('[  提示  ]:视频链接获取失败\r')
        video_url = ''
    try:
        music_url = str(js['aweme_detail']['music']['play_url']['url_list'][0])
    except:
        print('[  提示  ]:该音频目前不可用\r')
        music_url = ''
    try:
        video_title = str(js['aweme_detail']['desc'])
        music_title = str(js['aweme_detail']['music']['author']) + '创作的视频原声'
    except:
        print('[  提示  ]:标题获取失败\r')
        video_title = '视频走丢啦~'
        music_title = '音频走丢啦~'
        return None,None
    return download(video_url, music_url, video_title,
                music_title, headers, music, name)


# if __name__ == "__main__":
#     url, music, name = main()
#     # 获取命令行参数
#     cmd = Util.Command()
#     # 获取headers
#     headers = Util.Cookies(cmd.setting()).dyheaders
#     video_download(url, music, name, headers)
#     input('[  提示  ]:按任意键退出')
#     sys.exit()


if __name__ == "__main__":
    import os
    import shutil
    save_dir_path = "/Users/junqiangzhu/Desktop/ttvideo"
    os.makedirs(save_dir_path,exist_ok=True)
    VideoUrls = os.getenv("VideoUrls")
    print(VideoUrls,flush=True)
    with open(f"{save_dir_path}/downloadlist.txt","wb")as f:
        f.write(VideoUrls.encode())
        f.flush()
        pass

    # 获取命令行参数s
    cmd = Util.Command()
    
    def __getURls():
        urls = []
        with open(f"{save_dir_path}/downloadlist.txt","r")as f:
            lines = f.read().split("\n")
            for v in lines:
                for l in v.split(" "):
                    if l.startswith("https://"):
                        urls.append(l)
                    pass
                pass
            pass
        return urls
        pass
   
    def __dl(url):
        music = False
        name = ""
        
        # 获取headers
        headers = Util.Cookies(cmd.setting()).dyheaders
        video_path,music_path = video_download(url, music, name, headers)
        if video_path is not None:
            pass
        
        os.makedirs(save_dir_path,exist_ok=True)
        if video_path is not None:
            shutil.move(video_path,f"{save_dir_path}/{os.path.basename(video_path)}")
            pass
        pass
    
    urls = __getURls()
    for url in urls:
        __dl(url=str(url).strip())
        pass
    pass

# https://studio.ixigua.com/upload?from=post_article