# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:19:16 2022

@author: shangfr
"""
import re
import random
import pandas as pd
import streamlit as st
from tools import avp
from charts import render_china, render_radar,render_wordcloud, AgGrid,render_bar


st.set_page_config(page_title="Green_Credit", layout="wide")
st.sidebar.title("🥦 绿色金融")

@st.cache
def green_data(slct):
    url = 'data/data01.xlsx'
    data = pd.read_excel(url, slct)
    return data

@st.cache(allow_output_mutation=True)
def miit_data(slct):
    url = f'data/{slct}.csv'
    data = pd.read_csv(url)
    return data

@st.cache
def anyls_data():
    import pickle
    url = 'data/analysis_data.pkl'
    with open(url, 'rb') as f:
        analysis_data = pickle.load(f)
    return analysis_data
        
    
@st.cache
def get_avp(tle):
    data = avp(tle)
    return data['data']


@st.cache
def cmp_model(avp_data,agree):
    avp_tag = len(avp_data) > 0
    if agree and avp_tag:
        if  len(avp_data['avp']) > 25:
            g_value = "L1"
        else:
            g_value = "L2"
    elif agree:
        g_value = "L3"
    elif avp_tag:
        g_value = "L4"
    else:
        g_value = "L5"

    g_dict = {"L1": 3.5, "L2": 3.75, "L3": 3.85, "L4": 3.9, "L5": 3.95}
    g_delta = g_dict[g_value]
    

    if len(avp_data) > 0:
        if  len(avp_data['avp']) > 20:
            sa,sb = 80,100
        else:
            sa,sb = 70,90
    else:
        sa,sb = 50,70

    data_a = [random.randint(sa,sb) for i in range(6)]
    data_b = [80, 80, 80, 70, 60, 90]

    return data_a,data_b,g_value,g_delta

def stop(word=''):
    if len(word) == 0:
        st.stop()
        
        
def show_info():
    st.subheader("🗒️ 目录说明")
    col0,col1,col2 = st.columns(3)
    df = green_data('绿色产业指导目录')
    ctlg1 = df['一级目录'].unique()
    slct1 = col0.selectbox('一级目录', ctlg1)

    ctlg2 = df.loc[df['一级目录'] == slct1, '二级目录'].unique()
    slct2 = col1.selectbox('二级目录', ctlg2)

    gburl = 'https://std.samr.gov.cn/search/std?q='

    ctlg3 = df.loc[df['二级目录'] == slct2, '目录'].unique()
    slct3 = col2.selectbox('产业目录', ctlg3)

    ctlg4 = df.loc[df['目录'] == slct3, '说明'].unique()
    slct4 = ctlg4[0]
    
    st.markdown(slct4.replace("。", "。\n> "))
    products = slct4.replace("包括", "").replace(
        "和", "、").split('。')[0].split('、')
    st.multiselect('产品目录', products, products)

    ctlg5 = df.loc[df['说明'] == slct4, '国标'].unique()
    slct5 = ctlg5[0]
    if slct5 == '《）':
        slct6 = st.radio('标准目录：', ['无'])
    else:
        slct6 = st.radio('标准目录：', slct5.split("&"))
        pattern = re.compile(r'（([A-Z].*?\d+)）')
        st.markdown('[国标详情]('+gburl+pattern.findall(slct6)[0]+')')


def show_name_list():
    
    name_list = ['绿色工业园区名单', '绿色工厂名单', '绿色供应链管理示范企业名单','绿色设计产品名单']
    
    st.subheader(":bar_chart: 绿色示范企业统计")
    render_bar()
    st.markdown("---")
    col00, col01 = st.columns(2)
    col02, col03 = st.columns(2)
    
    col_list = [col00, col01,col02, col03]
    analysis_data = anyls_data()
    map_dict = analysis_data['map_dict']
    
    for index, item in enumerate(name_list):
        with col_list[index]:
            
            render_china(map_dict[item], '全国'+item.replace('名单', '分布'))
            st.markdown("---")
    
    st.subheader("🗒️ 绿色示范企业查询")
    col1, col2, col3  = st.columns(3)
    slct = col1.selectbox('名单查询', name_list)
    #df = green_data(slct)
    df = miit_data(slct)
    df.replace('新疆兵团','新疆', inplace = True)
    
    slct_pc = col2.selectbox('批次', [1,2,3,4,5,2021])
    df0 = df[df['批次'] == slct_pc]
    ctlg1 = df0['地区'].unique()
    slct1 = col3.selectbox('地区', ctlg1)
    df1 = df[(df['地区'] == slct1) & (df['批次'] == slct_pc)]

    st.info(f"{slct1}{slct.replace('名单','总数')}：{len(df1)}")
    st.dataframe(df1.drop(['序号','地区','批次'], axis = 1))


def show_tool():
    st.subheader("🗒️ 绿色企业申报")
    gkeywords = ["回收","节能","新能源","噪声","太阳能","储能","降噪","汽车充电设施","高性能","循环","除尘","环保设备","污染","环境监测","风力发电","废气","共享单车","热泵","节水","风能","能耗","环境影响","铁路建设","回收利用","水处理","生态修复","废旧","地铁","装配式建筑","减振","燃料电池","城市轨道交通","园林绿化","风力","低能耗","再生利用","清淤","废弃","再生","节约"]
    
    data = [
        {"name": name, "value": random.randint(200,1000)}
        for name in gkeywords
    ]
    with st.sidebar:
        st.markdown('[2022年度绿色制造名单申报](https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2022/art_3369f72687b447d799e6d155b9c7f20b.html)')
        render_wordcloud(data)
        st.markdown('---')
    
    name_list = ['绿色工厂','绿色设计产品','绿色工业园区',  '绿色供应链管理企业']
    
    search_cmp = st.text_input('企业名称:', '北京京东方显示技术有限公司')
    stop(search_cmp)
    avp_data = get_avp(search_cmp)
    if len(avp_data) > 0:
        st.info(avp_data['desc'])
        avp_df = pd.DataFrame(avp_data['avp'])
        with st.expander("企业详情："):
            outtxt = ''
            for t in avp_data['avp']:
                output = '`'+t[0]+'`'+':'+'`'+t[1]+'`'+'  \n'
                outtxt = outtxt + output
            st.markdown(outtxt)

    col0,col1 = st.columns([2,3])
    slct3 = col0.selectbox('申报项目', name_list)
    
    search_word = col1.text_input('绿色产品/服务：', 'LED')
    stop(search_word)

    df = green_data('绿色产业指导目录')
    result_df = df.loc[df['说明'].str.contains(search_word, regex=True)]
    # result_df
    if result_df.shape[0] > 0:
        ctlg1 = result_df['一级目录'].unique()
        slct1 = st.selectbox('信贷行业：', ctlg1)
    
        ctlg3 = result_df.loc[df['一级目录'] == slct1, '目录'].unique()
        slct3 = st.selectbox('资金用途：', ctlg3)
        ctlg4 = df.loc[df['目录'] == slct3, '说明'].unique()
        if len(ctlg4) > 0:
            slct4 = ctlg4[0]
            # st.subheader("目录说明")
            #st.markdown(slct4.replace("。","。\n> "))
            products = slct4.replace("包括", "").replace("和", "、").split('。')[0].split('、')
            slct16 = st.multiselect('产品清单：', products)
            stop(slct16)
            ctlg5 = df.loc[df['说明'] == slct4, '国标'].unique()
            slct5 = ctlg5[0]
            if slct5 == '《）':
                slct6 = st.radio('标准目录：', ['无'])
            else:
                slct6 = st.radio('标准目录：', slct5.split("&"))
            agree = st.checkbox('是否满足标准要求')
            st.file_uploader('补充资料', help='企业经营活动相关信息，包括经营票据、项目环评证书、合同信息、项目信息等')
            if st.button('申请'):
                st.success('申请成功，等待审核。')
                import time
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
    

                data_a,data_b,g_value,g_delta = cmp_model(avp_data,agree)
                
                col1, col2 = st.columns([1, 3])
                with col2:
                    render_radar(search_cmp, data_a, data_b)
                with col1:
                    st.metric(label="绿色等级预估：", value=g_value,
                              delta=f"{g_delta}%")
                    st.info('企业有绿色经营活动，符合《绿色产业指导目录（2019年版）》有关要求。')

    else:
        st.info('没有匹配到相关产品或服务！')

def show_policy():
    st.subheader("🗒️ 绿色金融政策列表")
    with open("data/政策.md", 'r', encoding='utf-8') as f:
        st.markdown(f.read())
    
    
def show_graph():
    st.subheader("🗒️ 绿色企业图谱")
    from PIL import Image
    image1 = Image.open('img/p1.png')
    image2 = Image.open('img/p2.png')
    col0, col1 = st.columns(2)
    col0.image(image1, caption='绿色判断图谱')
    col1.image(image2, caption='绿色产业链图谱')
    


def show_vs():
    st.markdown('[绿贷云](https://lhgf.lhcis.com/auth/login#banner)')
    st.markdown('[寰宇普惠](https://fintech.uniinclusive.com/)')

    
tools = ['查询', '申报', '图谱']
tool_opt = st.sidebar.selectbox('功能:', tools)
if tool_opt == tools[0]:
    opt_list = ['工信部绿色名单', '绿色产业指导目录', '绿色金融政策']
    slct = st.sidebar.selectbox('功能选择', opt_list)

    if slct == opt_list[1]:
        show_info()
    elif slct == opt_list[0]:
        show_name_list()
    elif slct == opt_list[2]:
        show_policy()
elif tool_opt == tools[1]:
    show_tool()
elif tool_opt == tools[2]:
    show_graph()
elif tool_opt == tools[3]:
    show_vs()
st.sidebar.markdown('---')
