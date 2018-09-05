import markdown
from markdown.util import etree
from markdown.extensions.headerid import HeaderIdExtension
from bs4 import BeautifulSoup

text = """```Begin
1. ************Tester provides info when submit bug*****************

[描述]：输入 查一下后天29点从成都到上海的特快，提示音为 '为你找到8月16号 29点 从成都 到 上海 的特快。’（8月16号是今天）

[期待输出]：按照VUI，应该提示 为你找到后天从成都到上海的特快

[Impact to SW]:

*************Engineer provides info after fix bug*****************
[Target]:
[Bug Type]:
[Age]:
```

```Begin
2. ************Tester provides info when submit bug*****************
[描述]：输入 查一下后天到乌镇的火车，提示音为 抱歉，你说的目的地 没有车站，换个地点试试吧。

[期待输出]:应该提示 抱歉，你说的目的地 没有火车站，换个地点试试吧。

[Impact to SW]:
*************Engineer provides info after fix bug*****************
[Target]:
[Bug Type]:
[Age]:

```

```Begin
3. ************Tester provides info when submit bug*****************
[描述]：输入 查一下从上海到杭州的火车票+第2个，第二个没有详情显示页面

[期待输出]：按照VUI应该有详情显示页面

[Impact to SW]:
*************Engineer provides info after fix bug*****************
[Target]:
[Bug Type]:
[Age]:

```

**Provide Informaiton When Submit Bug:** 

| Impact to SW | Description |
|:-----------------------------:|:-------------------------|
|Cannot recognize |比如: 没有识别结果, 没有被唤醒|
|Recognition Error |语音识别错误|
|Intention Error |意图理解错误|
|Wrong Returned Result |返回结果或者返回内容错误|
|Against Dialog Flow Spec |不符合预定义的对话流程|
|Cause Crash |软件运行异常 |
|Others | |

**Provide Information When Fix Issue:** 

|Target(需要在哪个Component上fix该Bug)|Bug Type(修改bug时，做了哪些修改)|Age(bug引入的时机) |
|:----------------------------------:|:-----------------------------:|:-----------------:|
|Component - Dialog |赋值/初始化 |Legacy issue |
|Component - Grammer/SLM/SEM V3 |算法 |Develop New Feature |
|Component - NLU |逻辑 |Update old Feature |
|Component - NCS |时序 |Fix Bug |
|Component - TTS |接口 | |
|Component - SSE |Config - user case | |
|Component - DDFW |Config - audio | |
|Component - OS |Config - NAPT Thread | |
|Component - Audio (plug-in) |Config - prompter | |
|Requirement - missing, error |Config - other | |
|Design - workflow |work around | |
|Design - UX |Lib | |
|Third Party - Tier 1 |Buffer | |
|Third Party - CP |Config - prompter | |
|Integration |Arbitration | |"
"""

html = markdown.markdown(text, extensions= ["markdown.extensions.fenced_code"])
print(html)

soup = BeautifulSoup(html)
code_block_list = soup.findAll("pre")
for code_block in code_block_list:
    print(code_block)