# -*- encoding: utf-8 -*-
# 自行百度安装chrome和chromedriver
# 配置文件中分别添加机器人的bot token（从bot father获取）和 频道id（格式为-100 后面跟频道信息中的id）
# 注意修改底部的chromedriver路径
import json
import os
import random
import re
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# 国内vps 需使用代理进行推送
# 以及把url_1 改为国内（服务器）可访问的镜像地址
proxies = {} # 举例 proxies = {"http": "http://127.0.0.1:123456"}
url_1 = "https://www.sehuatang.net/"
def get_content(web_url):
    if a == 2:
        while True:
            try:
                s = requests.get(web_url)
                # hostloc_content = etree.HTML(s.content).xpath('//td[@class="t_f"]/text()')
                hostloc_content = etree.HTML(s.content).xpath('//td[@class="t_f"]')[0]

                if len(hostloc_content) <= 0:
                    return "因权限原因，内容无法预览，请手动登陆查看！"
                else:
                    info = hostloc_content.xpath('string(.)')
                    findal = re.findall(r'本帖最后由.*编辑', info)
                    if findal:
                        info = info.replace(findal[0], "").lstrip()
                    s = ''
                    for j in info:
                        s = s + j
                    # 不展示全部内容，防止内容过长，严重影响体验
                    return s.replace("\r\n", '').replace('\n', '').replace('\xa0', '').replace('\u200b', '')[0:80]
            except Exception as e:
                print("网络原因，无法访问，请稍后再试...")
                return "因权限原因，内容无法预览，请手动登陆查看！"
    else:
        while True:
            try:
                browser.get(web_url)
                s = browser.page_source
                # hostloc_content = etree.HTML(s).xpath('//td[@class="t_f"]/text()')
                hostloc_content = etree.HTML(s).xpath('//td[@class="t_f"]')[0]

                if len(hostloc_content) <= 0:
                    return "因权限原因，内容无法预览，请手动登陆查看！"
                else:
                    info = hostloc_content.xpath('string(.)')
                    findal = re.findall(r'本帖最后由.*编辑', info)
                    if findal:
                        info = info.replace(findal[0], "").lstrip()
                    s = ''
                    for j in info:
                        s = s + j
                    # 不展示全部内容，防止内容过长，严重影响体验
                    return s.replace("\r\n", '').replace('\n', '').replace('\xa0', '').replace('\u200b', '')[0:80]

            except Exception as e:
                print("网络原因，无法访问，请稍后再试...")
                return "因权限原因，内容无法预览，请手动登陆查看！"


def mark_down(content):
    # 删除特殊符号，防止发生错误parse
    sign = ['&', '<', ".", '>', ' ', '?', '"', "'", '#', '%', '!', '@', '$', '^', '*', '(', ')', '-', '_', '+', '=',
            '~', '/', ',', ':', '’', '‘', '“', '”', '%', '^', '——', '{', '}', '*', '[', '、', ']', '`', '"', "'"]
    content = content.strip()
    content = content.replace("\n", "")
    for k in sign:
        content = content.replace(k, "\\" + k)
    return content


def post(chat_id: str, text: str, silent: bool = False, num=0):
    try:
        with requests.post(
                url=f'https://api.telegram.org/bot{bottoken}/sendMessage',
                headers={
                    'Content-Type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
                },
                data=json.dumps({
                    'chat_id': chat_id,
                    'text': text,
                    'parse_mode': 'MarkdownV2',
                    'disable_notification': silent,
                    'disable_web_page_preview': True,
                }),
                proxies=proxies
                ) as r:
            r.raise_for_status()
            return r.json()
    except Exception:
        print("推送失败！")
        if num > 10:
            return
        else:
            num += 1
        time.sleep(3)
        post(chat_id, text, num=num)


