#!/usr/bin/env python
from nonebot import on_command, CommandSession
import time,requests,json

url = "http://fundgz.1234567.com.cn/js/{}.js?rt={}"
time_stamp = int(time.time())
@on_command('fund',aliases=('查基金','基金'))
async def fund(session: CommandSession):
    code = session.get('code',prompt='输入基金代码啦~')
    fund_report = await get_fund_of_code(code)
    await session.send(fund_report)

@fund.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['code'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能为空哦😯')
    session.state[session.current_key] = stripped_arg

async def get_fund_of_code(code: str) -> str:
    if 'dkk' in code:
        fund_baijiu = "161725"
        fund_cc = "260108"
        fund_yfd = '110022'
        t1 = requests.get(url=url.format(fund_baijiu,time_stamp)).text
        j1 = json.loads(t1[8:][:-2])
        t2 = requests.get(url=url.format(fund_cc,time_stamp)).text
        j2 = json.loads(t2[8:][:-2])
        t3 = requests.get(url=url.format(fund_yfd,time_stamp)).text
        j3 = json.loads(t3[8:][:-2])
        return f'{j1["jzrq"]}\n{j1["name"]}-> {j1["gszzl"]}%\n{j2["name"]}-> {j2["gszzl"]}%\n{j3["name"]}-> {j3["gszzl"]}%\n截止时间{j1["gztime"]}'
    else:
        t1 = requests.get(url=url.format(code,time_stamp)).text
        j1 = json.loads(t1[8:][:-2])
        return f'{j1["jzrq"]}\n{j1["name"]}-> {j1["gszzl"]}%\n截止时间{j1["gztime"]}'