# -!- coding: utf-8 -!-

import time
import datetime
import os
import schedule

class UpdataData:
    def update(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(u'{} Updating...\n'.format(now))
        py = 'python GetData.py'  # python命令 + B.py
        re = os.system(py)
        if re == 0:
            print("Success\n")
        else:
            print("Fail\n")

    def main_update(self):
        schedule.every(1).hours.do(self.update)
        while True:
            now = datetime.datetime.now()
            print("Check Point: {}\n".format(now.strftime('%Y-%m-%d %H:%M:%S')))
            schedule.run_pending()
            time.sleep(300)

test = UpdataData()
test.main_update()
