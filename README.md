# DailyCP
## 简介
今日校园自动打卡脚本。

## 使用说明
```bash
pip3 install -U -r requirements.txt
python3 DailyCP.py <学校前缀> <账号> <密码> <定位地址>
```
学校前缀可以在[这里](https://static.campushoy.com/apicache/tenantListSort)自行查询
## 用例
```bash
python3 DailyCP.py sise 1640915111 password 中国广东省佛山市禅城区福贤路
```
## 

### 计划任务
*请注意系统时间是否设置正确*<br>
可以使用`corntab -e`设置定时任务`0 9 * * * /usr/bin/python3 <学校前缀> <账号> <密码> <定位地址>`
##### 用例
```bash
0 9 * * * /usr/bin/python3 /home/pi/DailyCP/DailyCP.py sise 1640915111 password 中国广东省佛山市禅城区福贤路
```
### GitHub ACTIONS 自动签到
Fork本项目，在你的仓库下点击Settings，增加`SCHOOL_NAME`、`ACCOUNT`、`PASSWORD`、`ADDRESS` 4个Secrets，分别对应上述的`<学校前缀> <账号> <密码> <定位地址>`，之后打开你仓库的ACTIONS就可以了。<br>
![Secrets](https://github.com/lemofire/AutoDailyCP/blob/master/Secrets.png)

##### 签到方式：

###### 手动签到
* push
* 自己给自己star
###### 自动签到
* 每6小时自动签到一次

## Credits
* [Finch/FuckDailyCP](https://gitee.com/Finch1/FuckDailyCP)