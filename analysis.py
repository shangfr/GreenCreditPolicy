# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 10:04:58 2022

@author: shangfr
"""
import pickle
import pandas as pd
def miit_data(slct):
    url = f'data/{slct}.csv'
    data = pd.read_csv(url)
    return data


name_list = ['绿色工业园区名单', '绿色工厂名单', '绿色供应链管理示范企业名单','绿色设计产品名单']

bar_dict = {}

for n in name_list:
    df0 = miit_data(n)
    s0 = df0['批次'].value_counts().sort_index(ascending=True)
    bar_dict[n] = s0.values.tolist()

map_dict = {}
for n in name_list:
    df = miit_data(n)
    df.dropna(inplace=True)
    df_v = df['地区'].value_counts().to_frame().reset_index()
    df_v.columns = ['name', 'value']
    data_list = df_v.to_dict('records')
    map_dict[n] = data_list


analysis_data = {'bar_dict':bar_dict,'map_dict':map_dict}

url = 'data/analysis_data.pkl'
with open(url, 'wb') as f:
    pickle.dump(analysis_data, f)
    
with open(url, 'rb') as f:
    analysis_data2 = pickle.load(f)
    
     
