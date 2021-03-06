# _*_ coding:utf-8 _*_
# Project Name: TPMService
# File Name: product
# Author： rockche
# Date:  2022/5/25  14:24
# Description :
from flask import Blueprint
from flask import request
import json
import pymysql.cursors


app_product = Blueprint("app_product", __name__)


# 使用用户名密码创建数据库链接
# PyMySQL使用文档  https://pymysql.readthedocs.io

def connectDB():
    connection = pymysql.connect(host='localhost',  # 数据库IP地址或链接域名
                                 user='root',  # 账号
                                 password='root',  # 密码
                                 port=3307,
                                 database='TPMDatas',  # 数据表
                                 charset='utf8mb4',  # 字符编码
                                 cursorclass=pymysql.cursors.DictCursor)  # 结果作为字典返回游标
    # 返回新的数据库链接对象
    return connection


@app_product.route("/api/product/list", methods=["GET"])
def product_list():
    # 初始化数据连接
    connection = connectDB()
    # 使用python的with..as控制流语句（相当于简化的try except finally）
    with connection.cursor() as cursor:
        # 查询产品信息表-按更新时间新旧排序
        sql = "SELECT * FROM `Products` ORDER BY `Update` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()

    resp_data = {
        "code": 20000,
        "data": data
    }
    return resp_data


# [POST方法]实现新建数据的数据库插入
@app_product.route("/api/product/create", methods=["POST"])
def product_create():
    # 初始化数据库连接
    connection = connectDB()
    # 定义默认返回结构体
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }

    # 获取请求传递json body
    body = request.get_data()
    body = json.loads(body)

    with connection:
        # 先做个查询，判断keycode是否重复（这里的关键词最初定义为唯一项目编号或者为服务的应用名）
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode`=%s"
            cursor.execute(select, (body["keyCode"],))
            result = cursor.fetchall()

        # 有数据说明存在相同值，封装提示直接返回
        if len(result) > 0:
            resp_data["code"] = 20001
            resp_data["message"] = "唯一编码keycode已存在"
            return resp_data

        with connection.cursor() as cursor:
            # 拼接插入语句,并用参数化%s构造防止基本的SQL注入
            # 其中id为自增，插入数据默认数据设置的当前时间
            sql = "INSERT INTO `products` (`keyCode`,`title`,`desc`,`operator`) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (body["keyCode"], body["title"], body["desc"], body["operator"]))
            # 提交执行保存插入数据
            connection.commit()

    # 按返回模版格式进行json结果返回
    return resp_data
