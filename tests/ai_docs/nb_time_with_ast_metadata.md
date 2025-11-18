# markdown content namespace: nb_time Project Root Dir Some Files 


## File Tree


```

├── README.md
└── setup.py

```

---


## Included Files


- `README.md`

- `README.md`

- `setup.py`


---


--- **start of file: README.md** --- 



# 1 NbTime 介绍

`NbTime("2025-10-01 09:00:00", time_zone='America/Los_Angeles').to_tz('Asia/Shanghai').same_day_zero.get_str()`

## 1.0 安装 

pip install nb_time

## 1.1 NbTime 为什么好?

`nb_time` 是面向对象,入参兼容类型能力最强,万能时间字符串识别,时区支持优雅,无限链式调用,性能最好的时间处理工具包(性能超 `arrow` 三方包 700%).

`NbTime`类始终是时间操作的唯一入口,不像其他三方包或者用户自己封装的公用`utils/time_utils.py` 需要记忆选择几十种时间转换函数,`NbTime(x)`是一招鲜吃遍天.

`nb_time` 要做的是用户 `utils/time_utils.py` 的“终结者”.

为什么要写处理时间的包
```
开发中，关于处理时间转换虽然是一件不值一提很微不足道很小的事情，但也是一个常见的事情。
封装的不好的时间操作工具库，造成每次调用麻烦，和性能问题.
例如要调用不同的函数来处理 时间戳 时间字符串 时间对象之间的转换，
以及烦人的时区的转化，从一个时间种类变化到另一个时间类型形态，用户在中间过程要调用三四次不同的函数来转化，
才能处理得到想要的最终结果。

NbTime对象实例化入参接受所有种类的入参，不需要用户针对不同的传参类型做时间转化而选择不同的函数
，用户无脑将任意入参传给NbTime即可；NbTime将常用的时间处理转化结果，作为对象的惰性属性。
一个NbTime的实例化入参搞定所有时间转化需求，不需要用户亲自去选择各种用途的时间转换函数来对时间做转换。
```

## 1.2  time_utils.py  为什么很不好用?

例如像下面图片这种 模块级 + 各种各样的函数 封装的 时间工具包，就太不好用了，因为需要记忆和选择各种各样的不同用途的函数对时间进行转化。

封装时间操作不难，但如果封装的不好用，造成项目中调用它处处难。

那种 一个 time_utils.py 下 def 100 多个时间转换函数的 公共工具包，真的太难用了，用的时候都不知道选用什么函数好,。

1️⃣ 🧩 **一个NbTime类，终结 100+ 个函数**

❌ `time_utils.py`：用户要记忆：

- `str_date_to_timestamp()`
- `timestamp_to_date_str()`
- `get_timestamp_7d_ago()`
- `str_date_time_diff_day()`
- `timestamp_add_day_to_str_date_time()`
- ……（还有 90 多个）


![img_2.png](img_2.png)


## 1.3 NbTime的优点?
```
NbTime 是oop面向对象开发的爽快的日期时间操作类
NbTime 支持无限链式操作来处理时间,
(因为是oop所以易用程度远远的暴击面向过程python工程师写的time_utils.py里面
写几百个独立的操作时间的面向过程函数)

NbTime 入参支持 None 字符串 时间戳 datetime对象 NbTime对象自身 arrow.Arrow对象
NbTime 支持将任意格式的时间字符串转成时间对象，无需提前精确指定写 yyyyy-mm-dd HHMMSS 这样的模板。
NbTime 非常轻松支持时区转化
Nbtime 内置属性 datetime对象,兼容性好
Nbtime 内置 to_arrow 方法,一键转换成arrow.Arrow对象

NbTime操作时间,远远暴击使用datetime和三方arrow包,
远远暴击用户在 utils.time_utils.py文件中写几百个孤立的面向过程操作时间的函数.
```

## 1.4 nb_time 🆚 与主流库对比

| 维度               | `datetime` 标准库 | `arrow`           | `pendulum`        | `nb_time`（你）         |
|--------------------|-------------------|-------------------|-------------------|--------------------------|
| 易用性             | ❌ 低             | ✅ 高             | ✅ 高             | ⭐⭐⭐⭐⭐ 极高              |
| 链式操作           | ❌ 无             | ✅ 支持           | ✅ 支持           | ✅✅✅ 更自然             |
| 时区处理           | ⚠️ 复杂           | ✅ 好             | ✅ 很好           | ⭐⭐⭐⭐⭐ 最智能           |
| 入参兼容性         | ❌ 严格           | ✅ 较好           | ✅ 好             | ⭐⭐⭐⭐⭐ 万能             |
| 性能               | ⭐⭐⭐⭐⭐ 最快       | ⭐⭐ 慢            | ⭐⭐⭐ 中等         | ⭐⭐⭐⭐ 很快（超 arrow）  |
| 可扩展性（继承）   | ❌ 难             | ⚠️ 有限           | ⚠️ 有限           | ⭐⭐⭐⭐⭐ 完美支持         |
| 学习成本           | ⭐⭐⭐ 中           | ⭐⭐ 低            | ⭐⭐ 低            | ⭐ 极低（NbTime(x) 万能）|

# 2 NbTime 时间值传参用法

NbTime 最方便的地方在于入参可以是任何种类，可以不传参；可以传递数字时间戳，自动识别是否是毫秒时间戳；

可以传递datetime对象；可以传递NbTime类型的对象；

可以传递时间字符串，而且可以自动把任何格式模板的时间字符串自动转化成NbTime对象；

综上所述NbTime入参方式已经囊括了所有可能。

所以用户始终用NbTime就可以了，无需记忆和选择几百个各种各样的时间转换函数。

不管是从 时间戳 时间字符串 datetime对象 以及不同时区 的之间互相转化，都是使用 NbTime 对象作为中转对象。

## 2.1 NbTime 不传参,就是当前时间
```
>>> from nb_time import NbTime
>>> NbTime()                   
<NbTime [2024-02-29 17:51:14 +0800]>
```

## 2.2 NbTime 传参datetime对象

```
>>> NbTime(datetime.datetime.now())
<NbTime [2024-02-29 17:56:43 +0800]>
```

## 2.3 NbTime 传参时间戳
```
>>> NbTime(1709192429)
<NbTime [2024-02-29 15:40:29 +0800]>
```

传了大于13位的毫秒时间戳，也能自动转化。
```
>>> NbTime(1709192429000)
<NbTime [2024-02-29 15:40:29 +0800]>
```


## 2.4 NbTime 传参字符串,可以对字符串设置时区,例如把东七区的时间字符串转化成东8区的格式.
```
>>> NbTime('2024-02-26 15:58:21',datetime_formatter=NbTime.FORMATTER_DATETIME,time_zone=NbTime.TIMEZONE_EASTERN_7).to_tz('UTC+8')
<NbTime [2024-02-26 16:58:21 +0800]>
```

## 2.4.b Nbtime 万能自动识别时间字符串模板，可以将所有常见的时间字符串转换成时间对象

Nbtime 万能自动识别时间字符串模板，可以将所有常见的时间字符串转换成时间对象，不需要提前精确的写 yyyy-mm-dd 这样的。

以下例子都能直接转化成时间对象，无视时间字符串格式。

```python
from nb_time import NbTime
print(NbTime('20230506T010203.886 +08:00'))
print(NbTime('2023-05-06 01:02:03.886'))
print(NbTime('2023-05-06T01:02:03.886 +08:00'))
print(NbTime('20221206 1:2:3'))
print(NbTime('Fri Jul 19 06:38:27 2024'))
print(NbTime('2013-05-05 12:30:45 America/Chicago'))
```

## 2.5 NbTime 传参 DateTimeValue类型对象
```
>>> from nb_time import DateTimeValue
>>> NbTime(DateTimeValue(year=2022,month=5,day=9,hour=6),time_zone='UTC+7')
<NbTime [2022-05-09 06:00:00 +0700]>

```

## 2.6 NbTime传参 NbTime对象

NbTime入参本身支持无限嵌套NbTime对象
```
NbTime(NbTime(NbTime(NbTime())))
<NbTime [2024-02-29 18:39:09]>


为什么 NbTime支持入参是自身类型,例如你可以方便的转时区和转字符串格式化
例如0时区的2024-02-29 07:40:34,你要转化成8时区的带毫秒带时区的时间字符串,
>>> from nb_time import NbTime                                                                                                    
>>> NbTime(NbTime('2024-02-29 07:40:34', time_zone='UTC+0', datetime_formatter=NbTime.FORMATTER_DATETIME_NO_ZONE),
...                time_zone='UTC+8', datetime_formatter=NbTime.FORMATTER_MILLISECOND).datetime_str
'2024-02-29 15:40:34.000000 +0800'
```

## 2.7 NbTime传参 arrow.Arrow对象
```
>>> NbTime(arrow.now())
<NbTime [2025-09-09T12:32:58+0800] (Asia/Shanghai)>
```
# 3 NbTime 链式计算时间

NbTime().shift方法返回的对象仍然是Nbtime类型。
因为Nbtime对象本身具有很多好用的属性和方法，所以使用NbTime作为时间转化的中转对象，比使用datetime作为中转对象方便使用很多。


求3天1小时10分钟后的时间,入参支持正数和负数
```
>>> NbTime().shift(hours=1,minutes=10).shift(days=3)
<NbTime [2024-03-03 19:02:49 +0800]>
```

求当前时间1天之前的时间戳
```commandline
>>> NbTime().shift(days=-1).timestamp
1709290123.409756

```

`arrow`和`nb_time`之间无限链式转化
```
>>> NbTime().arrow.ceil('day').to_nb_time()
<NbTime [2025-09-09T23:59:59+0800] (UTC+8)>

```





# 3 NbTime 时区设置

## 3.1 NbTime 实例化时候设置时区

实例化时候分别设置东7区和0时区
```
>>> NbTime(time_zone='UTC+7')
<NbTime [2024-02-29 17:05:08 +0700]>
>>> NbTime(time_zone='UTC+0') 
<NbTime [2024-02-29 10:05:08 +0000]>
```

## 3.2 全局设置时区
用户不传递时区时候,默认就是操作系统时区,如果用户想统一设置时区

例如用户统一设置东8区,以后实例化就不用每次亲自传递东八区.
```
NbTime.set_default_time_zone('UTC+8')
```

# 4 设置时间字符串格式化

## 4.1 NBTime实例化时候设置时间字符串格式
用户不想要毫秒时间字符串
```
>>> NbTime(datetime_formatter=NbTime.FORMATTER_DATETIME)    
<NbTime [2024-02-29 18:10:57 +0800]>
```

用户不想要字符串带时区
```
>>> NbTime(datetime_formatter=NbTime.FORMATTER_DATETIME_NO_ZONE) 
<NbTime [2024-02-29 18:12:18]>
```

##  4.2 NBTime全局设置字符串格式

