# coding:utf-8
from dao import *
from server import success, failed, server_error
import re


# 发送公告
def get_notice():
    try:
        f = open(r'Server\notice.txt', 'r')
        notice_content = f.read()
        return notice_content
    except Exception:
        return server_error


# 注册
def register(info_dic):
    username, pwd, pwd_confirm, safety_code = info_dic['username'], info_dic['pwd'], \
                                              info_dic['pwd_confirm'], info_dic['safety_code']
    login_name_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,12}$')
    pwd_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$')
    safety_code_re = re.compile(r'^[0-9]{6,12}$')
    if login_name_re.match(username) and pwd_re.match(pwd) and safety_code_re.match(safety_code) and pwd == pwd_confirm:
        try:
            if check(username):
                return failed
            else:
                if create_user(username, pwd, safety_code):
                    return success
                else:
                    return failed
        except Exception:
            return server_error
    else:
        return failed


# 登录
def login(info_dic, sid, onlineUser):
    username, pwd = info_dic['username'], info_dic['pwd']
    try:
        user = get_userinfo(username, pwd)
        if user is not None:
            if user[1] == username and user[2] == pwd:
                onlineUser[sid]['u_id'] = user[0]
                onlineUser[sid]['login_name'] = user[1]
                return success
            else:
                return failed
        else:
            return failed
    except Exception:
        return server_error


# 重置密码
def reset_password(info_dic):
    username, new_pwd, pwd_confirm, safety_code = info_dic['username'], info_dic['new_pwd'], \
                                              info_dic['pwd_confirm'], info_dic['safety_code']
    pwd_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$')
    if pwd_re.match(new_pwd) and new_pwd == pwd_confirm:
        try:
            user_info = get_userinfo_by_safetycode(username, safety_code)
            if user_info is not None:
                if modify_password(user_info[0], new_pwd):
                    return success
                else:
                    return failed
            else:
                return failed
        except Exception:
            return server_error
    else:
        return failed


# 提交战绩
def commit_result(info_dic, sid, onlineUser):
    if onlineUser[sid]['login_name'] is None:
        return failed
    u_id = onlineUser[sid]['u_id']
    pipe_count, len_of_time, game_level = info_dic['pipe_count'], info_dic['len_of_time'], info_dic['game_level']
    try:
        if create_record(u_id, pipe_count, len_of_time, game_level):
            return success
        else:
            return failed
    except Exception:
        return server_error


# 查询个人战绩
def query_record(sid, game_level, onlineUser):
    if onlineUser[sid]['login_name'] is None:
        return failed
    u_id = onlineUser[sid]['u_id']
    try:
        records = get_record_byId(u_id, game_level)
        if records is not None:
            return records
        else:
            return failed
    except Exception:
        return server_error


# 查询英雄榜
def query_hero_record(sid, game_level):
    # if onlineUser[sid]['login_name'] is None:
    #     return failed
    try:
        records = get_hero_record(game_level)
        if records is not None:
            return records
        else:
            return failed
    except Exception:
        return server_error


# 注销登录
def logout(sid, onlineUser):
    try:
        onlineUser[sid]['u_id'] = None
        onlineUser[sid]['login_name'] = None
        return success
    except Exception:
        return server_error




