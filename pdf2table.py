# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 15:53:38 2022

@author: shangfr
"""

import os
import pandas as pd
import pdfplumber


def extract_tbl(save_path, csv_name, pdf_url):
    table_all = []
    pdf = pdfplumber.open(pdf_url)
    if csv_name.find('绿色设计产品名单') != -1:
        for page in pdf.pages:
            line_pos = min(r["top"] for r in page.rects)
            table = page.extract_table({
                "explicit_horizontal_lines": [ line_pos ]
            })
            #table = page.extract_table()
            table_all.extend(table)
            
        pdf.close()
    else:
        for page in pdf.pages:
            table = page.extract_table()
            table_all.extend(table)
            
        pdf.close()    
    if csv_name.find('绿色设计产品名单') != -1:
        df = pd.DataFrame(table_all)
    else:
        df = pd.DataFrame(table_all[1:], columns=table_all[0])
        colname = df.columns[0]
        df = df[~df[colname].str.contains(colname)]
    
    df['批次'] = file_name.replace('.PDF','').split('-')[1]
    tbl_csv_name = f"{save_path}{csv_name}"
    tbl_csv_name = tbl_csv_name.replace('PDF', 'csv')
    df = df.replace('\t','', regex=True).replace('\n','', regex=True)
    df.to_csv(tbl_csv_name, index=False)
    print(f'{tbl_csv_name}转换成功！')

def tidy_df(df):
    df = df[~df['0'].str.contains("附件.*?|绿色设计产品名单.*?")]
    df.reset_index(drop=True, inplace=True)
    
    groups = df[df['0'].isin(['序号'])].index.tolist()
    df_new = pd.DataFrame()
    for i,v in enumerate(groups):
        j = i+1
        if j >= len(groups):
            break
        else:
            v1 = groups[j]-3
            dff = df[v+1:v1]
            dff.insert(0, '种类', df.iloc[v-3,0])
            dff.insert(0, '适用评价标准', df.iloc[v-2,0]+str(df.iloc[v-2,1]))
            dff.insert(0, '绿色设计亮点', df.iloc[v-1,0]+str(df.iloc[v-1,1]))
            dff.columns = ['绿色设计亮点', '适用评价标准', '种类', '序号','企业名称','产品名称','产品型号','推荐单位', '其他', '批次']
        
        df_new = pd.concat([df_new,dff])
    df_new['地区'] = df_new['推荐单位'].apply(lambda x: str(x)[:2])
    df_new.loc[df_new['地区'] == '绿色', '地区'] = df_new.loc[df_new['地区'] == '绿色','企业名称'].apply(lambda x: str(x)[:2])
    df_new['适用评价标准'].replace('适用评价标准：','',regex=True, inplace=True)
    df_new['绿色设计亮点'].replace('绿色设计亮点：','',regex=True, inplace=True)
    df_new = df_new[['序号','企业名称','产品名称','产品型号','推荐单位','地区', '批次','种类','绿色设计亮点', '适用评价标准' ]]
    return df_new

if __name__ == '__main__':

    path = 'files/pdf/'
    save_path = 'files/csv/'
    for file_name in os.listdir(path):
        pdf_url = path+file_name
        extract_tbl(save_path, file_name, pdf_url)

    
    csv_files = os.listdir(save_path)
    
    csv_name_list = ['绿色工厂名单','绿色工业园区名单','绿色供应链管理示范企业名单','绿色设计产品名单']
    rename_dict1 = {'公司名称':'企业名称','单位名称':'企业名称','地 区':'地区','省市':'地区','省份':'地区','第三方机构':'第三方评价机构','第三方机构名称':'第三方评价机构','第三方评价机构名称':'第三方评价机构','园区名称':'园区'}
    rename_dict2 = {'公司名称':'企业名称','单位名称':'企业名称','地 区':'地区','省市':'地区','省份':'地区','第三方机构':'第三方评价机构','第三方机构名称':'第三方评价机构','第三方评价机构名称':'第三方评价机构','园区名称':'企业名称'}
    
    #name_dict = {}
    for csv_name in csv_name_list:
        df_all = pd.DataFrame()
        #col_list = []
        for file_name in csv_files:
            csv_url = save_path+file_name
            if csv_name in file_name:
                #print(csv_url)
                df = pd.read_csv(csv_url,dtype=str)
                #col_list.extend(df.columns)
                if '园区' in file_name:
                    df.rename(columns=rename_dict1,inplace=True)
                else:
                    df.rename(columns=rename_dict2,inplace=True)
                df_all = pd.concat([df_all,df])
                
        #name_dict[csv_name] = list(set(col_list))
        if csv_name == '绿色设计产品名单':
            df_all = tidy_df(df_all)
        tbl_csv_name = f"data/{csv_name}.csv"
        df_all.to_csv(tbl_csv_name, index=False)
        print(f'{tbl_csv_name}合并成功！')