NbTime.set_default_formatter 可以全局设置时间格式字符串,就不需要每次都传递格式
```
>>> NbTime.set_default_formatter(NbTime.FORMATTER_DATETIME_NO_ZONE)
>>> NbTime()
<NbTime [2024-02-29 18:14:38]>
```

# 5 NbTime 对象内置的成员属性

见下面的交互,NbTime类型对象有非常便捷的各种成员变量,

```
datetime  类型datetime.datetime类型的时间对象,这个很方便和内置类型关联起来
time_zone_obj 时区
datetime_str 日期时间字符串
time_str 时间字符串
date_str 日期字符串
timestamp  时间戳秒
timestamp_millisecond 时间戳毫秒
today_zero_timestamp 当天凌晨的时间戳
arrow  arrow.Arrow对象
```

```
from nb_time import NbTime
>>> nbt=NbTime()
>>> nbt.datetime
datetime.datetime(2024, 2, 29, 18, 16, 23, 541415, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

>>> nbt.time_zone_obj
<DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>

>>> nbt.datetime_str
'2024-02-29 18:16:23'

>>> nbt.time_str
'18:16:23'

>>> nbt.date_str
'2024-02-29'

>>> nbt.timestamp
1709201783.541415

>>> nbt.timestamp_millisecond
1709201783541.415

>>> nbt.today_zero_timestamp
1709136000


>>> nbt.arrow
<Arrow [2025-09-09T13:01:17.526580+08:00]>
```

# 6 NbTime的方法

## 6.1 get_str 方法转化成任意字符串格式
```
例如获取今天的年月日,中间不要带 - 
>>> NbTime().get_str('%Y%m%d')
20240301
```

## 6.2 shift 是计算生成新的NbTime对象,支持无限连续链式操作
```
求3天1小时10分钟后的时间,入参支持正数和负数
>>> NbTime().shift(hours=1,minutes=10).shift(days=3)
<NbTime [2024-03-03 19:02:49 +0800]>
```

## 6.3 to_tz 是生成新的时区的NbTime对象,把NbTime对象转化成另一个时区.
```
一个东7区的时间:
>>> NbTime('2024-02-26 15:58:21',datetime_formatter=NbTime.FORMATTER_DATETIME,time_zone=NbTime.TIMEZONE_EASTERN_7)
<NbTime [2024-02-26 15:58:21 +0700]>

那这个东7区的时间转化成东8区的时间:
>>> NbTime('2024-02-26 15:58:21',datetime_formatter=NbTime.FORMATTER_DATETIME,time_zone=NbTime.TIMEZONE_EASTERN_7).to_tz('UTC+8')
<NbTime [2024-02-26 16:58:21 +0800]>
```

### 6.3.2 两种时区转化写法

例如东7区的2024-02-29 07:40:34转成东八区的时间字符串。

```python
from nb_time import  NbTime

# NbTime对象无限嵌套传参给NbTime方式
print(NbTime(NbTime('2024-02-29 07:40:34', time_zone='UTC+7'), time_zone='UTC+8').datetime_str)

# to_tz 方式
print(NbTime('2024-02-29 07:40:34', time_zone='UTC+7').to_tz('UTC+8').datetime_str)
```

## 6.4 NbTime 对象 支持 > < = 比较
```
NbTime 实现了 __gt__  __lt__  __eq__ 方法,可以直接比较大小

>>> NbTime() > NbTime('2023-05-06 01:01:01')                                            
True
>>> NbTime() > NbTime('2025-05-06 01:01:01') 
False

```
## 6.5 NbTime 转换为 arrow.Arrow对象

```
>>> nt=NbTime()
>>> nt.to_arrow()
<Arrow [2025-09-09T12:34:37.661360+08:00]>
```

## 6.6 NbTime humanize 方法,转人类自然语言
```
>>> NbTime().humanize()
'just now'

>>> NbTime().shift(days=5).humanize()
'in 5 days'

>>> NbTime().shift(days=-3).humanize() 
'3 days ago'
```

# 7.用户自定义继承 NbTime 类

因为 nb_time 是 oop面向对象开发的,所以可以继承,
如果是面向过程编程,使用模块级 + 函数的方式来编程,先改变模块的某个全局变量或者函数逻辑,只能使用猴子补丁技术,而且模块天然还是个单例,不适合多次猴子补丁
面向对象就是有优势.


## 7.1 例如用户想使用 UTC 0时区,但是不想频繁传递 时区入参,可以使用 nb_time的  自带的UtcNbTime 类,或者用户手写这个类自己继承NbTime

```python
class UtcNbTime(NbTime):
    default_time_zone = NbTime.TIMEZONE_UTC

# 使用的时候
UtcNbTime()   
```


## 7.2 例如 用户想使用上海时区,并且默认使用不带时区的时间字符串格式化
```python
class ShanghaiNbTime(NbTime):
    default_time_zone = NbTime.TIMEZONE_ASIA_SHANGHAI
    default_formatter = NbTime.FORMATTER_DATETIME_NO_ZONE

# 使用的时候
ShanghaiNbTime()  
```

## 7.3 数据分析,常用的时间也可以加上来

```python
class PopularNbTime(NbTime):
    @property
    def ago_1_days(self):
        return self.shift(days=-1)

    @property
    def ago_7_days(self):
        return self.shift(days=-7)

    @property
    def ago_30_days(self):
        return self.shift(days=-30)

    @property
    def ago_180_days(self):
        return self.shift(days=-180)
```

# 8 nb_time 性能暴打 arrow 700%
```python
for i in range(1000000):
    NbTime(time_zone='Asia/Shanghai') # 3秒100万次
    # arrow.now(tz='Asia/Shanghai')   # 20秒100万次
```

# 9 演示最差劲的 utils/time_utils.py

**一个“教科书级屎山时间工具包”**    

❌ 所有函数都是面向过程、无封装、无链式  
❌ 每个函数只做“半件事”，用户必须组合 3~4 个函数才能完成一个转换  
❌ 参数命名模糊、格式不统一、文档缺失   
❌ 时区处理靠“猜”和“硬编码数字”  
❌ 同一个功能有 5 个名字类似的函数，行为略有不同  
❌ 不处理异常、不校验输入、出错静默或崩溃   
❌ 大量重复代码、魔法数字、全局变量污染   
❌ 依赖系统本地时区，跨环境行为不一致   
❌ 支持“多种格式”，但用户得自己查源码才知道支持哪些     

💣 最差劲 time_utils.py 出炉！  
```python
# time_utils.py —— 地狱级时间工具包
# 作者：时间混乱之神
# 警告：使用本文件可能导致脱发、失眠、离职

import time
from datetime import datetime, timedelta

# 全局变量，假装是配置，其实是隐藏炸弹
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SYSTEM_TZ_OFFSET = -time.timezone // 3600  # 依赖运行环境！东8区服务器=8，洛杉矶=-7

# =================== 字符串解析区（每个函数只解析一种格式） ===================

def parse_time_str_type1(s):
    # 只支持 "2025-04-05 14:30:00"
    return time.strptime(s, "%Y-%m-%d %H:%M:%S")

def parse_time_str_type2(s):
    # 只支持 "2025/04/05 14:30"
    return time.strptime(s, "%Y/%m/%d %H:%M")

def parse_time_str_type3(s):
    # 只支持 "04-05-2025"
    return time.strptime(s, "%m-%d-%Y")

def parse_time_str_universal(s):
    # “通用”但只 try 3 种，失败就崩溃
    for fmt in ["%Y-%m-%d", "%d/%m/%Y %H:%M", "%Y年%m月%d日"]:
        try:
            return time.strptime(s, fmt)
        except:
            continue
    raise Exception("老子解析不了，你自己看着办")

# =================== 时间结构体 → 时间戳 （但有时区坑） ===================

def struct_time_to_timestamp_utc(st):
    # 输入 struct_time，返回 UTC 时间戳？不！是本地时间戳！
    return int(time.mktime(st))

def struct_time_to_timestamp_assume_utc(st):
    # 假装 st 是 UTC，但 mktime 是本地……所以错了
    return int(time.mktime(st)) - SYSTEM_TZ_OFFSET * 3600

def struct_time_to_timestamp_with_offset(st, offset_hours):
    # offset_hours 是什么？正负？文档？不存在的
    return int(time.mktime(st)) - offset_hours * 3600

# =================== 时间戳 → struct_time ===================

def timestamp_to_struct_local(ts):
    return time.localtime(ts)

def timestamp_to_struct_utc(ts):
    return time.gmtime(ts)

# =================== struct_time → 字符串 ===================

def struct_time_to_str_format1(st):
    return time.strftime("%Y-%m-%d %H:%M:%S", st)

def struct_time_to_str_format2(st):
    return time.strftime("%Y/%m/%d %H点%M分", st)

def struct_time_to_str_custom(st, fmt):
    return time.strftime(fmt, st)

# =================== 时区转换（靠猜） ===================

def convert_timestamp_from_tz7_to_tz8(ts):
    # 硬编码 +3600，假装专业
    return ts + 3600

def convert_timestamp_by_offset_diff(ts, from_offset, to_offset):
    # 文档？参数顺序？谁记得
    return ts + (to_offset - from_offset) * 3600

def convert_string_timezone_manual(s, from_tz_num, to_tz_num):
    # 用户必须自己：1.选解析函数 2.转时间戳 3.调此函数 4.再转回字符串
    st = parse_time_str_type1(s)  # 假设格式对
    ts = struct_time_to_timestamp_utc(st)
    ts2 = convert_timestamp_by_offset_diff(ts, from_tz_num, to_tz_num)
    st2 = timestamp_to_struct_local(ts2)
    return struct_time_to_str_format1(st2)

# =================== “便捷”函数（其实更麻烦） ===================

def get_current_time_in_tz8_str():
    # 返回“当前东八区时间字符串”，但依赖服务器时区！
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_current_timestamp_in_utc():
    return int(time.time())

def add_days_to_timestamp(ts, days):
    return ts + days * 86400

def add_hours_to_struct_time(st, hours):
    # struct_time 是只读的！必须转成 datetime 才能加！但用户不知道！
    dt = datetime(*st[:6])
    dt2 = dt + timedelta(hours=hours)
    return dt2.timetuple()  # 返回 struct_time，但丢失微秒和时区！

# =================== 隐藏陷阱函数 ===================

def quick_convert(s):
    # 名字很诱人，行为很随机
    if "-" in s:
        st = parse_time_str_type1(s)
    elif "/" in s:
        st = parse_time_str_type2(s)
    else:
        st = parse_time_str_universal(s)
    ts = struct_time_to_timestamp_utc(st)
    ts += 3600  # 假装转东8区
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))

# =================== 多余函数（制造选择困难） ===================

def str_to_timestamp_method_a(s): return struct_time_to_timestamp_utc(parse_time_str_type1(s))
def str_to_timestamp_method_b(s): return struct_time_to_timestamp_assume_utc(parse_time_str_type1(s))
def str_to_timestamp_method_c(s): return struct_time_to_timestamp_with_offset(parse_time_str_type1(s), 8)

# =================== 彩蛋：全局状态污染 ===================

_last_parsed_time = None  # 所有函数偷偷修改它，用于“调试”

def parse_and_remember(s):
    global _last_parsed_time
    st = parse_time_str_type1(s)
    _last_parsed_time = st
    return st

# =================== 文档？不存在的 ===================

# 没有类型提示
# 没有 docstring
# 没有示例
# 没有测试
# 只有注释：“以后再改”、“临时方案”、“别动这个！！！”
```

