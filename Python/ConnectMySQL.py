# -!- coding: utf-8 -!-

import pymysql
import datetime
import csv

class ConnectMySQL:
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

    def getNow(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def checkMySQL(self):
        # 查询正在操作的数据库
        self.cursor.execute("SELECT DATABASE()")
        dbName = self.cursor.fetchone()
        print("[%s]: The Operating Database: `%s`\n" % (self.getNow(), dbName[0]))

        # 查询其数据库下的所有表项
        self.cursor.execute("SHOW TABLES")
        tbName = self.cursor.fetchall()
        print("[%s]: This Database Contains Tables: %s\n" % (self.getNow(), [tb[0] for tb in tbName]))

    # 清空表中所有内容
    def delTable(self, name):
        sql = "TRUNCATE TABLE {}".format(name)
        try:
            # 清空表
            self.cursor.execute(sql)
            # 向数据库提交
            self.db.commit()
            print("[{}]: Table `{}` Deleted Successfully\n".format(self.getNow(), name))
        except:
            # 发生错误时回滚
            self.db.rollback()
            print("[{}] Error: Unable to Delete Table `{}`\n".format(self.getNow(), name))


    # 将 csv 文件写入表
    def updateTable(self, file, tb):
        try:
            with open('../{}.csv'.format(file), "r", encoding='UTF-8') as f:
                f_csv = csv.reader(f)
                next(f_csv)  # 忽略 csv 文件表头
                for row in f_csv:
                    # 逐行插入 csv 文件中的数据
                    sql = "INSERT INTO %s VALUES %s" % (tb, str(tuple(row)))
                    print("[{}]:".format(self.getNow()), sql)
                    self.cursor.execute(sql)
                    self.db.commit()
                print("[{}]: Table `{}` Uploading Done\n".format(self.getNow(), tb))
        except:
            print("[{}] Error: Unable to Write into Table `{}`\n".format(self.getNow(), tb))
            self.db.rollback()

    def main_upate(self, fname1, fname2):
        self.delTable('data')
        self.updateTable('{}'.format(fname1), 'data')

        self.delTable('data2')
        self.updateTable('{}'.format(fname2), 'data2')

if __name__ is '__main__':
    test = ConnectMySQL()
    test.main_upate('SevenDays', 'SevenDaysPeriod')