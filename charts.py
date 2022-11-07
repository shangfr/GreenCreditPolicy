import json
from streamlit_echarts import Map
from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid

data_list_demo = [
    {"name": "北京市", "value": 4822023},
    {"name": "天津市", "value": 731449},
    {"name": "河北省", "value": 6553255},
    {"name": "山西省", "value": 2949131},
]


def render_bar():

    s_dict = {'绿色工业园区': [24, 22, 34, 39, 53, 52],
              '绿色工厂': [201, 208, 391, 602, 719, 662],
              '绿色供应链管理示范企业': [15, 4, 21, 50, 99, 107],
              '绿色设计产品': [193, 53, 489, 371, 1068, 989]}

    name_list = list(s_dict.keys())

    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {
            "data": name_list
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": ['第一批', '第二批', '第三批', '第四批', '第五批', '第六批'],
        },
        "series": [
            {
                "name": name_list[0],
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": s_dict[name_list[0]],
            },
            {
                "name": name_list[1],
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": s_dict[name_list[1]],
            },
            {
                "name": name_list[2],
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": s_dict[name_list[2]],
            },
            {
                "name": name_list[3],
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": s_dict[name_list[3]],
            },
        ],
    }
    st_echarts(options=options, height="300px")


def render_china(data_list, slct):
    formatter = JsCode(
        "function (params) {"
        + "var value = (params.value + '').split('.');"
        + "value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');"
        + "return params.seriesName + '<br/>' + params.name + ': ' + value;}"
    ).js_code

    with open("./data/China.json", "r", encoding='utf-8') as f:
        map = Map(
            "China",
            json.loads(f.read()),
            {
                "Hawaii": {"left": -110, "top": 28, "width": 5},
                "Puerto Rico": {"left": -76, "top": 26, "width": 2},
            },
        )
    options = {
        "title": {
            "text": slct,
            "subtext": "工业和信息化部网站",
            "sublink": "http://www.gov.cn/zhengce/zhengceku/bmwj/index.htm",
            "left": "left",
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
            "formatter": formatter,
        },
        "visualMap": {
            "left": "right",
            "top": "top",
            "min": 0,
            "max": max([d['value'] for d in data_list]),
            "inRange": {
                "color": [
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "toolbox": {
            "show": True,
            "left": "right",
            "top": "bottom",
            "feature": {
                "dataView": {
                    "show": True,
                },
                "restore": {
                    "show": True
                },
                "saveAsImage": {
                    "show": False
                }
            },
        },
        "series": [
            {
                "name": "value",
                "type": "map",
                "roam": True,
                "map": "China",
                "emphasis": {"label": {"show": True}},
                "textFixed": {"北京": [20, -20]},
                "data": data_list,
            }
        ],
    }
    st_echarts(options, map=map, height="500px")


def render_radar(cmp_a="企业A",
                 data_a=[30, 30, 20, 10, 50, 60],
                 data_b=[80, 80, 80, 70, 60, 90]):

    option = {
        "title": {"text": "企业绿色评价"},
        "legend": {"data": [cmp_a, "行业"]},
        "color": ['#00EE76', '#C0FF3E'],
        "radar": {
            "indicator": [
                {"name": "管理与规划", "max": 100},
                {"name": "绿色生产", "max": 100},
                {"name": "环境治理", "max": 100},
                {"name": "社会责任", "max": 100},
                {"name": "绿色制造", "max": 100},
                {"name": "绿色经营", "max": 100},
            ]
        },
        "series": [
            {
                "name": f"{cmp_a} vs 行业",
                "type": "radar",
                "data": [
                    {
                        "value": data_a,
                        "name": cmp_a,
                        "areaStyle": {},
                    },
                    {
                        "value": data_b,
                        "name": "行业",
                        "lineStyle": {
                            "type": 'dashed'
                        },
                    },
                ],
            }
        ],
    }

    st_echarts(option, height="500px")


def render_wordcloud(data):

    wordcloud_option = {"series": [
        {"type": "wordCloud", "data": data, 'color': '#00ae9d'}]}
    st_echarts(wordcloud_option)
