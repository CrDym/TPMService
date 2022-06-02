# _*_ coding:utf-8 _*_
# Project Name: TPMService
# File Name: product
# Author： rockche
# Date:  2022/5/25  14:24
# Description :
from flask import Blueprint
import pymysql.cursors

app_product = Blueprint("app_product", __name__)

# 使用用户名密码创建数据库链接
# PyMySQL使用文档  https://pymysql.readthedocs.io
connection = pymysql.connect(host='localhost',  # 数据库IP地址或链接域名
                             user='root',  # 账号
                             password='root',  # 密码
                             port=3307,
                             database='TPMDatas',  # 数据表
                             charset='utf8mb4',  # 字符编码
                             cursorclass=pymysql.cursors.DictCursor)  # 结果作为字典返回游标


@app_product.route("/api/product/list", methods=["GET"])
def product_list():
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
