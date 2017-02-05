# coding:utf-8
import MySQLdb
import datetime


# 检查用户名
def check(username):
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "select * from u_info where login_name = '%s'"
        cursor.execute(sql % username)
        if cursor.rowcount == 0:
            return False
        else:
            for each_info in cursor.fetchall():
                if username == each_info[1]:
                    return True
            return False
    except Exception as e:
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 获取用户资料
def get_userinfo(username, pwd):
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "select * from u_info where login_name = '%s' and pwd = '%s'"
        cursor.execute(sql % (username, pwd))
        if cursor.rowcount == 0:
            return None
        else:
            for each_info in cursor.fetchall():
                if username == each_info[1] and pwd == each_info[2]:
                    return each_info
            return None
    except Exception as e:
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 通过安全码获取用户资料
def get_userinfo_by_safetycode(username, safety_code):
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "select * from u_info where login_name = '%s' and safety_code = '%s'"
        cursor.execute(sql % (username, safety_code))
        if cursor.rowcount == 0:
            return None
        else:
            for each_info in cursor.fetchall():
                if username == each_info[1] and safety_code == each_info[3]:
                    return each_info
            return None
    except Exception as e:
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 新建用户
def create_user(username, pwd, safety_code):
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "insert into u_info (login_name,pwd,safety_code) VALUES ('%s','%s','%s')"
        cursor.execute(sql % (username, pwd, safety_code))
        coon.commit()
        if cursor.rowcount == 0:
            return False
        else:
            return True
    except Exception as e:
        coon.rollback()
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 更改密码
def modify_password(u_id, new_pwd):
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "UPDATE u_info SET pwd = '%s' where Id = %s"
        cursor.execute(sql % (new_pwd, u_id))
        coon.commit()
        if cursor.rowcount == 0:
            return False
        else:
            return True
    except Exception as e:
        coon.rollback()
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 生成战绩
def create_record(u_id, pipe_count, len_of_time, game_level):
    generate_time = datetime.datetime.now().strftime('%Y/%m/%d')
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "insert into user_record (pipe_count,len_of_time,game_level,generate_time,u_id) VALUES (%s,%s,%s,'%s',%s)"
        cursor.execute(sql % (pipe_count, len_of_time, game_level, generate_time, u_id))
        coon.commit()
        if cursor.rowcount == 0:
            return False
        else:
            return True
    except Exception as e:
        coon.rollback()
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 获取战绩
def get_record_byId(u_id, game_level):
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "SELECT u.login_name,r.pipe_count,r.generate_time FROM u_info u,user_record r WHERE u.Id=r.u_id \
              and game_level = %s and u.Id = %s order by pipe_count DESC"
        cursor.execute(sql % (game_level, u_id))
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.fetchmany(5)
    except Exception as e:
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 获取英雄榜
def get_hero_record(game_level):
    try:
        coon = get_connection()
        cursor = coon.cursor()
        sql = "SELECT u.login_name,r.pipe_count,r.generate_time FROM u_info u,user_record r WHERE u.Id=r.u_id \
              and game_level = %s order by pipe_count DESC"
        cursor.execute(sql % game_level)
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.fetchmany(5)
    except Exception as e:
        print e
        raise e
    finally:
        cursor.close()
        coon.close()


# 获取数据库连接
def get_connection():
    conn = MySQLdb.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           passwd='hiahiahia',
                           db='flappybird',
                           charset='utf8')
    return conn

if __name__ == '__main__':
    print create_record(1, 60, 80.5, 4)

