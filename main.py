from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
love_date = os.environ['LOVE_DATE']
ymq_date = os.environ['YMQ_DATE']
city1 = os.environ['CITY1']
city2 = os.environ['CITY2']
birthday1 = os.environ['BIRTHDAY1']
birthday2 = os.environ['BIRTHDAY2']

key = "6f4569222d01a6f1d1fca322179d1724"

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id1 = os.environ["USER_ID1"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather1():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city1
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])


def get_weather1():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city1
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])


def get_xz(xz):
    url = "http://web.juhe.cn/constellation/getAll?consName=" + xz + "&type=today&key=" + key
    res = requests.get(url).json()
    return res['color'], res['health'], res['work'], res['money'], res['number'], res['summary'], res['all'], res['name']


lc, lh, lw, lm, ln, ls, la, lna = get_xz("水瓶座")
rc, rh, rw, rm, rn, rs, ra, rna = get_xz("天蝎座")


def get_weather2():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city2
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])


def get_day():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    dayOfWeek = datetime.today().weekday()
    xq = week_list[dayOfWeek]
    yy = datetime.now().year
    mm = datetime.now().month
    dd = datetime.now().day
    return xq, yy, mm, dd


def get_djs():
    # delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    # return delta.days
    next = datetime.strptime(str(date.today().year) + "-" + start_date, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_count():
    delta = today - datetime.strptime(love_date, "%Y-%m-%d")
    return delta.days


def get_ymqcount():
    next = datetime.strptime(str(date.today().year) + "-" + ymq_date, "%Y-%m-%d")
    if next < datetime.now():
        les = (today - next).days + 1
        if les <= 7:
            return "姨妈期第" + les.__str__() + "天"
        else:
            return "距离姨妈期开始还有" + ((next.replace(month=next.month + 1) - today).days + 7).__str__() + "天"
    else:
        return "距离姨妈期开始还有" + ((next - today).days + 1).__str__() + "天"


def get_birthday1():
    next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_birthday2():
    next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
xq, yy, mm, dd = get_day()
wea1, temperature1, minTemperature1, maxTemperature1 = get_weather1()
wea2, temperature2, minTemperature2, maxTemperature2 = get_weather2()


def get_weather_color1():
    if wea1 == "晴":
        return "#FFCC66"
    if wea1 == "多云":
        return "#CCCCCC"
    if wea1 == "阴":
        return "#777777"
    if wea1 == "小雨" or wea1 == "大雨" or wea1 == "中雨":
        return "#33CCFF"
    else:
        return "#FFFF00"


def get_weather_color2():
    if wea2 == "晴":
        return "#FFCC66"
    if wea2 == "多云":
        return "#CCCCCC"
    if wea2 == "阴":
        return "#777777"
    if wea2 == "小雨" or wea2 == "大雨" or wea2 == "中雨":
        return "#33CCFF"
    else:
        return "#FFFF00"


def get_t_color1():
    if temperature1.__int__() <= 30:
        return "#0066FF"
    else:
        return "#FF5511"


def get_mint_color1():
    if minTemperature1.__int__() <= 30:
        return "#0066FF"
    else:
        return "#FF5511"


def get_maxt_color1():
    if maxTemperature1.__int__() <= 30:
        return "#0066FF"
    else:
        return "#FF5511"


def get_t_color2():
    if temperature2.__int__() <= 30:
        return "#0066FF"
    else:
        return "#FF5511"


def get_mint_color2():
    if minTemperature2.__int__() <= 30:
        return "#0066FF"
    else:
        return "#FF5511"


def get_maxt_color2():
    if maxTemperature2.__int__() <= 30:
        return "#0066FF"
    else:
        return "#FF5511"


data1 = {"yy": {"value": yy},
         "mm": {"value": mm},
         "dd": {"value": dd},
         "xq": {"value": xq},
         "city": {"value": city1},
         "weather": {"value": wea1, "color": get_weather_color1()},
         "temperature": {"value": temperature1, "color": get_t_color1()},
         "minTemperature": {"value": minTemperature1, "color": get_mint_color1()},
         "maxTemperature": {"value": maxTemperature1, "color": get_maxt_color1()},
         "djs": {"value": get_djs()},
         "love_days": {"value": get_count(), "color": "#FF33FF"},
         "ymq": {"value": get_ymqcount(), "color": "#FF0000"},
         "birthday_left1": {"value": get_birthday1()},
         "birthday_left2": {"value": get_birthday2()},
         "h": {"value": rh, "color": "#B94FFF"},
         "c": {"value": rc, "color": "#B94FFF"},
         "w": {"value": rw, "color": "#B94FFF"},
         "m": {"value": rm, "color": "#B94FFF"},
         "a": {"value": ra, "color": "#B94FFF"},
         "n": {"value": rn, "color": "#B94FFF"},
         "s": {"value": rs, "color": "#AA7700"},
         "na": {"value": rs},
         "words": {"value": get_words(), "color": get_random_color()}}

data2 = {"yy": {"value": yy},
         "mm": {"value": mm},
         "dd": {"value": dd},
         "xq": {"value": xq},
         "city": {"value": city2},
         "weather": {"value": wea2, "color": get_weather_color2()},
         "temperature": {"value": temperature2, "color": get_t_color2()},
         "minTemperature": {"value": minTemperature2, "color": get_mint_color2()},
         "maxTemperature": {"value": maxTemperature2, "color": get_maxt_color2()},
         "djs": {"value": get_djs()},
         "love_days": {"value": get_count(), "color": "#FF33FF"},
         "ymq": {"value": get_ymqcount(), "color": "#FF0000"},
         "birthday_left1": {"value": get_birthday1()},
         "birthday_left2": {"value": get_birthday2()},
         "h": {"value": lh, "color": "#B94FFF"},
         "c": {"value": lc, "color": "#B94FFF"},
         "w": {"value": lw, "color": "#B94FFF"},
         "m": {"value": lm, "color": "#B94FFF"},
         "a": {"value": la, "color": "#B94FFF"},
         "n": {"value": ln, "color": "#B94FFF"},
         "s": {"value": ls, "color": "#AA7700"},
         "na": {"value": ls},
         "words": {"value": get_words(), "color": get_random_color()}}
res1 = wm.send_template(user_id1, template_id, data1)
res2 = wm.send_template(user_id2, template_id, data2)
print(res1)
print(res2)
