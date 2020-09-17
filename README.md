# python_learning_spider
使用python爬取猫眼评论并用pyecharts进行数据可视化分析--bar,geo
原博客链接：[《使用python爬取猫眼评论并用pyecharts进行数据可视化分析--bar,geo》](https://blog.csdn.net/qq_32392597/article/details/96891236)
上次简单的爬取了一些榜单数据，并提取出想要的信息，这次想要将数据爬取下来后，使用pyecharts展示，简单搜了下pyecharts有很多教程，例如[《使用PYTHON抓取猫眼近10万条评论并分析》](https://www.cnblogs.com/mylovelulu/p/9511369.html)，本来是想直接copy了事，一运行发现报错很多。上了官网（https://github.com/pyecharts/pyecharts） 下载查看官方样例文档，发现我下载的是最新的V1.3的版本，相较V0.5x变化改动很多
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190722195658152.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyMzkyNTk3,size_16,color_FFFFFF,t_70)
比如之前搜到的教程中，柱状图的形成代码是：
```python
    # coding=utf-8
__author__ = '汤小洋'

# 导入Style类，用于定义样式风格
from pyecharts import Style
import json
# 导入Geo组件，用于生成柱状图
from pyecharts import Bar
# 导入Counter类，用于统计值出现的次数
from collections import Counter
# 定义样式
    style = Style(
        title_color='#fff',
        title_pos='center',
        width=1200,
        height=600,
        background_color='#404a59'
    )
# 根据城市数据生成柱状图
data_top20 = Counter(cities).most_common(20)  # 返回出现次数最多的20条
bar = Bar('《一出好戏》粉丝来源排行TOP20', '数据来源：猫眼-汤小洋采集', title_pos='center', width=1200, height=600)
attr, value = bar.cast(data_top20)
bar.add('', attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
        is_label_show=True)
bar.render('粉丝来源排行-柱状图.html')
```
但是新版本的提供的示例是
```python 
from pyecharts.charts import Bar
from pyecharts import options as opts

# V1 版本开始支持链式调用
bar = (
    Bar()
    .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
)
bar.render()
```
pyecharts 不再包括Style类，不能直接通过bar.add添加所需参数，但是官方提供的样例并没有解释所有参数，我只好又继续搜，但是大部分都是根据V0.5x的版本写的，无奈，，还是根据官方源文件 [bar.py](https://github.com/pyecharts/pyecharts/blob/master/pyecharts/charts/basic_charts/bar.py)  一个个对比参数看了,可以看到参数如下：
[【后续搜到这篇《python 可视化数据神器》，不过排版较乱，但是是最新的，也比较全】](http://www.360doc.com/content/19/0519/01/39068176_836620421.shtml)

```python 
 def add_yaxis(
        self,
        series_name: str,#名称
        yaxis_data: types.Sequence[types.Union[types.Numeric, opts.BarItem, dict]],
        *,#数值  ex: [['a',1],['b',2]]
        #名称和数值为必传参数
        is_selected: bool = True, #是否被选中显示
        xaxis_index: types.Optional[types.Numeric] = None,#使用x轴的index，在单个图表中存在多个x轴时有用
        yaxis_index: types.Optional[types.Numeric] = None,#y轴同上
        color: types.Optional[str] = None,
        stack: types.Optional[str] = None,#堆叠数据
        category_gap: types.Union[types.Numeric, str] = "20%", #单系柱距离
        gap: types.Optional[str] = None,#不同系柱距离
        label_opts: types.Label = opts.LabelOpts(), #数轴
        markpoint_opts: types.MarkPoint = None, #标记点
        markline_opts: types.MarkLine = None,#标记线
        tooltip_opts: types.Tooltip = None,#提示框组件
        itemstyle_opts: types.ItemStyle = None, #图元样式
    ):
```
数据的获取和存取我直接照搬了[《使用PYTHON抓取猫眼近10万条评论并分析》](https://www.cnblogs.com/mylovelulu/p/9511369.html)的代码，修改了获取地址和存储地址，原获取地址是：

> http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=0&startTime=2018-08-18%2022%3A25%3A03

1200486表示电影的专属id，offset表示偏移量；startTime表示获取评论的起始时间，从该时间向前取数据，即获取最新的评论
我本来直接在猫眼网站上找到这个地址，但是暂时找不到，干脆直接修改了id为1229534

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190722213219226.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyMzkyNTk3,size_16,color_FFFFFF,t_70)
我主要修改的是数据可视化代码,如下：
```python
#统计每个城市出现的次数
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
#将柱状图和地图在一个页面展示
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
                #interval=0显示所有x值，不设置会自动隐藏一些x值
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
            # data为list类型，必须将data中的字段都转化为列表并形成新的列表
            .add("", [list(x) for x in data])
            #is_show=False不显示坐标值
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(is_piecewise=True,min_=min2, max_=max2),
                title_opts=opts.TitleOpts(title="《银河补习班》粉丝位置分布", subtitle="数据来源：猫眼",pos_left="300px"),
            )
        )
        return c

Page().add(*[fn() for fn, _ in C.charts]).render('C:/Users/Administrator/Desktop/使用python爬取猫眼影评并进行可视化处理分析/粉丝来源.html')


```
最终展示结果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190722215726670.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyMzkyNTk3,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190722215745356.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyMzkyNTk3,size_16,color_FFFFFF,t_70)
文档链接：https://download.csdn.net/download/qq_32392597/11408369
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190813114400425.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyMzkyNTk3,size_16,color_FFFFFF,t_70)
