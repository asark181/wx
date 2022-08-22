from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
ymq_date = os.environ['YMQ_DATE']
city = os.environ['CITY']
birthday1 = os.environ['BIRTHDAY1']
birthday2 = os.environ['BIRTHDAY2']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
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


def get_count():
    #delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    #return delta.days
    next = datetime.strptime(str(date.today().year) + "-" + start_date, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days

def get_ymqcount():
    next = datetime.strptime(str(date.today().year) + "-" + ymq_date, "%Y-%m-%d")
    if next < datetime.now():
        les = (today-next).days
    if les < 7:
        return "姨妈期第" + les.__str__() + "天"
    else:
        return "距离姨妈期开始还有" + ((next.replace(month=next.month+1)-today).days+7).__str__() + "天"

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
wea, temperature, minTemperature, maxTemperature = get_weather()
data = {"yy": {"value": yy},
        "mm": {"value": mm},
        "dd": {"value": dd},
        "xq": {"value": xq},
        "city": {"value": city},
        "weather": {"value": wea},
        "temperature": {"value": temperature},
        "minTemperature": {"value": minTemperature},
        "maxTemperature": {"value": maxTemperature},
        "love_days": {"value": get_count()},
        "ymq": {"value": get_ymqcount()},
        "birthday_left1": {"value": get_birthday1()},
        "birthday_left2": {"value": get_birthday2()},
        "words": {"value": get_words(), "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
