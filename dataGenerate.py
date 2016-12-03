# -*- coding: utf-8 -*-
import requests
import time
import datetime
import sys
import os
import csv
import re
import Params


def get_path():
    if sys.path[0]:
        return sys.path[0] + '/'
    else:
        return sys.path[0]


def get_wx(payload):
    url = '' # data source
    r = requests.get(url, params=payload)
    csv_url = r.text[3:]
    csv_url = csv_url.replace('', '')
    if not re.match(r'', csv_url):
        print("Error receiving csv_url")
        return

    for i in range(100):
        try:
            time.sleep(30)
            res = requests.get(csv_url)
            if res.status_code == 200:
                data = [row.split('\t') for row in res.content.decode('utf-8').split('\n')[1:]]
                if data:
                    return data
            print("Try time %d status_code: %d!" % (i, res.status_code))
        except requests.ConnectionError:
            pass
    print("Time out!")
    return


def read_file(file_path):
    data = list()
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return data


class DataGenerate:
    def __init__(self, lag_int=1, download=True, writeln=True):
        self.download = download
        self.writeln = writeln
        self.lag_int = lag_int
        self.end_date = datetime.datetime.now() + datetime.timedelta(-self.lag_int)
        self.date_thred = (datetime.datetime.now() + datetime.timedelta(
            days=-self.lag_int + Params.DATA_SOURCE_DAYGAP)).strftime("%Y%m%d")
        self.ad_text = dict()
        self.user_ad = dict()
        self.__generate()

    def __generate(self):
        if self.download:
            for fileInfo in Params.FILEINFO.keys():
                self.start_date = datetime.datetime.now() + \
                                  datetime.timedelta(Params.OPTSTART[fileInfo] + 1 - self.lag_int)
                if fileInfo in {"TEXT", "OTHER"}:
                    start_date, end_date = self.start_date.strftime("%Y-%m-%d"), \
                                                     self.end_date.strftime("%Y-%m-%d")
                elif fileInfo in {"VIEW"}:
                    start_date, end_date = self.start_date.strftime("%Y%m%d"), \
                                           self.end_date.strftime("%Y%m%d")
                else:
                    return

                payload = {''}  #according API
                data = get_wx(payload)
                if fileInfo == "VIEW":
                    data = data[1:]

                if self.writeln:
                    file_path = get_path() + Params.FILEINFO[fileInfo]["file"]
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    with open(file_path, 'w+') as f:
                        csv_writer = csv.writer(f, delimiter=',')
                        if data:
                            for row in data:
                                csv_writer.writerow(row)
                        else:
                            print("No Writing! Data is empty!")

                if len(data) <= 0:
                    continue

                if data:
                    self.__data_load(fileInfo, data)

        else:
            for fileInfo in Params.FILEINFO.keys():
                file_path = get_path() + Params.FILEINFO[fileInfo]["file"]
                data = read_file(file_path)
                if data:
                    self.__data_load(fileInfo, data)

    def __data_load(self, file_info, data):
        if file_info == "TEXT":
            for row in data:
                if len(row) > 1:
                    self.ad_text.setdefault(row[0], (str(row[1]), str(row[2])))
                    self.ad_text[row[0]] = (str(row[1]), str(row[2]))
        if file_info in {"VIEW", "OTHER"}:
            self.user_ad[file_info] = dict()
            for row in data:
                if len(row) < 2:
                    continue
                self.user_ad[file_info].setdefault(row[1], [])
                self.user_ad[file_info][row[1]].append(row[0])
















