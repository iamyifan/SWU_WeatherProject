import csv
import requests
from bs4 import BeautifulSoup

# 浏览器代理
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
}


# 获取 url 下的源码
def get_url(url):
    data = requests.get(url, headers=headers).content.decode("utf-8")
    soup = BeautifulSoup(data, "html5lib")
    return soup


# 获取源码中的七天的天气数据
def get_data(soup):
    hanmls = soup.find("div", class_="hanml")
    conmidtabs = hanmls.find_all("div", class_="conMidtab")
    return conmidtabs


# 获取每天的气象数据
def get_tables(conmidtab):
    tables = conmidtab.find_all("table")
    data = []
    # 遍历当天该地区的所有城市
    for table in tables:
        # 在表头提取日期
        tmp_date = list(table.find_all("tr")[0].find("td", height="37", colspan="3").stripped_strings)[0]
        date = tmp_date[3:-3]
        # 因为前两个是表头，所以从第三个获取每个省的城市的名字和气象信息
        trs = table.find_all("tr")[2:]
        for tr in trs:
            # 提取城市名称
            city = list(tr.find("td", width="83").stripped_strings)[0]
            # 提取天气现象（白天），爬取白天数据时，若当前时间为下午，则白天数据为字符“-”
            weather_condition1 = list(tr.find("td", width="89").stripped_strings)[0]
            # 提取风向（白天），同上
            wind_direction1 = list(tr.find("td", width="162").stripped_strings)[0]
            # 提取风速（白天），同上
            wind_speed1 = list(tr.find("td", width="162").stripped_strings)[1]
            # 提取城市最高温度（白天），同上
            max_tmp = list(tr.find("td", width="92").stripped_strings)[0]
            # 提取天气现象（夜间）
            weather_condition2 = list(tr.find("td", width="98").stripped_strings)[0]
            # 提取风向（夜间）
            wind_direction2 = list(tr.find("td", width="177").stripped_strings)[0]
            # 提取风速（夜间）
            wind_speed2 = list(tr.find("td", width="177").stripped_strings)[1]
            # 提取城市最低温度（夜间）
            min_tmp = list(tr.find("td", width="86").stripped_strings)[0]
            # 把城市名作为 key，上述气象数据作为 value，存入数组中
            data.append([date, city, weather_condition1, wind_direction1, wind_speed1, max_tmp, weather_condition2,
                         wind_direction2, wind_speed2, min_tmp])
    return data


# 存放数据到本地 csv 文件
def write_file(data):
    with open("../../Data.csv", "a", encoding="utf-8-sig", newline='') as fp:
        csv_writer = csv.writer(fp)
        for sub_data in data:
            csv_writer.writerow(sub_data)


if __name__ == '__main__':
    # 用来存放该地区七天的温度
    current_temperature = []
    partitions = {"hb": "华北", "db": "东北", "hd": "华东", "hz": "华中", "hn": "华南", "xb": "西北", "xn": "西南", "gat": "港澳台"}
    prefix = "http://www.weather.com.cn/textFC/"
    # 写入表头
    with open("../../Data.csv", "a", encoding="utf-8-sig", newline='') as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow(
            ['MonDay', 'Area', 'City', 'WeatherConDay', 'WindDirDay', 'WindSpdDay', 'MaxTmp', 'WeatherConNight',
             'WindDirNight', 'WindSpdNight', 'MinTmp'])
    # 遍历所有地区
    for partition in partitions:
        url = prefix + partition + ".shtml"
        # 调用 get_url 获取源码
        soup = get_url(url)
        # 调用 get_data 获取到七天天气的源码
        conmidtabs = get_data(soup)
        # 把七天的数据依次传递，获取每天的数据
        for conmidtab in conmidtabs:
            data = get_tables(conmidtab)
            # 插入地域信息
            for sub_data in data:
                sub_data.insert(1, partitions[partition])
            # 调用写入函数把 regions 里的数据写到本地
            write_file(data)
