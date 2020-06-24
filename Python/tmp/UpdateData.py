# coding:utf8
import time
import datetime
import os
import schedule


def update():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(u'{} Updating...\n'.format(now))
    py = 'python GetData2csv.py'  # python命令 + B.py
    re = os.system(py)
    if re == 0:
        print("Success\n")
    else:
        print("Fail\n")


if __name__ == '__main__':
    schedule.every(1).hours.do(update)
    while True:
        now = datetime.datetime.now()
        print("Check Point: {}\n".format(now.strftime('%Y-%m-%d %H:%M:%S')))
        schedule.run_pending()
        time.sleep(300)


