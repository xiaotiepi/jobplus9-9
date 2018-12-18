# jobplus9-9

## 环境配置

- python3.6
- pip安装requirement.txt。命令或许是`sudo pip3 install requirement.txt`.

## 测试使用方法

### 单元测试

在与manage.py同级的目录下，在命令行输入：
```shell
export FLASK_APP=manage.py
export FLASK_DEBUG=1
flask run
```

> windows下把export换成set

### 功能测试

在顶级目录jobplus9-9下，

在与manage.py同级的目录下，在命令行输入：

```shell
python tests/functional_tests.py
```

> 或许你的命令是`python3`

当结果是`AssertionError: Finish the test!`，表明测试通过（虽然看起来哪里错了）。
## 组员

- [黎明之翼_封心](https://github.com/Raymond38324)
- [蒲小帅](https://github.com/puxiaoshuai)
- [黄健楸](https://github.com/linxixizhi/)
- [小铁皮](https://github.com/xiaotiepi)
- [lightningwow](https://github.com/limi2018)
