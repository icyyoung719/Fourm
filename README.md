# 软件工程

### 介绍
2024秋软件工程小组作业
### 软件架构
软件架构说明

### 安装教程
```commandline
git clone https://gitee.com/yuxinyu0503/software-engineering.git
```
### 环境依赖
1.  python 3.8
```shell
pip install -r requirements.txt
```

#### pip list
```shell
Package            Version
------------------ -------
asgiref            3.8.1
backports.zoneinfo 0.2.1
Django             4.2.16
pip                24.2
setuptools         75.1.0
sqlparse           0.5.1
typing_extensions  4.12.2
tzdata             2024.2
wheel              0.44.0
```

#### 使用说明
```shell
1.  cd software-engineering
2.  python manage.py makemigrations
3.  python manage.py migrate
```
#### 本地部署运行
```shell
1.  修改software-engineering/settings.py中的DEBUG为True
2.  python manage.py runserver
```
#### 服务器部署
1.  修改software-engineering/settings.py中的DEBUG为False
2.  python manage.py runserver 0.0.0.0:8000
3.  使用cmd命令行输入：ipconfig ，查看本机ip（一般为无线局域网适配器 WLAN:的ipv4地址）
4.  在浏览器中输入：http://本机ip:8000/ 即可访问

#### 辅助工具
1.  https://sqlitebrowser.org/dl/   用于下载查看数据库的工具