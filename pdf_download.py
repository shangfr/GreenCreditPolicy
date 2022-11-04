# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 15:39:55 2022

@author: shangfr
"""

import io
import requests
import pandas as pd


def download_pdf(save_path, pdf_name, pdf_url):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    response = requests.get(pdf_url, headers=send_headers)
    bytes_io = io.BytesIO(response.content)
    with open(save_path + "%s.PDF" % pdf_name, mode='wb') as f:
        f.write(bytes_io.getvalue())
        print('%s.PDF,下载成功！' % (pdf_name))


if __name__ == '__main__':

    df = pd.read_csv('data/节能与综合利用.csv', dtype=str)
    # df.columns
    save_path = 'pdf/'
    for index, row in df.iterrows():
        pdf_name = row['名称']+'-'+row['批次']
        pdf_url = row['名单']
        download_pdf(save_path, pdf_name, pdf_url)
