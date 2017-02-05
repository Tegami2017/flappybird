# -*- coding: utf-8 -*-
import socket, netstream

connected = False
sock = None
serialID = 0  # server向客户端发回的序列ID号
isSet = False


def connect(gameScene):
    global connected, sock
    if connected:
        return connected
    # connect server
    host = "10.250.191.139"
    port = 9234
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except:
        connected = False
        return connected

    connected = True

    # 始终接收服务端消息
    def receiveServer(dt):
        global connected, serialID
        import game_controller
        if not connected:
            return
        data = netstream.read(sock)
        if data == netstream.TIMEOUT or data == netstream.CLOSED or data == netstream.EMPTY:
            return
        if 'server closed' in data:
             print data
             connected = False
             game_controller.back_to_login()

        # 客户端SID
        if 'sid' in data:
            serialID = data['sid']

        # 请求公告的返回信息， -1为服务器发生异常
        if 'notice' in data:
            if data['notice'] != -1:
                game_controller.showContent(data['notice'])  # showContent is from game_controller
            else:
                game_controller.showContent('server error')

        # 请求英雄榜的返回信息，  0：无数据  -1：服务器异常
        if 'query_hero_record' in data:
            a = game_controller.gameScene.get("rank_data_layer")
            if data['query_hero_record'] == -1:
                a.records[0][0].element.text = 'server error'
            elif data['query_hero_record'] == 0:
                a.records[0][0].element.text = 'no data'
            else:
                j = 0
                for each_record in data['query_hero_record']:
                    n, p, d = tuple([i for i in each_record])
                    a.records[j][0].element.text, a.records[j][1].element.text, a.records[j][2].element.text = \
                        n, str(p), d
                    j += 1

        # 请求个人战绩的返回信息，  0：无数据  -1：服务器异常
        if 'query_record' in data:
            a = game_controller.gameScene.get("rank_data_layer")
            if data['query_record'] == -1:
                a.records[0][0].element.text = 'server error'
            elif data['query_record'] == 0:
                a.records[0][0].element.text = 'no data'
            else:
                j = 0
                for each_record in data['query_record']:
                    n, p, d = tuple([i for i in each_record])
                    a.records[j][0].element.text, a.records[j][1].element.text, a.records[j][2].element.text = \
                        n, str(p), d
                    j += 1

        # 请求注销的返回信息，  1：注销成功  -1：服务器异常
        if 'logout' in data:
            if data['logout'] == -1:
                pass
            elif data['logout'] == 1:
                game_controller.logout()

        # 请求提交战绩的返回信息，  1：提交成功  0：提交失败  -1：服务器异常
        if 'commit_result' in data:
            if data['commit_result'] == -1:
                pass
            elif data['commit_result'] == 0:
                pass
            elif data['commit_result'] == 1:
                pass

    gameScene.schedule(receiveServer)
    return connected


def get_send_data():
    send_data = {}
    send_data['sid'] = serialID
    return send_data


# 向服务器请求公告
def request_notice():
    send_data = get_send_data()
    send_data['notice'] = 'request notice'
    netstream.send(sock, send_data)


# 向服务器发送注册请求
def request_register(username, pwd, pwd_confirm, safety_code):
    send_data = get_send_data()
    send_data['register'] = {'username': username, 'pwd': pwd, 'pwd_confirm': pwd_confirm, 'safety_code': safety_code}
    netstream.send(sock, send_data)


# 向服务器发送登录请求
def request_login(username, pwd):
    send_data = get_send_data()
    send_data['login'] = {'username': username, 'pwd': pwd}
    netstream.send(sock, send_data)


# 向服务器发送重置密码请求
def request_reset_password(username, new_pwd, pwd_confirm, safety_code):
    send_data = get_send_data()
    send_data['reset_password'] = \
        {'username': username, 'new_pwd': new_pwd, 'pwd_confirm': pwd_confirm, 'safety_code': safety_code}
    netstream.send(sock, send_data)


# 向服务器提交战绩
def request_commit_result(pipe_count, len_of_time, game_level):
    send_data = get_send_data()
    send_data['commit_result'] = {'pipe_count': pipe_count, 'len_of_time': len_of_time, 'game_level': game_level}
    netstream.send(sock, send_data)


# 向服务器请求个人战绩信息
def request_user_record(game_level=4):
    send_data = get_send_data()
    send_data['query_record'] = game_level
    netstream.send(sock, send_data)
    # print netstream.read(sock)


# 向服务器请求英雄榜信息
def request_hero_record(game_level=4):
    send_data = get_send_data()
    send_data['query_hero_record'] = game_level
    netstream.send(sock, send_data)
    # print netstream.read(sock)


# 向服务器请求注销
def request_logout():
    send_data = get_send_data()
    send_data['logout'] = ''
    netstream.send(sock, send_data)
    # print netstream.read(sock)