🧩用户使用示例（东7区时间字符串 → 东8区时间字符串):  

```python
from time_utils import *

input_str = "2025-04-05 14:30:00"

# Step 1: 解析字符串 → struct_time
st = parse_time_str_type1(input_str)  # 如果格式不对？崩溃！

# Step 2: struct_time → 时间戳（但这是本地时间戳！坑！）
ts = struct_time_to_timestamp_utc(st)

# Step 3: 手动加3600秒，假装时区转换
ts_east8 = ts + 3600

# Step 4: 时间戳 → struct_time（本地时区！再次依赖服务器！）
st_east8 = timestamp_to_struct_local(ts_east8)

# Step 5: struct_time → 字符串
output_str = struct_time_to_str_format1(st_east8)

print(output_str)  # 可能是 "2025-04-05 15:30:00" —— 如果服务器在东8区！
                   # 如果在洛杉矶？→ 输出错误时间！
```

# 10 真实场景对比 
需求：把东7区的字符串时间，转成东8区，再减3天，取当天0点的毫秒时间戳

**❌ 传统地狱模式（5-7行，并且要查文档）**
```python
dt_str = "2024-02-26 15:58:21"
dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
dt = dt.replace(tzinfo=pytz.timezone("Etc/GMT-7"))
dt = dt.astimezone(pytz.timezone("Asia/Shanghai"))
dt = dt - timedelta(days=3)
dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
result = int(dt.timestamp() * 1000)
```

**✅ NbTime心流模式 (一行链式搞定,不会出错)**
```python
result = NbTime("2024-02-26 15:58:21", time_zone='UTC+7').to_tz('UTC+8').shift(days=-3).same_day_zero.timestamp_millisecond
```

# 20 (额外概念讲解) NbTime 永远内置使用的是 Aware datetime（感知时间/带时区时间）

Aware datetime 清晰无异议带时区,Naive datetime 是 朴素时间/无时区时间
Aware datetime 可以无视服务器时区,清楚的知道是什么时区,不需要猜测.

在 Python 的 `datetime` 模块中，这两种时间的专业术语是：

### ✅ 1. **Naive datetime（朴素时间 / 无时区时间）**
- **定义**：不包含时区信息的 `datetime` 对象。
- **特点**：
  - 简单、轻量
  - Python 不知道它对应哪个时区（可能是本地时间，也可能是 UTC，但没标明）
  - **不能直接与其他时区的时间安全比较或转换**
- **示例**：
  ```python
  from datetime import datetime
  naive = datetime(2023, 1, 1, 12, 0)  # 没有时区信息
  print(naive.tzinfo)  # 输出: None
  ```

---

### ✅ 2. **Aware datetime（感知时间 / 带时区时间）**
- **定义**：包含明确时区信息的 `datetime` 对象。
- **特点**：
  - 通过 `tzinfo` 属性绑定时区（如 `timezone.utc`、`pytz.timezone('Asia/Shanghai')` 等）
  - 可以安全地进行跨时区比较、转换和计算
  - **推荐在涉及多时区或持久化存储时使用**
- **示例**：
  ```python
  from datetime import datetime, timezone
  aware = datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
  print(aware.tzinfo)  # 输出: datetime.timezone.utc
  ```

---

### 📌 官方文档术语
Python 官方文档明确使用这两个词：
> - **naive** objects: `datetime` objects that do not contain timezone information.  
> - **aware** objects: `datetime` objects that contain timezone information.

（来源：[Python `datetime` documentation](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects)）

---

### 💡 最佳实践建议
- **永远不要假设 naive datetime 的时区含义**（比如“它就是本地时间”——这在服务器部署时极易出错）。
- **处理用户输入或日志时**：尽量转换为 aware datetime（通常用 UTC）。
- **存储时间到数据库**：推荐用 UTC 的 aware datetime。
- **显示给用户时**：再转成用户所在时区。

---

### 🔧 如何判断？
```python
dt = some_datetime_object
if dt.tzinfo is None:
    print("Naive (无时区)")
else:
    print("Aware (带时区)")
```

总结：  
> **Naive datetime** = 无时区（朴素）  
> **Aware datetime** = 有时区（感知）  

这是 Python 时间处理中最基础也最重要的概念之一。

# 30 NbTime总结
```
总结就是 NbTime 的入参接受所有类型,NbTime支持链式调用,Nbtime方便支持时区,Nbtime方便操作时间转化,
所以NbTime操作时间,远远暴击使用datetime和三方arrow包,
远远暴击用户在 utils.time_utils.py文件中写几百个孤立的面向过程操作时间的函数.
```

--- **end of file: README.md** --- 

---


--- **start of file: README.md** --- 



# 1 NbTime 介绍

`NbTime("2025-10-01 09:00:00", time_zone='America/Los_Angeles').to_tz('Asia/Shanghai').same_day_zero.get_str()`

## 1.0 安装 

pip install nb_time

## 1.1 NbTime 为什么好?

`nb_time` 是面向对象,入参兼容类型能力最强,万能时间字符串识别,时区支持优雅,无限链式调用,性能最好的时间处理工具包(性能超 `arrow` 三方包 700%).

`NbTime`类始终是时间操作的唯一入口,不像其他三方包或者用户自己封装的公用`utils/time_utils.py` 需要记忆选择几十种时间转换函数,`NbTime(x)`是一招鲜吃遍天.

`nb_time` 要做的是用户 `utils/time_utils.py` 的“终结者”.

为什么要写处理时间的包
```
开发中，关于处理时间转换虽然是一件不值一提很微不足道很小的事情，但也是一个常见的事情。
封装的不好的时间操作工具库，造成每次调用麻烦，和性能问题.
例如要调用不同的函数来处理 时间戳 时间字符串 时间对象之间的转换，
以及烦人的时区的转化，从一个时间种类变化到另一个时间类型形态，用户在中间过程要调用三四次不同的函数来转化，
才能处理得到想要的最终结果。

NbTime对象实例化入参接受所有种类的入参，不需要用户针对不同的传参类型做时间转化而选择不同的函数
，用户无脑将任意入参传给NbTime即可；NbTime将常用的时间处理转化结果，作为对象的惰性属性。
一个NbTime的实例化入参搞定所有时间转化需求，不需要用户亲自去选择各种用途的时间转换函数来对时间做转换。
```

## 1.2  time_utils.py  为什么很不好用?

例如像下面图片这种 模块级 + 各种各样的函数 封装的 时间工具包，就太不好用了，因为需要记忆和选择各种各样的不同用途的函数对时间进行转化。

封装时间操作不难，但如果封装的不好用，造成项目中调用它处处难。

那种 一个 time_utils.py 下 def 100 多个时间转换函数的 公共工具包，真的太难用了，用的时候都不知道选用什么函数好,。

1️⃣ 🧩 **一个NbTime类，终结 100+ 个函数**

❌ `time_utils.py`：用户要记忆：

- `str_date_to_timestamp()`
- `timestamp_to_date_str()`
- `get_timestamp_7d_ago()`
- `str_date_time_diff_day()`
- `timestamp_add_day_to_str_date_time()`
- ……（还有 90 多个）


![img_2.png](img_2.png)


## 1.3 NbTime的优点?
```
NbTime 是oop面向对象开发的爽快的日期时间操作类
NbTime 支持无限链式操作来处理时间,
(因为是oop所以易用程度远远的暴击面向过程python工程师写的time_utils.py里面
写几百个独立的操作时间的面向过程函数)

NbTime 入参支持 None 字符串 时间戳 datetime对象 NbTime对象自身 arrow.Arrow对象
NbTime 支持将任意格式的时间字符串转成时间对象，无需提前精确指定写 yyyyy-mm-dd HHMMSS 这样的模板。
NbTime 非常轻松支持时区转化
Nbtime 内置属性 datetime对象,兼容性好
Nbtime 内置 to_arrow 方法,一键转换成arrow.Arrow对象

NbTime操作时间,远远暴击使用datetime和三方arrow包,
远远暴击用户在 utils.time_utils.py文件中写几百个孤立的面向过程操作时间的函数.
```

## 1.4 nb_time 🆚 与主流库对比

| 维度               | `datetime` 标准库 | `arrow`           | `pendulum`        | `nb_time`（你）         |
|--------------------|-------------------|-------------------|-------------------|--------------------------|
| 易用性             | ❌ 低             | ✅ 高             | ✅ 高             | ⭐⭐⭐⭐⭐ 极高              |
| 链式操作           | ❌ 无             | ✅ 支持           | ✅ 支持           | ✅✅✅ 更自然             |
| 时区处理           | ⚠️ 复杂           | ✅ 好             | ✅ 很好           | ⭐⭐⭐⭐⭐ 最智能           |
| 入参兼容性         | ❌ 严格           | ✅ 较好           | ✅ 好             | ⭐⭐⭐⭐⭐ 万能             |
| 性能               | ⭐⭐⭐⭐⭐ 最快       | ⭐⭐ 慢            | ⭐⭐⭐ 中等         | ⭐⭐⭐⭐ 很快（超 arrow）  |
| 可扩展性（继承）   | ❌ 难             | ⚠️ 有限           | ⚠️ 有限           | ⭐⭐⭐⭐⭐ 完美支持         |
| 学习成本           | ⭐⭐⭐ 中           | ⭐⭐ 低            | ⭐⭐ 低            | ⭐ 极低（NbTime(x) 万能）|

# 2 NbTime 时间值传参用法

NbTime 最方便的地方在于入参可以是任何种类，可以不传参；可以传递数字时间戳，自动识别是否是毫秒时间戳；

可以传递datetime对象；可以传递NbTime类型的对象；

可以传递时间字符串，而且可以自动把任何格式模板的时间字符串自动转化成NbTime对象；

综上所述NbTime入参方式已经囊括了所有可能。

所以用户始终用NbTime就可以了，无需记忆和选择几百个各种各样的时间转换函数。

不管是从 时间戳 时间字符串 datetime对象 以及不同时区 的之间互相转化，都是使用 NbTime 对象作为中转对象。

## 2.1 NbTime 不传参,就是当前时间
```
>>> from nb_time import NbTime
>>> NbTime()                   
<NbTime [2024-02-29 17:51:14 +0800]>
```

## 2.2 NbTime 传参datetime对象

```
>>> NbTime(datetime.datetime.now())
<NbTime [2024-02-29 17:56:43 +0800]>
```

