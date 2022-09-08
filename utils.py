# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:05:35 2022

@author: shangfr
"""

import pandas as pd

df_cmp = pd.read_excel('data/data00.xlsx', sheet_name='企业信息')
df_prd = pd.read_excel('data/data00.xlsx', sheet_name='产品信息')
df_patent = pd.read_excel('data/data00.xlsx', sheet_name='专利信息')
df_cide = pd.read_excel('data/data00.xlsx', sheet_name='词典')
