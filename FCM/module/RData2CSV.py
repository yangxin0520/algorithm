# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/11/5 21:51
# @Author : yangxin0520
# @Email : yangxin0520@outlook.com
# @File : RData2CSV.py
# @Software: PyCharm
"""
本程序用于读取RData类型数据，并写入到CSV当中
"""
import pyreadr
import csv


def RData2CSV(ADD_RData, ADD_CSV):
    """
    RData2CSV()用于将RData数据转换为CSV数据
    :param ADD_RData: RData文件的地址
    :param ADD_CSV: CSV文件的地址
    :return: 无返回值
    """
    x_temp = []  # 用于读取的RData
    y_temp = []
    results = pyreadr.read_r(ADD_RData)  # 读取RData文件

    for nums in [0, 1]:  # 读取每一行的第0个、第1个数据
        # results属于OrderedDict类型，items()方法返回由键值对组会元素的列表
        for item in results.items():
            if nums == 0:
                for value_x in item[1][nums]:
                    x_temp.append(value_x)
            else:
                for value_y in item[1][nums]:
                    y_temp.append(value_y)

    # 将从RData中读到的元素存入CSV当中
    for coor in zip(x_temp, y_temp):
        with open(ADD_CSV, "a", newline='') as csvfile:
            writer = csv.writer((csvfile))
            writer.writerows([coor])


if __name__ == '__main__':
    ADD_RData = "E:\\workspace\\Py\\FCM\\data\\RData\\heart_centers.RData"
    ADD_CSV = "E:\\workspace\\Py\\FCM\\data\\test.csv"
    RData2CSV(ADD_RData, ADD_CSV)
    print("转换完成！")