## 2.3 NbTime 传参时间戳
```
>>> NbTime(1709192429)
<NbTime [2024-02-29 15:40:29 +0800]>
```

传了大于13位的毫秒时间戳，也能自动转化。
```
>>> NbTime(1709192429000)
<NbTime [2024-02-29 15:40:29 +0800]>
```


## 2.4 NbTime 传参字符串,可以对字符串设置时区,例如把东七区的时间字符串转化成东8区的格式.
```
>>> NbTime('2024-02-26 15:58:21',datetime_formatter=NbTime.FORMATTER_DATETIME,time_zone=NbTime.TIMEZONE_EASTERN_7).to_tz('UTC+8')
<NbTime [2024-02-26 16:58:21 +0800]>
```

## 2.4.b Nbtime 万能自动识别时间字符串模板，可以将所有常见的时间字符串转换成时间对象

Nbtime 万能自动识别时间字符串模板，可以将所有常见的时间字符串转换成时间对象，不需要提前精确的写 yyyy-mm-dd 这样的。

以下例子都能直接转化成时间对象，无视时间字符串格式。

```python
from nb_time import NbTime
print(NbTime('20230506T010203.886 +08:00'))
print(NbTime('2023-05-06 01:02:03.886'))
print(NbTime('2023-05-06T01:02:03.886 +08:00'))
print(NbTime('20221206 1:2:3'))
print(NbTime('Fri Jul 19 06:38:27 2024'))
print(NbTime('2013-05-05 12:30:45 America/Chicago'))
```

## 2.5 NbTime 传参 DateTimeValue类型对象
```
>>> from nb_time import DateTimeValue
>>> NbTime(DateTimeValue(year=2022,month=5,day=9,hour=6),time_zone='UTC+7')
<NbTime [2022-05-09 06:00:00 +0700]>

```

## 2.6 NbTime传参 NbTime对象

NbTime入参本身支持无限嵌套NbTime对象
```
NbTime(NbTime(NbTime(NbTime())))
<NbTime [2024-02-29 18:39:09]>


为什么 NbTime支持入参是自身类型,例如你可以方便的转时区和转字符串格式化
例如0时区的2024-02-29 07:40:34,你要转化成8时区的带毫秒带时区的时间字符串,
>>> from nb_time import NbTime                                                                                                    
>>> NbTime(NbTime('2024-02-29 07:40:34', time_zone='UTC+0', datetime_formatter=NbTime.FORMATTER_DATETIME_NO_ZONE),
...                time_zone='UTC+8', datetime_formatter=NbTime.FORMATTER_MILLISECOND).datetime_str
'2024-02-29 15:40:34.000000 +0800'
```

## 2.7 NbTime传参 arrow.Arrow对象
```
>>> NbTime(arrow.now())
<NbTime [2025-09-09T12:32:58+0800] (Asia/Shanghai)>
```
# 3 NbTime 链式计算时间

NbTime().shift方法返回的对象仍然是Nbtime类型。
因为Nbtime对象本身具有很多好用的属性和方法，所以使用NbTime作为时间转化的中转对象，比使用datetime作为中转对象方便使用很多。


求3天1小时10分钟后的时间,入参支持正数和负数
```
>>> NbTime().shift(hours=1,minutes=10).shift(days=3)
<NbTime [2024-03-03 19:02:49 +0800]>
```

求当前时间1天之前的时间戳
```commandline
>>> NbTime().shift(days=-1).timestamp
1709290123.409756

```

`arrow`和`nb_time`之间无限链式转化
```
>>> NbTime().arrow.ceil('day').to_nb_time()
<NbTime [2025-09-09T23:59:59+0800] (UTC+8)>

```





# 3 NbTime 时区设置

## 3.1 NbTime 实例化时候设置时区

实例化时候分别设置东7区和0时区
```
>>> NbTime(time_zone='UTC+7')
<NbTime [2024-02-29 17:05:08 +0700]>
>>> NbTime(time_zone='UTC+0') 
<NbTime [2024-02-29 10:05:08 +0000]>
```

## 3.2 全局设置时区
用户不传递时区时候,默认就是操作系统时区,如果用户想统一设置时区

例如用户统一设置东8区,以后实例化就不用每次亲自传递东八区.
```
NbTime.set_default_time_zone('UTC+8')
```

# 4 设置时间字符串格式化

## 4.1 NBTime实例化时候设置时间字符串格式
用户不想要毫秒时间字符串
```
>>> NbTime(datetime_formatter=NbTime.FORMATTER_DATETIME)    
<NbTime [2024-02-29 18:10:57 +0800]>
```

用户不想要字符串带时区
```
>>> NbTime(datetime_formatter=NbTime.FORMATTER_DATETIME_NO_ZONE) 
<NbTime [2024-02-29 18:12:18]>
```

##  4.2 NBTime全局设置字符串格式

NbTime.set_default_formatter 可以全局设置时间格式字符串,就不需要每次都传递格式
```
>>> NbTime.set_default_formatter(NbTime.FORMATTER_DATETIME_NO_ZONE)
>>> NbTime()
<NbTime [2024-02-29 18:14:38]>
```

# 5 NbTime 对象内置的成员属性

见下面的交互,NbTime类型对象有非常便捷的各种成员变量,

```
datetime  类型datetime.datetime类型的时间对象,这个很方便和内置类型关联起来
time_zone_obj 时区
datetime_str 日期时间字符串
time_str 时间字符串
date_str 日期字符串
timestamp  时间戳秒
timestamp_millisecond 时间戳毫秒
today_zero_timestamp 当天凌晨的时间戳
arrow  arrow.Arrow对象
```

```
from nb_time import NbTime
>>> nbt=NbTime()
>>> nbt.datetime
datetime.datetime(2024, 2, 29, 18, 16, 23, 541415, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

>>> nbt.time_zone_obj
<DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>

>>> nbt.datetime_str
'2024-02-29 18:16:23'

>>> nbt.time_str
'18:16:23'

>>> nbt.date_str
'2024-02-29'

>>> nbt.timestamp
1709201783.541415

>>> nbt.timestamp_millisecond
1709201783541.415

>>> nbt.today_zero_timestamp
1709136000


>>> nbt.arrow
<Arrow [2025-09-09T13:01:17.526580+08:00]>
```

# 6 NbTime的方法

## 6.1 get_str 方法转化成任意字符串格式
```
例如获取今天的年月日,中间不要带 - 
>>> NbTime().get_str('%Y%m%d')
20240301
```

## 6.2 shift 是计算生成新的NbTime对象,支持无限连续链式操作
```
求3天1小时10分钟后的时间,入参支持正数和负数
>>> NbTime().shift(hours=1,minutes=10).shift(days=3)
<NbTime [2024-03-03 19:02:49 +0800]>
```

## 6.3 to_tz 是生成新的时区的NbTime对象,把NbTime对象转化成另一个时区.
```
一个东7区的时间:
>>> NbTime('2024-02-26 15:58:21',datetime_formatter=NbTime.FORMATTER_DATETIME,time_zone=NbTime.TIMEZONE_EASTERN_7)
<NbTime [2024-02-26 15:58:21 +0700]>

那这个东7区的时间转化成东8区的时间:
>>> NbTime('2024-02-26 15:58:21',datetime_formatter=NbTime.FORMATTER_DATETIME,time_zone=NbTime.TIMEZONE_EASTERN_7).to_tz('UTC+8')
<NbTime [2024-02-26 16:58:21 +0800]>
```

### 6.3.2 两种时区转化写法

例如东7区的2024-02-29 07:40:34转成东八区的时间字符串。

```python
from nb_time import  NbTime

# NbTime对象无限嵌套传参给NbTime方式
print(NbTime(NbTime('2024-02-29 07:40:34', time_zone='UTC+7'), time_zone='UTC+8').datetime_str)

# to_tz 方式
print(NbTime('2024-02-29 07:40:34', time_zone='UTC+7').to_tz('UTC+8').datetime_str)
```

## 6.4 NbTime 对象 支持 > < = 比较
```
NbTime 实现了 __gt__  __lt__  __eq__ 方法,可以直接比较大小

>>> NbTime() > NbTime('2023-05-06 01:01:01')                                            
True
>>> NbTime() > NbTime('2025-05-06 01:01:01') 
False

```
## 6.5 NbTime 转换为 arrow.Arrow对象

```
>>> nt=NbTime()
>>> nt.to_arrow()
<Arrow [2025-09-09T12:34:37.661360+08:00]>
```

## 6.6 NbTime humanize 方法,转人类自然语言
```
>>> NbTime().humanize()
'just now'

>>> NbTime().shift(days=5).humanize()
'in 5 days'

>>> NbTime().shift(days=-3).humanize() 
'3 days ago'
```

# 7.用户自定义继承 NbTime 类

因为 nb_time 是 oop面向对象开发的,所以可以继承,
如果是面向过程编程,使用模块级 + 函数的方式来编程,先改变模块的某个全局变量或者函数逻辑,只能使用猴子补丁技术,而且模块天然还是个单例,不适合多次猴子补丁
面向对象就是有优势.


## 7.1 例如用户想使用 UTC 0时区,但是不想频繁传递 时区入参,可以使用 nb_time的  自带的UtcNbTime 类,或者用户手写这个类自己继承NbTime

```python
class UtcNbTime(NbTime):
    default_time_zone = NbTime.TIMEZONE_UTC

# 使用的时候
UtcNbTime()   
```


## 7.2 例如 用户想使用上海时区,并且默认使用不带时区的时间字符串格式化
```python
class ShanghaiNbTime(NbTime):
    default_time_zone = NbTime.TIMEZONE_ASIA_SHANGHAI
    default_formatter = NbTime.FORMATTER_DATETIME_NO_ZONE

# 使用的时候
ShanghaiNbTime()  
```

## 7.3 数据分析,常用的时间也可以加上来

```python
class PopularNbTime(NbTime):
    @property
    def ago_1_days(self):
        return self.shift(days=-1)

    @property
    def ago_7_days(self):
        return self.shift(days=-7)

    @property
    def ago_30_days(self):
        return self.shift(days=-30)

    @property
    def ago_180_days(self):
        return self.shift(days=-180)
```

# 8 nb_time 性能暴打 arrow 700%
```python
for i in range(1000000):
    NbTime(time_zone='Asia/Shanghai') # 3秒100万次
    # arrow.now(tz='Asia/Shanghai')   # 20秒100万次
```

# 9 演示最差劲的 utils/time_utils.py

**一个“教科书级屎山时间工具包”**    

❌ 所有函数都是面向过程、无封装、无链式  
❌ 每个函数只做“半件事”，用户必须组合 3~4 个函数才能完成一个转换  
❌ 参数命名模糊、格式不统一、文档缺失   
❌ 时区处理靠“猜”和“硬编码数字”  
❌ 同一个功能有 5 个名字类似的函数，行为略有不同  
❌ 不处理异常、不校验输入、出错静默或崩溃   
❌ 大量重复代码、魔法数字、全局变量污染   
❌ 依赖系统本地时区，跨环境行为不一致   
❌ 支持“多种格式”，但用户得自己查源码才知道支持哪些     

