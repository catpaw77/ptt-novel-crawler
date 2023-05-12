# -*- coding: utf-8 -*-
from lxml import etree
import requests
import re
import os
import unicodedata
from requests.models import parse_header_links
from requests.utils import prepend_scheme_if_needed


def get_content(url):
    res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
    res = rs.get(base_url+link)
    res.encoding = 'utf-8'
    html = etree.HTML(res.text)
    content = html.xpath('//*[@id="main-content"]/text()')
    content = str(content)
    content = re.sub(r'\\xa0|\\r', '', content)
    content = re.sub(',|\'|\[|\]|\s', '', content)
    content = re.sub('\'', '', content)
    content = re.sub(r'\\n', '\n', content)
    return content


if __name__ == '__main__':
    base_url = 'https://www.ptt.cc'
    headers = {'cookie':  'over18 = 1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    payload = {
        'from': '/bbs/BB-Love/search?q=%E9%9D%9E%E5%B8%B8%E6%85%8B',
        'yes': 'yes'
    }
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
    res = rs.get(
        "https://www.ptt.cc/bbs/BB-Love/search?page=1&q=%E9%9D%9E%E5%B8%B8%E6%85%8B")
    res.encoding = 'utf-8'
    html = etree.HTML(res.text)
    links = html.xpath('//*[@id="main-container"]/div[2]/div/div[2]/a/@href')
    links.reverse()
    for link in links:
        res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
        res = rs.get(base_url+link)
        res.encoding = 'utf-8'
        html = etree.HTML(res.text)
        title = html.xpath('//*[@id="main-content"]/div[3]/span[2]/text()')
        title = re.sub(',|\'|\[|\]| ', '', str(title))
        content = get_content(base_url+link)
        print(title)
        with open('小說.txt', "a", encoding="UTF-8") as f:  # 保存小说
            f.write(str(title)+'\n')
            f.write(content)
