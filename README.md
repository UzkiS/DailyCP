# DailyCP
#### 简介
今日校园自动打卡脚本。
forked from https://gitee.com/Finch1/FuckDailyCP, 感谢原作者。<br>
主要修改了使用方式
#### 使用说明
```bash
pip3 install -U -r requirements.txt
python3 DailyCP.py <学校前缀> <账号> <密码> <定位地址>
```
#### 用例
```bash
python3 DailyCP.py sise 1640915111 password 中国广东省佛山市禅城区福贤路
```
#### 计划任务
*请注意系统时间是否设置正确*<br>
可以使用`corntab -e`设置定时任务<br>
`0 9 * * * /usr/bin/python3 <学校前缀> <账号> <密码> <定位地址>`
##### 用例
```bash
0 9 * * * /usr/bin/python3 /home/pi/DailyCP/DailyCP.py sise 1640915111 password 中国广东省佛山市禅城区福贤路
```