💣 最差劲 time_utils.py 出炉！  
```python
# time_utils.py —— 地狱级时间工具包
# 作者：时间混乱之神
# 警告：使用本文件可能导致脱发、失眠、离职

import time
from datetime import datetime, timedelta

# 全局变量，假装是配置，其实是隐藏炸弹
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SYSTEM_TZ_OFFSET = -time.timezone // 3600  # 依赖运行环境！东8区服务器=8，洛杉矶=-7

# =================== 字符串解析区（每个函数只解析一种格式） ===================

def parse_time_str_type1(s):
    # 只支持 "2025-04-05 14:30:00"
    return time.strptime(s, "%Y-%m-%d %H:%M:%S")

def parse_time_str_type2(s):
    # 只支持 "2025/04/05 14:30"
    return time.strptime(s, "%Y/%m/%d %H:%M")

def parse_time_str_type3(s):
    # 只支持 "04-05-2025"
    return time.strptime(s, "%m-%d-%Y")

def parse_time_str_universal(s):
    # “通用”但只 try 3 种，失败就崩溃
    for fmt in ["%Y-%m-%d", "%d/%m/%Y %H:%M", "%Y年%m月%d日"]:
        try:
            return time.strptime(s, fmt)
        except:
            continue
    raise Exception("老子解析不了，你自己看着办")

# =================== 时间结构体 → 时间戳 （但有时区坑） ===================

def struct_time_to_timestamp_utc(st):
    # 输入 struct_time，返回 UTC 时间戳？不！是本地时间戳！
    return int(time.mktime(st))

def struct_time_to_timestamp_assume_utc(st):
    # 假装 st 是 UTC，但 mktime 是本地……所以错了
    return int(time.mktime(st)) - SYSTEM_TZ_OFFSET * 3600

def struct_time_to_timestamp_with_offset(st, offset_hours):
    # offset_hours 是什么？正负？文档？不存在的
    return int(time.mktime(st)) - offset_hours * 3600

# =================== 时间戳 → struct_time ===================

def timestamp_to_struct_local(ts):
    return time.localtime(ts)

def timestamp_to_struct_utc(ts):
    return time.gmtime(ts)

# =================== struct_time → 字符串 ===================

def struct_time_to_str_format1(st):
    return time.strftime("%Y-%m-%d %H:%M:%S", st)

def struct_time_to_str_format2(st):
    return time.strftime("%Y/%m/%d %H点%M分", st)

def struct_time_to_str_custom(st, fmt):
    return time.strftime(fmt, st)

# =================== 时区转换（靠猜） ===================

def convert_timestamp_from_tz7_to_tz8(ts):
    # 硬编码 +3600，假装专业
    return ts + 3600

def convert_timestamp_by_offset_diff(ts, from_offset, to_offset):
    # 文档？参数顺序？谁记得
    return ts + (to_offset - from_offset) * 3600

def convert_string_timezone_manual(s, from_tz_num, to_tz_num):
    # 用户必须自己：1.选解析函数 2.转时间戳 3.调此函数 4.再转回字符串
    st = parse_time_str_type1(s)  # 假设格式对
    ts = struct_time_to_timestamp_utc(st)
    ts2 = convert_timestamp_by_offset_diff(ts, from_tz_num, to_tz_num)
    st2 = timestamp_to_struct_local(ts2)
    return struct_time_to_str_format1(st2)

# =================== “便捷”函数（其实更麻烦） ===================

def get_current_time_in_tz8_str():
    # 返回“当前东八区时间字符串”，但依赖服务器时区！
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_current_timestamp_in_utc():
    return int(time.time())

def add_days_to_timestamp(ts, days):
    return ts + days * 86400

def add_hours_to_struct_time(st, hours):
    # struct_time 是只读的！必须转成 datetime 才能加！但用户不知道！
    dt = datetime(*st[:6])
    dt2 = dt + timedelta(hours=hours)
    return dt2.timetuple()  # 返回 struct_time，但丢失微秒和时区！

# =================== 隐藏陷阱函数 ===================

def quick_convert(s):
    # 名字很诱人，行为很随机
    if "-" in s:
        st = parse_time_str_type1(s)
    elif "/" in s:
        st = parse_time_str_type2(s)
    else:
        st = parse_time_str_universal(s)
    ts = struct_time_to_timestamp_utc(st)
    ts += 3600  # 假装转东8区
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))

# =================== 多余函数（制造选择困难） ===================

def str_to_timestamp_method_a(s): return struct_time_to_timestamp_utc(parse_time_str_type1(s))
def str_to_timestamp_method_b(s): return struct_time_to_timestamp_assume_utc(parse_time_str_type1(s))
def str_to_timestamp_method_c(s): return struct_time_to_timestamp_with_offset(parse_time_str_type1(s), 8)

# =================== 彩蛋：全局状态污染 ===================

_last_parsed_time = None  # 所有函数偷偷修改它，用于“调试”

def parse_and_remember(s):
    global _last_parsed_time
    st = parse_time_str_type1(s)
    _last_parsed_time = st
    return st

# =================== 文档？不存在的 ===================

# 没有类型提示
# 没有 docstring
# 没有示例
# 没有测试
# 只有注释：“以后再改”、“临时方案”、“别动这个！！！”
```

🧩用户使用示例（东7区时间字符串 → 东8区时间字符串):  

```python
from time_utils import *

input_str = "2025-04-05 14:30:00"

# Step 1: 解析字符串 → struct_time
st = parse_time_str_type1(input_str)  # 如果格式不对？崩溃！

# Step 2: struct_time → 时间戳（但这是本地时间戳！坑！）
ts = struct_time_to_timestamp_utc(st)

# Step 3: 手动加3600秒，假装时区转换
ts_east8 = ts + 3600

# Step 4: 时间戳 → struct_time（本地时区！再次依赖服务器！）
st_east8 = timestamp_to_struct_local(ts_east8)

# Step 5: struct_time → 字符串
output_str = struct_time_to_str_format1(st_east8)

print(output_str)  # 可能是 "2025-04-05 15:30:00" —— 如果服务器在东8区！
                   # 如果在洛杉矶？→ 输出错误时间！
```

# 10 真实场景对比 
需求：把东7区的字符串时间，转成东8区，再减3天，取当天0点的毫秒时间戳

**❌ 传统地狱模式（5-7行，并且要查文档）**
```python
dt_str = "2024-02-26 15:58:21"
dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
dt = dt.replace(tzinfo=pytz.timezone("Etc/GMT-7"))
dt = dt.astimezone(pytz.timezone("Asia/Shanghai"))
dt = dt - timedelta(days=3)
dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
result = int(dt.timestamp() * 1000)
```

**✅ NbTime心流模式 (一行链式搞定,不会出错)**
```python
result = NbTime("2024-02-26 15:58:21", time_zone='UTC+7').to_tz('UTC+8').shift(days=-3).same_day_zero.timestamp_millisecond
```

# 20 (额外概念讲解) NbTime 永远内置使用的是 Aware datetime（感知时间/带时区时间）

Aware datetime 清晰无异议带时区,Naive datetime 是 朴素时间/无时区时间
Aware datetime 可以无视服务器时区,清楚的知道是什么时区,不需要猜测.

在 Python 的 `datetime` 模块中，这两种时间的专业术语是：

### ✅ 1. **Naive datetime（朴素时间 / 无时区时间）**
- **定义**：不包含时区信息的 `datetime` 对象。
- **特点**：
  - 简单、轻量
  - Python 不知道它对应哪个时区（可能是本地时间，也可能是 UTC，但没标明）
  - **不能直接与其他时区的时间安全比较或转换**
- **示例**：
  ```python
  from datetime import datetime
  naive = datetime(2023, 1, 1, 12, 0)  # 没有时区信息
  print(naive.tzinfo)  # 输出: None
  ```

---

### ✅ 2. **Aware datetime（感知时间 / 带时区时间）**
- **定义**：包含明确时区信息的 `datetime` 对象。
- **特点**：
  - 通过 `tzinfo` 属性绑定时区（如 `timezone.utc`、`pytz.timezone('Asia/Shanghai')` 等）
  - 可以安全地进行跨时区比较、转换和计算
  - **推荐在涉及多时区或持久化存储时使用**
- **示例**：
  ```python
  from datetime import datetime, timezone
  aware = datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
  print(aware.tzinfo)  # 输出: datetime.timezone.utc
  ```

---

### 📌 官方文档术语
Python 官方文档明确使用这两个词：
> - **naive** objects: `datetime` objects that do not contain timezone information.  
> - **aware** objects: `datetime` objects that contain timezone information.

（来源：[Python `datetime` documentation](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects)）

---

### 💡 最佳实践建议
- **永远不要假设 naive datetime 的时区含义**（比如“它就是本地时间”——这在服务器部署时极易出错）。
- **处理用户输入或日志时**：尽量转换为 aware datetime（通常用 UTC）。
- **存储时间到数据库**：推荐用 UTC 的 aware datetime。
- **显示给用户时**：再转成用户所在时区。

---

### 🔧 如何判断？
```python
dt = some_datetime_object
if dt.tzinfo is None:
    print("Naive (无时区)")
else:
    print("Aware (带时区)")
```

总结：  
> **Naive datetime** = 无时区（朴素）  
> **Aware datetime** = 有时区（感知）  

这是 Python 时间处理中最基础也最重要的概念之一。

# 30 NbTime总结
```
总结就是 NbTime 的入参接受所有类型,NbTime支持链式调用,Nbtime方便支持时区,Nbtime方便操作时间转化,
所以NbTime操作时间,远远暴击使用datetime和三方arrow包,
远远暴击用户在 utils.time_utils.py文件中写几百个孤立的面向过程操作时间的函数.
```

--- **end of file: README.md** --- 

---


--- **start of file: setup.py** --- 

``python
# coding=utf-8
from pathlib import Path
from setuptools import setup, find_packages
import os

# with open("README.md", "r",encoding='utf8') as fh:
#     long_description = fh.read()

# filepath = ((Path(__file__).parent / Path('README.md')).absolute()).as_posix()
filepath = 'README.md'
print(filepath)


extra_requires = {}
install_requires = [
    'tzlocal',
    'pytz',
    'arrow',
    # 'pydantic',
    'python-dateutil',
]

# if os.name == 'nt':
#     install_requires.append('pywin32')

