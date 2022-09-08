# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 10:02:53 2022

@author: shangfr
"""

# 半结构化数据挖掘AVP 知识抽取
import requests
from urllib.parse import quote, unquote


def avp(data='姚明'):
    url = 'https://api.ownthink.com/kg/knowledge?entity=' + quote(data)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"data": {}, "message": "error"}