# 主程序
def master(r):
    xml_content = etree.HTML(r)
    href_list = xml_content.xpath('/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[2]/@href')
    author = xml_content.xpath('/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/text()')
    author_url = xml_content.xpath(
        '/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody/tr/td[2]/cite/a/@href')
    number = xml_content.xpath('/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody/tr/td[3]/a/text()')
    href = xml_content.xpath('/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[2]/text()')
    href_2 = xml_content.xpath('/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[3]/text()')
    # print(author)
    # print(number)
    for i in range(len(number)):
        href_id = href_list[i].split("tid=", )[-1].split("&", )[0]
        if not re.match(r'^\d+$', href_id):
            continue
        if str(href_id) not in tie_list:
            tie_list.append(str(href_id))
            name = href[i].replace("\r\n", "")
            if name == "隐藏置顶帖":
                print("这是啥东西")
                continue
            print(str(name) + "id:" + str(href_id))
            # 判断是否为权限贴
            if name == "New":
                name = href_2[i].replace("\r\n", "")
            else:
                pass
            # 文章链接
            # print(i)
            k = i + 1
            # print(k)
            url_list = url_1+"{}".format(href_list[i])
            # 作者id链接
            url_author = url_1+"{}".format(author_url[k])
            content_2 = mark_down(get_content(url_list))
            text = '\\[ 主        题 \\] ：' + "***{}***".format(
                mark_down(name)) + '\n' + '\\[ 用        户 \\] ：[{0}]({1})'.format(
                mark_down(author[i]),
                url_author) + '\n' + '\\[ 地        址 \\] ：[{0}]({1})'.format(str(href_id),
                                                                               url_list) + '\n' + '\\[ 内        容 ' \
                                                                                                  '\\]：[{}]'.format(
                content_2)
            # print(text)
            post(pid, text)
        else:
            pass
    add_list(tie_list)


def get_list():
    if not os.path.exists("./tielist.json"):
        file = open('./tielist.json', 'w')
        sehua_list = ["1035238", "1028441"]
        file.write(json.dumps(sehua_list))
        file.close()
    else:
        f = open("./tielist.json", encoding="utf-8")
        res = f.read()
        f.close()
        sehua_list = json.loads(res)
    return sehua_list


def add_list(content):
    f = open('./tielist.json', 'w')
    f.write(json.dumps(content))
    f.close()


# 读取配置文件
def get_con():
    if not os.path.exists("./98.json"):
        print("缺少配置文件")
        exit()
    else:
        f = open("./98.json", encoding="utf-8")
        res = f.read()
        f.close()
        config = json.loads(res)
        if config["bottoken"] == "机器人token" or config["pid"] == "-100后面跟你的频道id":
            print("请填写配置文件")
            exit()
        return str(config["bottoken"]), str(config["pid"])


# 获取配置
bottoken, pid = get_con()
# 获取已经发送的帖子列表
tie_list = get_list()
headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
}
# 可以改为其他镜像网站 或者其他分区，按这种格式写即可

url_sehua = url_1+"forum.php?mod=forumdisplay&fid=95&filter=author&orderby=dateline"

while True:
    try:
        # 网站不要求js验
        r = requests.get(url_sehua, headers=headers)
        xml_content = etree.HTML(r.content)
        href_list = xml_content.xpath(
            '/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[2]/@href')
        if href_list:
            a = 2
            print(a)
            master(r.content)
            time.sleep(random.randint(14, 24))
        else:
            a = 1
            print("js验证")
            # 网址
            # executable_path=r"/app/chromedriver"
            c_service = Service(r"/usr/local/bin/chromedriver")
            c_service.command_line_args()
            c_service.start()
            c_options = Options()
            # 无界面浏览器
            c_options.add_argument('--no-sandbox')
            c_options.add_argument('--headless')
            c_options.add_argument('--disable-gpu')
            # 修改为自己的chromedriver路径
            browser = webdriver.Chrome(service=c_service, options=c_options)

            browser.get(url_sehua)
            master(browser.page_source)
            browser.quit()
            c_service.stop()
            time.sleep(random.randint(15, 20))
    except Exception:
        print("网络错误，请稍后重试")
        time.sleep(60)