print(f'nb_time install_requires:{install_requires}')
setup(
    name='nb_time',  #
    version="2.8",
    description=(
        'Awesome time conversion handling with support for chaining operations. '
    ),
    keywords=['arrow','time','datetime','time_utils'],
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    long_description_content_type="text/markdown",
    long_description=open(filepath, 'r', encoding='utf8').read(),
    url='https://github.com/ydf0509/nb_time',
    # data_files=[filepath],
    author='bfzs',
    author_email='ydf0509@sohu.com',
    maintainer='ydf',
    maintainer_email='ydf0509@sohu.com',
    # license='BSD License',
    license='BSD-3-Clause',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=install_requires,
    extras_require = extra_requires
)
"""
打包上传
python setup.py sdist upload -r pypi




python setup.py sdist && python -m  twine upload dist/nb_time-0.1.tar.gz

twine upload dist/*


python -m pip install nb_time --upgrade -i https://pypi.org/simple   # 及时的方式，不用等待 阿里云 豆瓣 同步
"""

```

--- **end of file: setup.py** --- 

---

# markdown content namespace: nb_time codes with AST metadata 


## File Tree


```

└── nb_time
    └── __init__.py

```

---


## Included Files


- `nb_time/__init__.py`


---


--- **start of file: nb_time/__init__.py** --- 


### 📄 Python File Metadata: `nb_time/__init__.py`

#### 📦 Imports

- `import copy`
- `import functools`
- `import logging`
- `import pickle`
- `import sys`
- `import threading`
- `import types`
- `import typing`
- `import re`
- `import time`
- `import datetime`
- `from dateutil.relativedelta import relativedelta`
- `import dateutil.parser`
- `import pytz`
- `import arrow`
- `from tzlocal import get_localzone`
- `import nb_log`
- `import arrow`

#### 🏛️ Classes (8)

##### 📌 `class DateTimeValue`
*Line: 41*

**Public Methods (1):**
- `def dict(self)`

##### 📌 `class TimeInParamError(Exception)`
*Line: 63*

##### 📌 `class ArrowWrap(arrow.Arrow)`
*Line: 66*

**Public Methods (1):**
- `def to_nb_time(self)`

##### 📌 `class NbTime`
*Line: 70*

**Docstring:**
```
时间转换，支持链式操作，纯面向对象的的。

相比模块级下面定义几十个函数，然后将不同类型的时间变量传到不同的函数中return结果，然后把结果作为入参传入到另一个函数进行转换，
...
```

**Public Methods (22):**
- `def set_default_formatter(cls, datetime_formatter: str)` `classmethod`
- `def set_default_time_zone(cls, time_zone: str)` `classmethod`
- `def get_localzone_name() -> str` `staticmethod` `functools.lru_cache()`
- `def get_time_zone_str(self, time_zone: typing.Union[str, datetime.tzinfo, None] = None)`
- `def universal_parse_datetime_str(self, datetime_str)`
- `def build_datetime_obj(self, datetimex)`
- `def add_timezone_to_time_str(cls, datetimex: str, time_zone: str)` `classmethod`
- `def get_timezone_offset(cls, time_zone: str) -> datetime.timedelta` `classmethod`
- `def build_pytz_timezone(cls, time_zone: typing.Union[str, datetime.tzinfo]) -> datetime.tzinfo` `classmethod`
  - *pytz 不支持 GTM+8  UTC+7 这种时区表示方式*
- `def get_str(self, formatter = None)`
- `def fast_get_str_formatter_datetime_no_zone(self)`
- `def is_greater_than_now(self) -> bool`
- `def humanize(self) -> str`
- `def to_arrow(self) -> ArrowWrap`
- `def isoformat(self, timespec: str = 'seconds') -> str`
  - *返回 ISO 8601 格式字符串*
- `def clone(self) -> 'NbTime'`
- `def shift(self, years = 0, months = 0, days = 0, leapdays = 0, weeks = 0, hours = 0, minutes = 0, seconds = 0, microseconds = 0) -> 'NbTime'`
- `def replace(self, year = None, month = None, day = None, hour = None, minute = None, second = None, microsecond = None)`
- `def to_tz(self, time_zone: str) -> 'NbTime'`
- `def to_utc(self)`
- `def to_utc8(self)`
- `def seconds_to_hour_minute_second(seconds)` `staticmethod`
  - *把秒转化成还需要的时间*

**Properties (9):**
- `@property datetime_str -> str`
- `@property time_str -> str`
- `@property date_str -> str`
- `@property timestamp -> float`
- `@property timestamp_millisecond -> float`
- `@property arrow -> ArrowWrap`
- `@property today_zero -> 'NbTime'`
- `@property today_zero_timestamp -> float`
- `@property same_day_zero -> 'NbTime'`

##### 📌 `class PopularNbTime(NbTime)`
*Line: 458*

**Properties (6):**
- `@property ago_1_days`
- `@property ago_7_days`
- `@property ago_30_days`
- `@property ago_180_days`
- `@property ago_360_days`
- `@property ago_720_days`

##### 📌 `class UtcNbTime(NbTime)`
*Line: 484*

##### 📌 `class ShanghaiNbTime(NbTime)`
*Line: 488*

##### 📌 `class NowTimeStrCache`
*Line: 494*

**Public Methods (1):**
- `def fast_get_now_time_str(cls, timezone_str: str = None) -> str` `classmethod`
  - *获取当前时间字符串，格式为 '%Y-%m-%d %H:%M:%S'。*

#### 🔧 Public Functions (2)

- `def get_localzone_ignore_version()` `functools.lru_cache()`
  - *Line: 23*

- `def calculate_age(birth_date, datetime_formatter = '%Y-%m-%d')`
  - *Line: 537*


---

```python
import copy
import functools
import logging
import pickle
import sys
import threading
import types
import typing
import re
import time
import datetime
from dateutil.relativedelta import relativedelta
import dateutil.parser
import pytz
import arrow

# from pydantic import BaseModel

logger = logging.getLogger(__name__)


@functools.lru_cache()
def get_localzone_ignore_version():  # python3.9以上不一样.  tzlocal 版本在不同python版本上自动安装不同版本
    from tzlocal import get_localzone
    try:
        return get_localzone().zone
    except AttributeError as e:
        return get_localzone().key


# class DateTimeValue(BaseModel):
#     year: int
#     month: int
#     day: int
#     hour: int = 0
#     minute: int = 0
#     second: int = 0
#     microsecond: int = 0


class DateTimeValue:
    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

    def dict(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'hour': self.hour,
            'minute': self.minute,
            'second': self.second,
            'microsecond': self.microsecond
        }


class TimeInParamError(Exception):
    pass

class ArrowWrap(arrow.Arrow):
    def to_nb_time(self):
        return NbTime(self)

