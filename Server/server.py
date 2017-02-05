# -*- coding: utf-8 -*-
import socket
import select
import netstream
import random
import pickle
import os
import traceback
import services
success = 1
failed = 0
server_error = -1
import threading

HOST = "10.250.191.139"
disconnected_list = []  # 断开连接的客户端列表
onlineUser = {}         # 在线客户端列表
sid = 0                 # 给用户分配的ID，由0开始


# 给全服发信息
def send_to_all_user(message):
    for each_sid in onlineUser:
        netstream.send(onlineUser[each_sid]['connection'], {'server closed': message})


# 返回结果
def send_result(u_sid, key, result):
    sendData = {}
    sendData[key] = result
    netstream.send(onlineUser[u_sid]['connection'], sendData)


# 用户断开连接时用来移除服务器的用户信息
def remove_user(connection):
    for each_sid in onlineUser:
        if onlineUser[each_sid]['connection'] is connection:
            del onlineUser[each_sid]
            break


# 主函数
def main():
    global HOST, disconnected_list, onlineUser, game_started, sid
    s = socket.socket()

    host = HOST
    port = 9234

    s.bind((host, port))    # 建立服务器
    s.listen(4)

    inputs = []             # 用来存放socket的列表
    inputs.append(s)        # 把socket放进列表中
    print 'server start! listening host:', host, ' port:', port

    while inputs:
        try:
            rs, ws, es = select.select(inputs, [], [])   # 监听socket列表的变化情况
            for r in rs:
                if r is s:                               # 发生变化的是服务器socket
                    print 'sid:', sid
                    # accept
                    connection, addr = s.accept()         # 获取用户地址和connection
                    print 'Got connection from' + str(addr)
                    inputs.append(connection)             # 放进监听列表
                    sendData = {}
                    sendData['sid'] = sid
                    netstream.send(connection, sendData)  # 把sid返回给用户

                    cInfo = {}                            # 建立客户端信息
                    cInfo['connection'] = connection
                    cInfo['addr'] = str(addr)
                    cInfo['ready'] = False
                    cInfo['login_name'] = None
                    cInfo['u_id'] = None
                    onlineUser[sid] = cInfo               # 把客户端信息放入客户端列表中
                    print 'Client Information:'           # 显示所有用户的信息
                    for each_sid in onlineUser:
                        print onlineUser[each_sid]
                    sid += 1
                else:
                    recvData = netstream.read(r)           # 获取用户请求信息
                    if recvData == netstream.CLOSED or recvData == netstream.TIMEOUT:    # socket关闭
                        if r.getpeername() not in disconnected_list:
                            disconnected_list.append(r.getpeername())   # 把客户端信息放入离线列表中
                            remove_user(r)  # 把用户在客户端列表中移除
                            print str(r.getpeername()) + 'disconnected'
                    else:  # 根据收到的request发送response
                        if 'sid' in recvData:
                            number = recvData['sid']                # 获取用户sid,通过sid获取cInfo的信息
                            print 'receive notice request from user id:', number
                            # 处理请求
                            if 'notice' in recvData:                # 请求公告
                                send_result(number, 'notice', services.get_notice())
                                continue
                            if 'register' in recvData:              # 请求注册
                                info_dic = recvData['register']
                                send_result(number, 'register', services.register(info_dic))
                                continue
                            if 'login' in recvData:                 # 请求登录
                                info_dic = recvData['login']
                                send_result(number, 'login', services.login(info_dic, number, onlineUser))
                                print onlineUser[number]
                                continue
                            if 'reset_password' in recvData:        # 请求重置密码
                                info_dic = recvData['reset_password']
                                send_result(number, 'reset_password', services.reset_password(info_dic))
                                continue
                            if 'commit_result' in recvData:         # 请求提交战绩
                                info_dic = recvData['commit_result']
                                send_result(number, 'commit_result',
                                            services.commit_result(info_dic, number, onlineUser))
                                continue
                            if 'query_record' in recvData:          # 请求个人战绩
                                game_level = recvData['query_record']
                                send_result(number, 'query_record',
                                            services.query_record(number, game_level, onlineUser))
                                continue
                            if 'query_hero_record' in recvData:     # 请求英雄榜战绩
                                game_level = recvData['query_hero_record']
                                send_result(number, 'query_hero_record', services.query_hero_record(number, game_level))
                                continue
                            if 'logout' in recvData:                # 请求注销
                                send_result(number, 'logout', services.logout(number, onlineUser))

        except Exception:
            traceback.print_exc()
            print 'Error: socket 链接异常'


def server_debug():
    while True:
        message = raw_input(">")
        if message == 'closed':
            send_to_all_user("服务器已关闭")

if __name__ == "__main__":
    main_thread = threading.Thread(target=main)  # 接收信息线程
    debug_thread = threading.Thread(target=server_debug)  # 执行服务器指令线程
    main_thread.start()
    debug_thread.start()
