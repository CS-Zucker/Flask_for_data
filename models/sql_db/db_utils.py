import pymysql

config = {
    'MYSQL_HOST': 'localhost',
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': '1234',
    'DATABASE_NAME': 'test'
}


def select(sql):
    """
    功能; 使用sql语句查询数据库信息.
    参数: sql(string)
    """
    db = pymysql.connect(host=config['MYSQL_HOST'], user=config['MYSQL_USER'], password=config['MYSQL_PASSWORD'], database=config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        # print('query success')
        # print('query success')
    except:
        # print('query loss')
        db.rollback()
    cur.close()
    db.close()
    return result

def update(sql):
    """
    功能; 使用sql语句更新数据库信息。
    参数: sql(string)
    """
    db = pymysql.connect(host=config['MYSQL_HOST'], user=config['MYSQL_USER'], password=config['MYSQL_PASSWORD'], database=config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    flag = False
    try:
        cur.execute(sql)
        db.commit()
        flag = True
        # print('update success')
        # print('update success')
    except:
        # print('update loss')
        db.rollback()
    cur.close()
    db.close()
    return flag


def insert_db(table, key, value):
    """
    功能: 获取用户在前端 GET / POST 请求中的数据， 进行数据库插入操作
    :param table: 插入数据库->表的名称
    :param key: 插入数据库->表的字段名
    :param value: 插入数据库->表中字段的值
    :return: 无
    """
    sql = "INSERT INTO {}({}) VALUES ({}); ".format(table, key, value)
    print(sql)
    res_flag = update(sql)
    return res_flag

def select_db(table, res_key, search_key, search_value):
    """
    功能: 获取用户在前端 GET / POST 请求中的数据， 进行数据库查询操作
    :param table: 查询数据库->表的名称
    :param res_key: 查询数据库->查询结果_字段名
    :param search_key: 查询数据库->条件_字段名
    :param search_value: 查询数据库->条件_字段的值
    :return: 无
    """
    sql = "SELECT {} FROM {} WHERE {} = '{}'; ".format(res_key, table, search_key, search_value)
    print(sql)
    res = select(sql)
    return res