class NbTime:
    """ 时间转换，支持链式操作，纯面向对象的的。

    相比模块级下面定义几十个函数，然后将不同类型的时间变量传到不同的函数中return结果，然后把结果作为入参传入到另一个函数进行转换，
    纯面向对象支持链式转换的要方便很多。

    初始化能够接受的变量类型丰富，可以传入一切类型的时间变量。

    """
    FORMATTER_DATETIME = "%Y-%m-%d %H:%M:%S %z"  # 2023-07-03 16:20:21 +0800 ,这种字符串格式的时间清晰明了没有时区的歧义.
    FORMATTER_DATETIME_WITH_ZONE = "%Y-%m-%d %H:%M:%S %z"
    FORMATTER_DATETIME_NO_ZONE = "%Y-%m-%d %H:%M:%S"
    FORMATTER_MILLISECOND = "%Y-%m-%d %H:%M:%S.%f %z"
    FORMATTER_DATE = "%Y-%m-%d"
    FORMATTER_TIME = "%H:%M:%S"
    FORMATTER_ISO = "%Y-%m-%dT%H:%M:%S%z"  # iso8601,全球最标准的时间格式

    TIMEZONE_UTC = 'UTC'
    TIMEZONE_EASTERN_7 = 'UTC+7'
    TIMEZONE_EASTERN_8 = 'UTC+8'  # UTC+08:00 这是东八区
    TIMEZONE_E8 = 'Etc/GMT-8'  # 这个也是东八区，这个Etc/GMT是标准的pytz的支持的格式。
    TIMEZONE_ASIA_SHANGHAI = 'Asia/Shanghai'  # 就是东八区.
    TIMEZONE_TZ_EAST_8 = datetime.timezone(datetime.timedelta(hours=8),
                                           name='UTC+08:00')  # 这种性能比pytz 'Asia/Shanghai' 性能高很多。但pytz可以处理历史夏令时。
    TIMEZONE_TZ_UTC = datetime.timezone(datetime.timedelta(hours=0), name='UTC+07:00')

    default_formatter: str = None
    default_time_zone: str = None

    @classmethod
    def set_default_formatter(cls, datetime_formatter: str):
        cls.default_formatter = datetime_formatter

    @classmethod
    def set_default_time_zone(cls, time_zone: str):
        cls.default_time_zone = time_zone

    @staticmethod
    @functools.lru_cache()
    def get_localzone_name() -> str:
        zone = get_localzone_ignore_version()
        print(f'auto get the system time zone is "{zone}"')
        return zone

    time_zone_str__obj_map = {}

    def __init__(self,
                 datetimex: typing.Union[
                     None, int, float, datetime.datetime, str, 'NbTime', DateTimeValue, arrow.Arrow] = None,
                 *,
                 datetime_formatter: str = None,
                 time_zone: typing.Union[str, datetime.tzinfo, None] = None):
        """
        :param datetimex: 接受时间戳  datatime类型 和 时间字符串 和类对象本身四种类型,如果为None，则默认当前时间now。
        :param time_zone  时区例如 Asia/Shanghai， UTC  UTC+8  GMT+8  Etc/GMT-8 等,也可以是 datetime.timezone(datetime.timedelta(hours=7))东7区,
                          默认是操作系统时区
        """
        # init_params = copy.copy(locals())
        # init_params.pop('self')
        # init_params.pop('datetimex')

        self._raw_in_params = {'datetimex':datetimex,'datetime_formatter':datetime_formatter,'time_zone':time_zone}
 
        init_params = {'datetime_formatter': datetime_formatter, 'time_zone': time_zone}
        self.init_params = init_params
        self.first_param = datetimex

        self.time_zone_str = self.get_time_zone_str(time_zone)
        self.datetime_formatter = datetime_formatter or self.default_formatter or self.FORMATTER_ISO
        '''
        将 time_zone 转成 pytz 可以识别的对应时区
        '''
        self.time_zone_obj = self.build_pytz_timezone(self.time_zone_str)
        self.datetime_obj = self.build_datetime_obj(datetimex)
        self.datetime = self.datetime_obj

    def _build_nb_time(self, datetimex) -> 'NbTime':
        return self.__class__(datetimex, **self.init_params)

    def get_time_zone_str(self, time_zone: typing.Union[str, datetime.tzinfo, None] = None):
        return time_zone or self.default_time_zone or self.get_localzone_name()

    def universal_parse_datetime_str(self, datetime_str):
        try:
            return dateutil.parser.parse(datetime_str)
        except Exception as e:
            date_string = datetime_str  # "2013-05-05 12:30:45 America/Chicago"
            date_parts = date_string.split()
            parsed_date = dateutil.parser.parse(' '.join(date_parts[:-1]))
            timezone = dateutil.tz.gettz(date_parts[-1])
            datetime_obj = parsed_date.replace(tzinfo=timezone)
            return self._build_nb_time(datetime_obj).datetime_obj

    def build_datetime_obj(self, datetimex):
        if datetimex is None:
            # print(self.time_zone_obj,type(self.time_zone_obj))
            datetime_obj = datetime.datetime.now(tz=self.time_zone_obj)
        elif isinstance(datetimex, str):
            # print(self.datetime_formatter)
            if '%z' in self.datetime_formatter and ('+' not in datetimex or '-' not in datetimex):
                datetimex = self.add_timezone_to_time_str(datetimex, self.time_zone_str)
            try:
                datetime_obj = datetime.datetime.strptime(datetimex, self.datetime_formatter)
            except Exception as e:
                # print(e,type(e))
                # print(f'尝试使用万能时间字符串解析 {datetimex}')
                logger.warning(f'warning! formatter: {self.datetime_formatter} cannot parse time str: {datetimex}  , {type(e)} , {e}  , will try use  Universal time string parsing')
                datetime_obj = self.universal_parse_datetime_str(datetimex)
            # print(repr(datetime_obj))
            if datetime_obj.tzinfo is None:
                if isinstance(self.time_zone_obj, pytz.BaseTzInfo):
                    datetime_obj = self.time_zone_obj.localize(datetime_obj, )
                else:
                    datetime_obj = datetime_obj.replace(tzinfo=self.time_zone_obj, )
            else:
                datetime_obj = datetime_obj.astimezone(self.time_zone_obj)
            # if isinstance(self.time_zone_obj,pytz.BaseTzInfo) and datetime_obj.tzinfo is None:
            #     datetime_obj = self.time_zone_obj.localize(datetime_obj, )
            # else:
            #     datetime_obj = datetime_obj.replace(tzinfo=self.time_zone_obj, )
            # print(repr(datetime_obj))
        elif isinstance(datetimex, (int, float)):
            if datetimex < 1:
                datetimex += 86400
            if datetimex >= 10 ** 12:
                # raise TimeInParamError(
                #     f'Invalid datetime param: {datetimex}. need seconds,not microseconds')  # 需要传入秒，而不是毫秒
                datetimex = datetimex / 1000.0
            datetime_obj = datetime.datetime.fromtimestamp(datetimex, tz=self.time_zone_obj)  # 时间戳0在windows会出错。
        elif isinstance(datetimex, datetime.datetime):
            datetime_obj = datetimex
            if datetimex.tzinfo is None:
                # 视为 self.time_zone_obj 时区的时间
                datetime_obj = self.time_zone_obj.localize(datetimex) if isinstance(self.time_zone_obj, pytz.BaseTzInfo) else datetimex.replace(tzinfo=self.time_zone_obj)
            else:
                datetime_obj = datetimex.astimezone(self.time_zone_obj)
        elif isinstance(datetimex, DateTimeValue):
            datetime_obj = datetime.datetime(**datetimex.dict(), tzinfo=self.time_zone_obj)
        elif isinstance(datetimex, NbTime):
            datetime_obj = datetimex.datetime_obj
            datetime_obj = datetime_obj.astimezone(tz=self.time_zone_obj)
        elif isinstance(datetimex, arrow.Arrow):
            datetime_obj = datetimex.datetime
            datetime_obj = datetime_obj.astimezone(tz=self.time_zone_obj)
        else:
            raise ValueError('input parameters is not right')
        return datetime_obj

    @classmethod
    def add_timezone_to_time_str(cls, datetimex: str, time_zone: str):
        offset = cls.get_timezone_offset(time_zone)
        offset_hour = int(offset.total_seconds() // 3600)
        abs_offset_hour = abs(offset_hour)
        int_timezone = ''
        if abs_offset_hour < 10:
            int_timezone = f'0{abs_offset_hour}00'
        else:
            int_timezone = f'{abs_offset_hour}00'
        if offset_hour < 0:
            int_timezone = f'-{int_timezone}'
        else:
            int_timezone = f'+{int_timezone}'
        if not cls._contains_two_or_more_letters(datetimex):
            datetimex += f' {int_timezone}'
        return datetimex

    @staticmethod
    def _contains_two_or_more_letters(text):
        pattern = r"[a-zA-Z]"
        letters = re.findall(pattern, text)
        return len(letters) >= 2

    @classmethod
    def get_timezone_offset(cls, time_zone: str) -> datetime.timedelta:
        tz = cls.build_pytz_timezone(time_zone)
        # 将时区转换为以Etc/GMT+形式表示的时区
        offset = tz.utcoffset(datetime.datetime.now())
        return offset

    @staticmethod
    def _utc_to_etc(timezone_str: str):
        """把UTC+8或UTC+08:00 转化成pytz可以识别的Etc/GMT-8的时区格式"""
        offset_match = re.match(r"UTC([+-]?)(\d{1,2}):?(\d{0,2})", timezone_str,re.IGNORECASE)
        if not offset_match:
            return timezone_str
        # 提取小时和分钟的偏移量
        sign = offset_match.group(1)
        hours = offset_match.group(2)
        minutes = offset_match.group(3)

        if sign == "+":
            sign = "-"
        else:
            sign = "+"

        # 构建新的时区表示
        new_timezone = f"Etc/GMT{sign}{int(hours)}"
        return new_timezone

    @classmethod
    def build_pytz_timezone(cls, time_zone: typing.Union[str, datetime.tzinfo]) -> datetime.tzinfo:
        """pytz 不支持 GTM+8  UTC+7 这种时区表示方式
        Etc/GMT-8 就是 GMT+8 代表东8区。
        """
        # print(time_zone,type(time_zone))
        time_zone0 = time_zone
        if time_zone0 in cls.time_zone_str__obj_map:
            # print('zhijie')
            return cls.time_zone_str__obj_map[time_zone0]

        if isinstance(time_zone, datetime.tzinfo):
            return time_zone

        # 常见时区字符串转化为内置的timezone类型，比pytz性能高很多。
        if time_zone in (cls.TIMEZONE_ASIA_SHANGHAI, cls.TIMEZONE_E8, cls.TIMEZONE_EASTERN_8):
            # print('aaaa')
            return cls.TIMEZONE_TZ_EAST_8
        if time_zone in (cls.TIMEZONE_UTC, 'UTC+0'):
            return cls.TIMEZONE_TZ_UTC

        if 'Etc/GMT' in time_zone:
            tz = pytz.timezone(time_zone)
            cls.time_zone_str__obj_map[time_zone0] = tz
            return tz
        # print(time_zone,type(time_zone))
        time_zone = cls._utc_to_etc(time_zone)
        # print(time_zone)
        # pytz_timezone_xialinshi = pytz.timezone(time_zone)
        pytz_timezone = pytz.timezone(time_zone, )
        cls.time_zone_str__obj_map[time_zone0] = pytz_timezone
        return pytz_timezone

    @property
    def datetime_str(self) -> str:
        return self.get_str()

    @property
    def time_str(self) -> str:
        return self.datetime_obj.strftime(self.FORMATTER_TIME)

    @property
    def date_str(self) -> str:
        return self.datetime_obj.strftime(self.FORMATTER_DATE)

    def get_str(self, formatter=None):
        # print(self.datetime_formatter)
        return self.datetime_obj.strftime(formatter or self.datetime_formatter)

    def fast_get_str_formatter_datetime_no_zone(self):
        return f'{self.datetime_obj.year:04d}-{self.datetime_obj.month:02d}-{self.datetime_obj.day:02d} {self.datetime_obj.hour:02d}:{self.datetime_obj.minute:02d}:{self.datetime_obj.second:02d}'

    @property
    def timestamp(self) -> float:
        return self.datetime_obj.timestamp()

    @property
    def timestamp_millisecond(self) -> float:
        return self.datetime_obj.timestamp() * 1000

    def is_greater_than_now(self) -> bool:
        return self.timestamp > time.time()

    def __lt__(self, other: 'NbTime'):
        return self.timestamp < other.timestamp

    def __gt__(self, other: 'NbTime'):
        return self.timestamp > other.timestamp

    def __eq__(self, other: 'NbTime'):
        return self.timestamp == other.timestamp

    def __str__(self) -> str:
        return f'<NbTime [{self.datetime_str}] ({self.time_zone_str})>'

    def __repr__(self) -> str:
        return f'<NbTime [{self.datetime_str}] ({self.time_zone_str})>'

    def humanize(self)->str:
        return self.arrow.humanize()

    def to_arrow(self)->ArrowWrap:
        # return arrow.get(self.datetime_obj)
        return ArrowWrap(year=self.datetime_obj.year, month=self.datetime_obj.month, day=self.datetime_obj.day,
                         hour=self.datetime_obj.hour,minute=self.datetime_obj.minute,second=self.datetime_obj.second,
                         microsecond=self.datetime_obj.microsecond,
                         tzinfo=self.time_zone_str)

    @property
    def arrow(self) -> ArrowWrap:
        if getattr(self, '_arrow_obj', None) is None:
            self._arrow_obj = self.to_arrow()
        return self._arrow_obj

    def isoformat(self, timespec: str = 'seconds') -> str:
        """
        返回 ISO 8601 格式字符串
        :param timespec: 'seconds', 'milliseconds', 'microseconds'
        """
        return self.datetime_obj.isoformat(timespec=timespec)

    def __call__(self) -> datetime.datetime:
        return self.datetime_obj

    def clone(self) -> "NbTime":
        return self._build_nb_time(self.datetime_obj, )

    def __copy__(self):
        return self.clone()

    
    # def __getstate__(self):
    #     # 自定义序列化时保存的状态
    #     state = self._raw_in_params
    #     return state
    
    # def __setstate__(self, state):
    #     new_self = self.__class__(**state)
    #     self.__dict__.update(new_self.__dict__)
    
    def shift(self, years=0, months=0, days=0, leapdays=0, weeks=0,
              hours=0, minutes=0, seconds=0, microseconds=0, ) -> 'NbTime':
        relativedeltax = relativedelta(years=years, months=months, days=days, leapdays=leapdays, weeks=weeks,
                                       hours=hours, minutes=minutes, seconds=seconds,
                                       microseconds=microseconds, )
        new_date = self.datetime_obj + relativedeltax
        # seconds_delta = seconds + minutes * 60 + hours * 3600 + days * 86400 + weeks * 86400 * 7
        return self._build_nb_time(new_date, )

    def replace(self, year=None,
                month=None,
                day=None,
                hour=None,
                minute=None,
                second=None,
                microsecond=None,
                ):
        kw = copy.copy(locals())
        kw.pop('self')
        kw_new = {}
        for k, v in kw.items():
            if v is not None:
                kw_new[k] = v
        datetime_new = self.datetime_obj.replace(**kw_new)
        return self._build_nb_time(datetime_new)

    def to_tz(self, time_zone: str) -> 'NbTime':
        init_params = copy.copy(self.init_params)
        init_params['time_zone'] = time_zone
        return self.__class__(self.timestamp, **init_params)

    def to_utc(self):
        return self.to_tz(self.TIMEZONE_UTC)

    def to_utc8(self):
        return self.to_tz(self.TIMEZONE_E8)

    @property
    def today_zero(self) -> 'NbTime':
        now = datetime.datetime.now(tz=self.time_zone_obj)
        today_zero_datetime = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self._build_nb_time(today_zero_datetime, )

    @property
    def today_zero_timestamp(self) -> float:
        return self.today_zero.timestamp

    @property
    def same_day_zero(self) -> 'NbTime':
        """
        获取时间对象对应的当天的该对象时区的0点的 NbTime对象
        :return:
        """

        same_day_zero_datetime = self.datetime_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        return self._build_nb_time(same_day_zero_datetime, )

    @staticmethod
    def seconds_to_hour_minute_second(seconds):
        """
        把秒转化成还需要的时间
        :param seconds:
        :return:
        """
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)


