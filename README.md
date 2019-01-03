# jobplus9-9

## 环境配置

- python3.6
- pip安装requirement.txt。命令或许是`sudo pip3 install requirement.txt`.
- 如果MySQL数据库有密码，记得配置环境变量，若密码为123456：
`export DEVELOP_DATABASE_URL=mysql://root:123456@localhost:3306/plus_job?charset=utf8`
- 迁移数据库，其中，`flask db init`会创建migrations，若该文件已存在，跳过此行代码。
```shell
export FLASK_APP=manage.py
export FLASK_DEBUG=1
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

> 若在Windows上，请把export改完set。

## 数据生成
1. 确保存在`plus_job`名称的数据库，manage.py同级目录运行 `flask db upgrade`  生成迁移文件
2. 运行spider_laou.py文件，爬取拉钩职位信息及对应的公司信息，保存到jobs.json文件
（太频繁，拉钩会弹出登录页）
3. 运行 create_data.py文件，会默认生成一个boss账号，该账号会关联数据中生成的第一个公司。每个公司下，有一个对应的职位
    如果create_data.py生成数据报错no model jobplus，可以运行create.py文件

## 测试使用

先在`manage.py`中更改模式：
```python
app = create_app('testing')
```

先运行Flask服务器，再与manage.py同级的目录下，运行`flask test`:

```shell
export FLASK_APP=manage.py
export FLASK_DEBUG=1
flask test
```

> windows下把export换成set

## 开发者

- [黎明之翼_封心](https://github.com/Raymond38324)
- [蒲小帅](https://github.com/puxiaoshuai)
- [黄健楸](https://github.com/linxixizhi/)
- [小铁皮](https://github.com/xiaotiepi)
- [lightningwow](https://github.com/limi2018)

> 排名不分前后
