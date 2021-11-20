# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/11/5 15:24
# @Author : yangxin0520
# @Email : yangxin0520@outlook.com
# @File : main.py
# @Software: PyCharm
import numpy as np

from module.base_tools import *
import random
import matplotlib.pyplot as plt
import math


def Init_Ci(coors, c_nums):
    """
    初始化c_i
    :param c_nums: 需要初始化c_i的个数
    :return: 聚类中心c_i的值
    """

    # random()随机取点
    c_is = [(random.random(), random.random()) for i in range(c_nums)]

    # 在离散点中随机取点
    # c_is = [coors[random.randint(0, len(coors))] for i in range(c_nums)]
    return c_is



def Calculate_Ci(coors, u_ij, c_is):
    """
    计算聚类中心c_i
    :param coors: 所有的离散点
    :param u_ij: 隶属值
    :param c_is: 旧的聚类中心c_i
    :return: 经过计算后的新的聚类中心c_i
    """
    c_inew = []  # 存储新的更新后的聚类中心c_i
    # 下面完全就是按照PPT上给的公式敲出来的
    for i in range(len(c_is)):
        x_value = 0
        y_value = 0
        sum_ = 0
        for i_i in range(len(coors)):
            sum_ += u_ij[(i_i, i)]
        for j in range(len(coors)):
            x_value += u_ij[(j, i)] * coors[j][0]
            y_value += u_ij[(j, i)] * coors[j][1]
        c_inew.append((x_value/sum_, y_value/sum_))
    return c_inew


def Calculate_Uij(coors, c_is, m_value):
    """
    计算更新隶属值u_ij的值
    :param coors: 所有离散点的坐标
    :param c_is: 聚类中心的坐标
    :param m_value: membership的值
    :return: 更新后的隶属值u_ij的值
    """
    i_value = len(c_is)  # 聚类中心的个数i
    j_value = len(coors)  # 离散点的个数j
    u_ij = np.zeros((j_value, i_value))
    # 2.2 计算分子及u_ij
    for coor in coors:
        # 2.1 计算分母
        denominator = 0  # 初始化一个分母求和变量
        for c_i in c_is:  # 对分母进行求和
            denominator_ = (
                math.pow(math.sqrt(math.pow(coor[0] - c_i[0], 2) + math.pow(coor[1] - c_i[1], 2)), 2 / (m_value
                                                                                                        - 1)))
            if denominator_ != 0:
                denominator += 1 / denominator_
            else:
                continue

        # 2.2 计算分子及u_ij
        for c_i in c_is:
            # 2.2.1 计算分子
            molecule_up = math.pow(math.sqrt(math.pow(coor[0] - c_i[0], 2) + math.pow(coor[1] - c_i[1], 2)),
                                   2 / (m_value - 1))
            if molecule_up != 0:
                molecule = 1 / molecule_up
            else:
                continue
            # 2.2.2 计算u_ij
            u_ij[(coors.index(coor), c_is.index(c_i))] = molecule / denominator
    return u_ij


def Calculate_J(coors, c_is, u_ij):
    """
    计算目标函数J(u_ij, c_i)的值
    :param coors:
    :param c_is:
    :param u_ij:
    :return:
    """
    # 给目标函数J进行赋值
    J_value = 0
    # 计算目标函数J的值
    for i in range(len(c_is)):
        for j in range(len(coors)):
            J_value += u_ij[(j, i)] * (math.pow(coors[j][0] - c_is[i][0], 2) + math.pow(coors[j][1] - c_is[i][0], 2))
    return J_value


def FCM(coors, c_nums, m_value, eps, plot_=False, save_=False, ADD=None):
    """
    FCM聚类分析算法
    :param coors: 离散点坐标
    :param c_nums: 聚类中心的个数
    :param m_value: membership values
    :return: 聚类中心的区域和聚类中心点的坐标
    """

    # 初始化c_i
    global gather_all
    c_is = Init_Ci(coors, c_nums)

    # 初始化两个J值，用于while循环前后J值作差
    J_values = 0
    J_values_next = 10000000000

    # 用于输出迭代次数
    times = 1

    # 用于保存图片的组件1
    if save_ == True:
        name_num = 0
    else:
        name_num = None

    # 迭代
    while abs(J_values_next - J_values) > eps:
        times += 1
        need_paint = []
        print("目前已经迭代了：" + str(times) + "次！")
        u_ij = Calculate_Uij(coors, c_is, m_value=m_value)

        # 用于绘图的组件1
        if plot_ == True:
            gather_all = []
            for i in range(c_nums):
                gather_all.append([])
            # init_coor = 0
            # for u_ij_max in u_ij:
            #     gather_all[np.argmax(u_ij_max)].append(coors[init_coor])
            #     init_coor += 1
        else:
            pass

        c_is = Calculate_Ci(coors, u_ij, c_is)
        J_values = J_values_next
        J_values_next = Calculate_J(coors, c_is, u_ij)
        print("当前目标函数值为：" + str(J_values_next))

        # 用于绘图的组件2
        if plot_ == True:

            plt.clf()  # 清除画布
            # FCM将点绘制
            need_paint.append(coors)  # 将所有点加入需要绘制的数据存储列表
            for i in gather_all:
                need_paint.append(i)
            need_paint.append(c_is)

            for data in need_paint:
                Paint_2dPoint([i[0] for i in data], [i[1] for i in data])
        else:
            pass

        # 用于保存图片的组件2
        if save_ == True:
            plt.savefig(ADD + "\\" + str(name_num) + '.png', bbox_inches='tight')
            name_num += 1
        else:
            pass

        plt.pause(3)
    print("迭代完成！")
    return c_is
    # for coor1 in c_is:
    #     with open('E:\\workspace\\Py\\FCM\\data\\heart_large40.csv', "a", newline='') as csvfile:
    #         writer = csv.writer((csvfile))
    #         writer.writerows([coor1])


if __name__ == "__main__":
    random.seed(12)  # 随机数种子
    ADD_CSV = 'E:\\workspace\\Py\\FCM\\data\\goudao_y_028_025.csv'  # CSV数据文件
    x_init, y_init = ReadCSV(ADD_CSV)  # 使用ReadCSV()函数获取离散点的x坐标和y坐标
    coors_init = MergeData(x_init, y_init)  # 将离散点的x坐标和y坐标合并在一起
    ci1 = FCM(coors_init, c_nums=40, m_value=1.1, eps=0.0000001, plot_=True, save_=False,
              ADD="E:\\Workspace\\Py\\FCM\\file\\goudao_seed12_15")
    # FCM(ci1, c_nums=20, m_value=1.1, eps=0.00000001, plot_=True, save_=False,
    #     ADD="E:\\workspace\\Py\\FCM\\data")
    plt.show()