class PopularNbTime(NbTime):
    @property
    def ago_1_days(self):
        return self.shift(days=-1)

    @property
    def ago_7_days(self):
        return self.shift(days=-7)

    @property
    def ago_30_days(self):
        return self.shift(days=-30)

    @property
    def ago_180_days(self):
        return self.shift(days=-180)

    @property
    def ago_360_days(self):
        return self.shift(days=-360)

    @property
    def ago_720_days(self):
        return self.shift(days=-720)


class UtcNbTime(NbTime):
    default_time_zone = NbTime.TIMEZONE_UTC


class ShanghaiNbTime(NbTime):
    # default_time_zone = NbTime.TIMEZONE_ASIA_SHANGHAI
    default_time_zone = NbTime.TIMEZONE_TZ_EAST_8
    default_formatter = NbTime.FORMATTER_DATETIME_NO_ZONE


class NowTimeStrCache:
    # 生成100万次当前时间字符串%Y-%m-%d %H:%M:%S仅需0.4秒.
    # 全局变量，用于存储缓存的时间字符串和对应的整秒时间戳
    _cached_time_str: typing.Optional[str] = None
    _cached_time_second: int = 0

    # 为了线程安全，使用锁。在极高并发下，锁的开销远小于每毫秒都进行时间格式化。
    _time_cache_lock = threading.Lock()

    @classmethod
    def fast_get_now_time_str(cls, timezone_str: str = None) -> str:
        """
        获取当前时间字符串，格式为 '%Y-%m-%d %H:%M:%S'。
        通过缓存机制，同一秒内的多次调用直接返回缓存结果，极大提升性能。
        适用于对时间精度要求不高（秒级即可）的高并发场景。
        :return: 格式化后的时间字符串，例如 '2024-06-12 15:30:45'
        """
        # timezone_str = timezone_str or FunboostCommonConfig.TIMEZONE

        # 获取当前的整秒时间戳（去掉小数部分）
        current_second = int(time.time())

        # 如果缓存的时间戳与当前秒数一致，直接返回缓存的字符串。
        if current_second == cls._cached_time_second:
            return cls._cached_time_str

        # 如果不一致，说明进入新的一秒，需要重新计算并更新缓存。
        # 使用锁确保在多线程环境下，只有一个线程会执行更新操作。

        with cls._time_cache_lock:
            # 双重检查锁定 (Double-Checked Locking)，防止在等待锁的过程中，其他线程已经更新了缓存。
            if current_second == cls._cached_time_second:
                return cls._cached_time_str

            # 重新计算时间字符串。这里直接使用 time.strftime，因为它在秒级更新的场景下性能足够。
            # 我们不需要像 Funboost 那样为每一毫秒的调用都去做查表优化。
            now = datetime.datetime.now(tz=pytz.timezone(timezone_str))
            cls._cached_time_str = now.strftime('%Y-%m-%d %H:%M:%S', )
            cls._cached_time_second = current_second

        return cls._cached_time_str


def calculate_age(birth_date,datetime_formatter='%Y-%m-%d'):
    birth_date = NbTime(birth_date,datetime_formatter=datetime_formatter)
    now = NbTime()
    age = now.datetime_obj.year - birth_date.datetime_obj.year
    # 如果今年生日还没到，减一岁
    if (now.datetime_obj.month, now.datetime_obj.day) < (birth_date.datetime_obj.month, birth_date.datetime_obj.day):
        age -= 1
    return age



if __name__ == '__main__':
    import nb_log

    """
    1557113661.0
    '2019-05-06 12:34:21'
    '2019/05/06 12:34:21'
    NbTime(1557113661.0)()
    """

    print(NbTime.get_localzone_name())

    print(NbTime(time_zone='UTC+8').today_zero_timestamp)
    print(NbTime(time_zone='UTC+7').datetime_obj)
    print(NbTime(time_zone='UTC+8').datetime_str)
    print(NbTime(time_zone='UTC+7').time_zone_obj)

    print(NbTime.get_timezone_offset('Asia/Shanghai'))
    # NbTime.set_default_formatter(NbTime.FORMATTER_MILLISECOND)
    NbTime.set_default_time_zone('UTC+8')

    # print(NbTime('2023-05-06 12:12:12'))
    print(NbTime())
    print(NbTime(datetime.datetime.now()))  # 和上面等效
    print(NbTime(1709192429))
    print(NbTime('2024-02-26 15:58:21', datetime_formatter=NbTime.FORMATTER_DATETIME_NO_ZONE,
                 time_zone=NbTime.TIMEZONE_EASTERN_7).datetime)
    print(NbTime(DateTimeValue(year=2022, month=5, day=9, hour=6), time_zone='UTC+7'))
    print(NbTime(datetime.datetime(2022, 5, 9, 6, 0, 0, )))

    print(NbTime(datetime.datetime.now(tz=pytz.timezone('Etc/GMT+0')), time_zone='UTC+8'))
    print(NbTime().shift(months=1).shift(hours=-1))
    print(NbTime(datetime_formatter=NbTime.FORMATTER_MILLISECOND).to_tz(time_zone='UTC+8').to_tz(time_zone='UTC+0'))

    print(NbTime.get_timezone_offset(NbTime.get_localzone_name()).total_seconds())

    print(NbTime(time_zone='UTC+7').today_zero_timestamp)

    print(NbTime.seconds_to_hour_minute_second(450))

    print(NbTime(time_zone=NbTime.TIMEZONE_ASIA_SHANGHAI).datetime.tzinfo)

    print(NbTime(time_zone='UTC+8').time_zone_obj)
    print(NbTime(time_zone='UTC+07:00').time_zone_obj)

    print(NbTime(time_zone=datetime.timezone(datetime.timedelta(hours=7))))

    print(
        NbTime(NbTime('2024-02-29 07:40:34', time_zone='UTC+0', datetime_formatter=NbTime.FORMATTER_DATETIME_NO_ZONE),
               time_zone='UTC+8', datetime_formatter=NbTime.FORMATTER_MILLISECOND).datetime_str
    )

    print(NbTime('2024-02-29 07:40:34', time_zone='UTC+7'))
    print(NbTime(NbTime('2024-02-29 07:40:34', time_zone='UTC+7'), time_zone='UTC+8',
                 datetime_formatter=NbTime.FORMATTER_ISO).datetime_str)
    print(NbTime('2024-02-29 07:40:34', time_zone='UTC+7').to_tz('UTC+8').to_tz('utc').to_utc().datetime_str)

    print(NbTime().get_str('%Y%m%d'))
    print(NbTime().today_zero)
    print(NbTime().today_zero_timestamp)

    print(NbTime().replace(day=10, ).to_tz('UTC+6'))
    print(NbTime().replace(day=10, ).to_tz('utc+6'))
    print(NbTime().shift(days=-7).timestamp_millisecond)
    print(NbTime().shift(days=-1).to_tz('UTC').same_day_zero.timestamp)  # 昨天utc 0时区的时间戳

    print(NbTime(1709283094))

    print(NbTime(DateTimeValue(year=2023, month=7, day=5, hour=4, minute=3, second=2, microsecond=1))
          > NbTime(DateTimeValue(year=2023, month=6, day=6, hour=4, minute=3, second=2, microsecond=1)))

    print(NbTime(1727252278000))

    print(PopularNbTime().ago_7_days.timestamp_millisecond)

    print(UtcNbTime())

    print(UtcNbTime().today_zero.timestamp_millisecond)

    print(ShanghaiNbTime())

    print(NbTime('20230506T010203.886 +08:00'))
    print(NbTime('2023-05-06 01:02:03.886'))
    print(NbTime('2023-05-06T01:02:03.886 +08:00'))
    print(NbTime('20221206 1:2:3'))
    print(NbTime('Fri Jul 19 06:38:27 2024'))
    print(NbTime('2013-05-05 12:30:45 America/Chicago'))
    print(NbTime('2013-05-05 12:30:45 America/Chicago').isoformat())
    print(NbTime('Jun 12 2024 10:30AM'))

    import arrow

    # print(arrow.get("tomorrow at 3pm")) # 报错
    # print(NbTime("tomorrow at 3pm"))
    print(arrow.now().shift(hours=-3).shift(days=6).humanize())
    print(arrow.now().shift(hours=-3).shift(days=6))

    print(NbTime('2025-09-29 10:01:02').humanize())
    print(NbTime('2025-09-29 10:01:02').isoformat('microseconds'))

    print(NbTime(arrow.now(tz='utc+7')))

    print(NbTime().arrow.floor('hour'))
    print(NbTime().arrow.floor('day'))
    print(NbTime().arrow.ceil('day').to_nb_time().timestamp) # nb_time 和 arrow 之间 无限链式转化


    nbt6 = NbTime()

    nbt6_pickled =pickle.dumps(nbt6)
    print(nbt6_pickled)
    nbt6_new = pickle.loads(nbt6_pickled)
    print(nbt6_new)

    print(calculate_age('1990-11-01',datetime_formatter='%Y-%m-%d'))
    print(calculate_age('19901101',datetime_formatter='%Y%m%d'))
    print(calculate_age('1990-10-01',datetime_formatter='%Y-%m-%d'))
    print(calculate_age('19901001',datetime_formatter='%Y%m%d'))

    print()
    for i in range(1000000):
        # ShanghaiNbTime(time_zone='Asia/Shanghai').get_str()
        # ShanghaiNbTime(time_zone='UTC+8').get_str()
        # datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # NbTime(time_zone='Asia/Shanghai') # 3秒100万次
        arrow.now(tz='Asia/Shanghai') # 20秒100万次
        # datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        # NbTime().fast_get_str_formatter_datetime_no_zone()
        # get_now_time_str_by_tz()

        # ts = 1717567890  # 示例时间戳
        # time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))

        # datetime.datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")
        # NowTimeStrCache.fast_get_now_time_str('Asia/Shanghai')
    print()

```

--- **end of file: nb_time/__init__.py** --- 

---

