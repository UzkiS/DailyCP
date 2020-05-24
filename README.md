# FuckDailyCP
#### 简介
今日校园自动打卡脚本。
可以挂服务器上定时自动打卡。
健康的人可以用一下（雾）。
![](doc/img.png)
#### 使用说明
理论上支持所有学校，针对不同的学校，代码中有这样一行
```python
def __init__(self, host="aust.campusphere.net"):
```
其中aust是我们学校的简称，请替换成你们的学校的。
然后运行以下命令，根据提示输入账号（通常是学号），密码，自定义定位地址即可。
```bash
pip3 install -U -r requirements.txt
python3 DailyCP.py
```
#### 挂服务器提示
自己先建立一个文件里面存了帐号和密码，然后创建定时任务。
```bash
cat /root/FuckDailyCP/account | python3 /root/FuckDailyCP/DailyCP.py >> /root/FuckDailyCP/history.log
```
我已经挂服务器三个月惹，稳的不行。
#### 效果截图
![](doc/psc.jpg)
#### 最后
小老板，给个Star？
联系QQ：2836365231
脚本失效请提Issue，作者失联请QQ留言。