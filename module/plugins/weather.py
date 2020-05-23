#!/usr/bin/env python
from nonebot import on_command, CommandSession
import requests
import json

@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    weather_report = await get_weather_of_city(city)
    await session.send(weather_report)

@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['city'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('要查询的城市名称不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg

async def get_weather_of_city(city: str) -> str:
    weather = requests.get(url="http://wthrcdn.etouch.cn/weather_mini?city="+city).text
    if "invilad-citykey" in weather:
        return "没有这个城市呢~"
    weather = json.loads(weather)
    #weather = weather["data"]["forecast"][0]
    Data = weather["data"]["forecast"][0]["date"]  #22日星期五
    High = weather["data"]["forecast"][0]["high"][3:]
    fengli = weather["data"]["forecast"][0]["fengli"][9:][:-3:]
    low = weather["data"]["forecast"][0]["low"][3:]
    fengxiang = weather["data"]["forecast"][0]["fengxiang"]
    type1 = weather["data"]["forecast"][0]["type"]
    return f'{Data}->{city}\n最高气温{High},最低气温{low}\n{type1},有{fengli}{fengxiang}😋'