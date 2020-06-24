import pymysql
import datetime
import csv

def getNow():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 连接数据库
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="weather",
    charset="utf8"
)

# 返回一个可以执行 MySQL 语句的光标对象
cursor = db.cursor()


# 查询正在操作的数据库
cursor.execute("SELECT DATABASE()")
dbName = cursor.fetchone()
print("[%s]: The Operating Database: `%s`\n" % (getNow(), dbName[0]))


# 查询其数据库下的所有表项
cursor.execute("SHOW TABLES")
tbName = cursor.fetchall()
print("[%s]: This Database Contains Tables: %s\n" % (getNow(), [tb[0] for tb in tbName]))


"""
测试 MySQL 与 Python 的连接和同步：
1. 清空表 data 和 data2 的全部内容
2. 填入 data 和 data2 的最新信息
"""


# 清空表中所有内容
def delTable(name):
    sql = "TRUNCATE TABLE {}".format(name)
    try:
        # 清空表
        cursor.execute(sql)
        # 向数据库提交
        db.commit()
        print("[{}]: Table `{}` Deleted Successfully\n".format(getNow(), name))
    except:
        # 发生错误时回滚
        db.rollback()
        print("[{}] Error: Unable to Delete Table `{}`\n".format(getNow(), name))


# 将 csv 文件写入表
def updateTable(file, tb):
    try:
        with open('../{}.csv'.format(file), "r", encoding='UTF-8') as f:
            f_csv = csv.reader(f)
            next(f_csv)  # 忽略 csv 文件表头
            for row in f_csv:
                # 逐行插入 csv 文件中的数据
                sql = "INSERT INTO %s VALUES %s" % (tb, str(tuple(row)))
                print("[{}]:".format(getNow()), sql)
                cursor.execute(sql)
                db.commit()
            print("[{}]: Table `{}` Uploading Done\n".format(getNow(), tb))
    except:
        print("[{}] Error: Unable to Write into Table `{}`\n".format(getNow(), tb))
        db.rollback()


delTable('data')
updateTable('Data', 'data')


delTable('data2')
updateTable('Data2', 'data2')
