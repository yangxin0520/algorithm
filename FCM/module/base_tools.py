# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/11/8 9:46
# @Author : yangxin0520
# @Email : yangxin0520@outlook.com
# @File : base_tools.py
# @Software: PyCharm
"""
基础公用函数，防止重复造轮子
"""
import csv
import matplotlib.pyplot as plt


def ReadCSV(ADD_CSV):
    """
    用于读取CSV，分别返回两个坐标的列表
    :param ADD_CSV: CSV文件地址
    :return: 分别存储x和y的数值列表
    """
    x_temp = []  # 创建临时列表用于存储x坐标的数值
    y_temp = []

    with open(ADD_CSV) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            x_temp.append(float(row[0]))

    with open(ADD_CSV) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            y_temp.append(float(row[1]))

    return x_temp, y_temp


def initial2(x, c, alpha, xlim, ylim):
    """
    计算聚类中心并进行曲线初始化
    :param x: 数据集
    :param c: 聚类点的个数
    :param alpha: 正则化参数
    :param xlim: 使用(x1,x2)限制x轴
    :param ylim: 使用(y1,y2)限制x轴
    :return: 两个元素的列表：1.平滑前的聚类中心；2.平滑后的聚类中心
    """
    pass


def MergeData(x_, y_):
    """
    合并x坐标值和y坐标值为(x, y)
    :param x_: x坐标
    :param y_: y坐标
    :return: (x, y)格式的返回值
    """
    coors = []
    for coor in zip(x_, y_):
        coors.append(coor)

    return coors


def Paint_2dPoint(projection_a, projection_b):
    """
    绘制离散点图，可以同时绘制多组坐标数据，第一个参数是x坐标的列表集合，第二个坐标是y坐标的列表集合，第三个参数是颜色集合，全部都是用[]
    :param projection_a: x坐标列表集合
    :param projection_b: y坐标列表集合
    :return: 绘制的图像
    """
    plt.scatter(projection_a, projection_b)
