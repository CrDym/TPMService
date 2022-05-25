# _*_ coding:utf-8 _*_
# Project Name: TPMService
# File Name: user
# Author： rockche
# Date:  2022/5/25  14:12
# Description :
from flask import request
import json

from flask import Blueprint

app_user = Blueprint('app_user', __name__)


@app_user.route("/api/user/login", methods=["POST"])
def login():
    data = request.get_data()
    js_data = json.loads(data)

    if "username" in js_data and js_data["username"] == "admin":
        result_success = {"code": 20000, "data": {"token": "admin-token"}}
        return result_success
    else:
        result_error = {"code": 60204, "message": "账号密码错误"}
        return result_error


@app_user.route("/api/user/info", methods=["GET"])
def info():
    token = request.args.get("token")
    if token == "admin-token":
        result_success = {
            "code": 20000,
            "data": {
                "roles": ["admin"],
                "introduction": "I am a super administrator",
                "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                "name": "Super Admin"}
        }
        return result_success
    else:
        result_error = {"code": 60204, "message": "用户信息获取错误"}
        return result_error
