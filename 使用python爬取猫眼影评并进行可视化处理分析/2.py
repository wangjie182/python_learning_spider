# coding=utf-8

# 导入Map组件，用于生成地理坐标类图
# 导入Bar组件，用于生成柱状图
from pyecharts.charts import Map,Bar,Geo,Page
import json
from pyecharts import options as opts

# 导入Counter类，用于统计值出现的次数
from collections import Counter

def handle(cities):
    # 获取坐标文件中所有地名
    data = None
    with open(
            'C:/Users/Administrator/AppData/Local/Temp/pip-uninstall-a6xdz27r/pycharmprojects/yinhe/lib/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

    # print(len(data), len(data_new))

    # 写入覆盖坐标文件
    with open(
            'C:/Users/Administrator/AppData/Local/Temp/pip-uninstall-a6xdz27r/pycharmprojects/yinhe/lib/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str
# 获取评论中所有城市
cities = []
with open('C:/Users/Administrator/Desktop/使用python爬取猫眼影评并进行可视化处理分析/comments.txt', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        try:
            city = row.split(',')[2]
        except IndexError:
            pass
        if city != '':  # 去掉城市名为空的值
            cities.append(city)

# 对城市数据和坐标文件中的地名进行处理
handle(cities)

# 统计每个城市出现的次数
data = []
value = []
attr = []

for city in set(cities):
    data.append((city, cities.count(city)))
#数据超过94个时会报错，应该是有限制吧
data = Counter(cities).most_common(93)
value = [city[1] for city in data]
#确定最小值和最大值
max2 = value[0]
min2 = value[-1]
#将数值调整为可分段显示
if (max2-min2)%5!=0:
    max2 = max2 + (5-(max2-min2)%5)

# 使用Counter类统计出现的次数，并转换为元组列表
data_top25 = Counter(cities).most_common(25)
attr = [city[0] for city in data_top25]
value = [city[1] for city in data_top25]
max1 = value[0]
min1 = value[-1]

class Collector:
    charts = []

    @staticmethod
    def funcs(fn):
        Collector.charts.append((fn, fn.__name__))

C = Collector()

@C.funcs
def bar_base():
        c = (
            Bar()
            .add_xaxis(attr)
            #category_gap是指单系柱距离
            .add_yaxis("", value,category_gap="15%")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="《银河补习班》粉丝来源排行TOP25", subtitle="数据来源：猫眼",pos_left="400px"),
                visualmap_opts=opts.VisualMapOpts(min_=min1, max_=max1),
                #显示所有x值，不设置会自动隐藏一些x值
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0))
            )
        )
        return c
@C.funcs
def geo_base():
        c = (
            Geo()
            .add_schema(
                maptype="china"
                )
            .add("", [list(x) for x in data])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(is_piecewise=True,min_=min2, max_=max2),
                title_opts=opts.TitleOpts(title="《银河补习班》粉丝位置分布", subtitle="数据来源：猫眼",pos_left="300px"),
            )
        )
        return c

Page().add(*[fn() for fn, _ in C.charts]).render('C:/Users/Administrator/Desktop/使用python爬取猫眼影评并进行可视化处理分析/粉丝来源.html')

