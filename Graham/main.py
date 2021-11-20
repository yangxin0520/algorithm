# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time: 2021/9/14 21:01
# @Author: yangxin0520
# @File: slice.py
# @Software: Pycharm
import csv

import matplotlib.pyplot as plt
import math
import open3d as o3d
import numpy as np


def Load_Data(path):
    """
    加载点云数据
    :param path: 点云模型的绝对地址
    :return: 读取的点云模型
    """
    # init_model = o3d.io.read_point_cloud(path, format="txt")  # 读取txt格式的点云模型
    init_model = o3d.io.read_point_cloud(path)  # 读取ply格式的点云模型
    print(init_model)
    return init_model  # 返回一个初始模型数据


def Decide_Color(init_model):
    """
    给点云模型上色，当输入多个点云模型时，给不同的点云上不同的颜色，便于区分点云模型
    :param init_model: 读取的初始模型
    :return: 上了固定颜色的点云模型
    """
    init_model.paint_nuniform_color([1, 0.706, 0])  # 给模型上一个[1, 0.706, 0]的颜色
    return init_model  # 返回一个上了颜色的点云模型


def O3d_to_Np(init_model):
    """
    将Open3D.o3d.geometry.PointCloud数据转化为numpy数据
    :param init_model: 读取的点云模型
    :return: np数据
    """
    np_model_data = np.asarray(init_model.points)  # 将Open3d.o3d.geometry.PointCloud数据转化为numpy数据
    return np_model_data  # 返回numpy数据


def Np_to_List(np_model_data):
    """
    将numpy类型转化为list类型，方便读取
    :param np_model_data: 点云模型数据的numpy型
    :return: 点云模型数据的list型
    """
    list_model_data = np_model_data.tolist()  # 将numpy数据转化为list数据
    return list_model_data  # 返回list数据


def Cut_Model(list_model_data, axis):
    """
    切割模型
    :param list_model_data: 点云模型的list形式
    :return: 切片后的点云合集
    """
    # 将xyz坐标值取出，放入单独的集合当中
    coor_x = []
    coor_y = []
    coor_z = []
    projection_a = []
    projection_b = []
    for i in list_model_data:  # 遍历出来的i是[x, y, z]的形式
        coor_x.append(i[0])  # 取x的坐标值放入x的列表中
        coor_y.append(i[1])  # 取y的坐标值放入y的列表中
        coor_z.append(i[2])  # 取z的坐标值放入z的列表中

    # 进行切割，并将切割后的Point的坐标分别写入list当中
    slice_coor_x = []  # 切割后的Point的x坐标值列表
    slice_coor_y = []  # 切割后的Point的y坐标值列表
    slice_coor_z = []  # 切割后的Point的z坐标值列表
    if axis == 'x':  # 如果投影轴为x
        for i in coor_x:
            if i >= 0.185 and i < 0.185:  # 这里要重写，目前是验证阶段，只有一个断面
                index_x = coor_x.index(i)
                slice_coor_y.append(coor_y[index_x])
                slice_coor_z.append(coor_z[index_x])
                projection_a = slice_coor_y
                projection_b = slice_coor_z
    elif axis == 'y':  # 如果投影轴为y
        for i in  coor_y:
            if i >= -0.27 and i < -0.25:  # 左边取等号，这里要重写，目前是验证阶段，只有一个断面
                index_y = coor_y.index(i)  # 得到数值为i的索引值index
                slice_coor_x.append(coor_x[index_y])  # 向x坐标值列表中append索引值为index的值
                slice_coor_z.append(coor_z[index_y])  # 向y坐标值列表中append索引值为index的值
                projection_a = slice_coor_x
                projection_b = slice_coor_z
    else:  # 既不是x也不是y，那就是z咯
        for i in coor_z:
            if i >= -10 and i < 10: # 这里要重写，目前是验证阶段，只有一个断面
                index_z = coor_z.index(i)
                slice_coor_x.append(coor_x[index_z])
                slice_coor_y.append(coor_y[index_z])
                projection_a = slice_coor_x
                projection_b = slice_coor_y
    for coors in zip(projection_a, projection_b):
        with open('E:\\workspace\\Py\\FCM\\data\\goudao_y_028_025.csv', 'a', newline='') as csvfile:
            witer = csv.writer((csvfile))
            witer.writerows([coors])
    return projection_a, projection_b



def Paint_2dPoint(projection_a, projection_b, name):
    """
    绘制切割后的点云图，即进行可视化
    :param projection_a: 第一个坐标值
    :param projection_b: 第二个坐标值
    :return: 可视化
    """
    plt.figure()  # 创建一个窗口
    plt.title(name)  # 将其命名为slice
    plt.scatter(projection_a, projection_b)  # 将二维坐标输入进去
    plt.show()  #运行可视化


def Merge_Data(projection_a, projection_b):
    """
    存储单圈点云数据，将分开的x坐标值和y坐标值成对放入[x, y]中
    :param projection_a: 第一个坐标
    :param projection_b: 第二个坐标
    :return: 返回[x, y]数据
    """
    one_circle_data = [
        [0, 0]  # 防止后面找不到矩阵的维数产生报错，首先初始化一个1*2的矩阵
    ]
    for i in range(len(projection_a)):  # 向矩阵中添加[x, y]
        one_circle_data = np.append(one_circle_data, [[projection_a[i], projection_b[i]]], axis=0)
    one_circle_data = np.delete(one_circle_data, 0, 0)  # 删除初始化矩阵时加入的[0, 0]
    return one_circle_data  # 返回[x, y]数据


def Calculate_Averagedistance(one_circle_data):
    """
    根据点的坐标计算每个Point和最近两点之间的距离，然后求得临近两个Point的距离的平均数
    :param one_circle_data: 所有Point的坐标
    :return: 临近两点距离的平均数
    """
    distance = []  # 初始化一个距离空列表，用于存储每一个点与最近两个点之间的距离
    for i in range(len(one_circle_data)):  # 第一次循环：找到每一个点
        temp_distance_all = []  # 初始化一个距离空列表，用于存储第i个点与其余所有的点的距离
        for n in range(len(one_circle_data)):  # 第二次循环，计算第i个点与其他所有点的距离，并存储到temp_distance_all里
            temp_distance_one = math.sqrt(pow((one_circle_data[i][0] - one_circle_data[n][0]), 2) + pow(
                (one_circle_data[i][1] - one_circle_data[n][0]), 2))  # 计算两点之间的距离
            temp_distance_all.append(temp_distance_one)  # 将计算到的距离存入到列表里
        temp_distance_all.sort()  # sort()对列表进行排序
        distance.append(temp_distance_all[0])  # 将最小的距离加入到distance中
        distance.append(temp_distance_all[1])  # 将第二小的距离加入到distance中
    sum_distance = 0  # 初始化总距离变量
    for i in distance:  # 循环获取距离值
        sum_distance = sum_distance + i  # 将距离值进行累加
    average_disatance = sum_distance / len(distance)  # 计算平均距离值
    return average_disatance


def Sort_cosangle(points, center_coor):
    """
    对所有的点进行cos角排序
    :param points: 所有的点
    :param A_coor: cos角排序的中心点
    :return: 按cos角排序后的points坐标
    """
    index = points.index(center_coor)  # 获取目标中心点的索引
    points.pop(index)  # 根据获取到的中心点的索引，将其从list中pop掉
    n = len(points)  # 获取list的长度
    cos_value = []  # 存储每个点与中心点构成向量的cos值
    seq = []  # 记录点的顺序
    line_distance = []  # 继续中心点与目标点的直线距离

    # 下面进行cos值计算
    for i in range(0, n):  # 计算除中心点外，所有的点与中心点构成向量的cos值
        seq.append(i)  # 记录点的seq(顺序)
        aim_point = points[i]  # 得到目标点的坐标
        line_distance_value = math.sqrt(pow(aim_point[0] - center_coor[0], 2) + pow(aim_point[1] - center_coor[1], 2))  # 计算中心点与目标点的直线距离
        line_distance.append(line_distance_value)  # 将直线距离append进列表中储存
        # 下面开始计算cos值
        if line_distance_value == 0:  # 如果目标点与中心点的距离为零，那么cos值极为1
            cos_value.append(1)
        else:  # 如果目标点与中心点的距离不为零，那么利用公式 cosA = x / r，计算cos值
            cos_value.append((aim_point[0] - center_coor[0]) / line_distance_value)

    # 下面进行cos值排序
    for i in range(0, n - 1):  # 判断所有的点
        index_value = i + 1
        '''
            难点！下面个while循环的作用是判断两个cos值的大小，并进行排序
            具体逻辑思路如下：
            1.首先拿到索引index_value
            2.判断索引的cos值与索引前一个cos值的大小，假如这两个cos值大小相等了，则继续判断他们的line_distance,如果后一个大于前一个，则保存，否则break
            3.满足上述条件后，将索引值与索引值前一个的值的位置进行对调，利用"a->b" "b->c" "c->a"的方法，完成a与c的值的互换。
            4.索引对调后，index_value向前一位，利用while循环回到第二步，继续判断，直至判断完全
        '''
        while index_value > 0:
            if cos_value[index_value] > cos_value[index_value - 1] or (cos_value[index_value] == cos_value[index_value - 1] and line_distance[index_value] > line_distance[index_value - 1]):
                temp = cos_value[index_value]
                temp_seq = seq[index_value]
                temp_line_distance = line_distance[index_value]
                cos_value[index_value] = cos_value[index_value - 1]
                seq[index_value] = seq[index_value - 1]
                line_distance[index_value] = line_distance[index_value - 1]
                cos_value[index_value - 1] = temp
                seq[index_value - 1] = temp_seq
                line_distance[index_value - 1] = temp_line_distance
                index_value = index_value - 1
            else:
                break
    sorted_points = []  # 排好序的points
    for i in seq:  # 便利seq里面的顺序值
        sorted_points.append(points[i])  # 按照seq列表提供的顺序值将points append进sorted_points中
    return sorted_points




def Graham_scan(points, center_coor):
    """
    Graham扫描法计算凸包
    分两个步骤进行：
    1.进行角排序(以角度大小进行排序)
    2.进栈 叉积
    :param points: Points数据
    :return:
    """
    # 1.进行角排序
    sorted_points = Sort_cosangle(points, center_coor)  # 进行角排序
    number_points = len(sorted_points)  # 获取排序后的点的个数
    if number_points < 2:
        print("point的数量不足以构成凸包，无法进行Graham计算")
    stack = []  # 初始化一个空栈(栈)
    """
    栈的操作思路：
    对栈顶两元素向量判断下一个元素是否在左边
    如果在左边，下一个元素进栈
    如果不在左边，则栈顶元素出栈
    若栈内元素不足两个，则下一元素直接入栈
    """
    stack.append(center_coor)  # 首先将中心点append进栈
    stack.append(sorted_points[0])  # 再将排序好的point中的第一个点也放进栈中，与中心点可以构成第一条边，开始找边界
    stack.append(sorted_points[1])
    # 2.开始找边界（重点！难点！大难点！深刻理解！）
    for i in range(2, number_points):  # 从1开始，是因为0已经被append到栈中了
        length = len(stack)  # 获取当前栈的长度，要记住栈的特性是先进后出
        top = stack[length - 1]  # 这里length减1 是因为栈底是0，往上就是0,1,2,3···，假如长度是2的话，那么栈顶的索引就是1，所以这里要减1
        under_top = stack[length - 2]  # under_top指的是栈顶下面的那个元素
        """
        下面开始计算向量外积
        1.假设under_top的元素是O，栈顶top元素是A，目标点的元素是B
        2.求得OB和OA的向量V1(x1,y1)和V2(x2,y2)
        3.计算向量外积（叉乘），即x1*y2-x2*y1
        4.如果叉积,小于0，则说明目标点在under_top和top组成的向量OA的左边，即可之间入栈
        5.如果叉积大于等于0，则说明目标点在under_top和top组成的向量OA的右边，那么就要把栈顶元素pop出去
        6.假如发生了第五步，那么使用while循环一直判断，直至under_top与目标点组成的向量OB左侧没有点之后结束，然后将目标点入栈
        """
        v1 = [top[0] - under_top[0], top[1] - under_top[1]]  # top元素与under_top元素组成的向量v1
        v2 = [sorted_points[i][0] - under_top[0], sorted_points[i][1] - under_top[1]]  # under_top与目标点组成的向量v2

        while (v1[0]*v2[1] - v2[0]*v1[1]) >= 0:  # 如果外积满足小于0，那么说明目标点在向量的右边
            """
            深刻理解两条：
            1.若目标点B在向量OA()的左边，那么向量OA叉乘向量OB为正
            2.若目标点B在向量OA()的右边，那么向量OA
            """
            stack.pop()  # 目标点在向量的右边，则需要把栈顶的元素pop出去
            length = len(stack)  # 把栈顶元素pop出去之后重新计算栈的长度
            #  下面重新获取栈顶元素和under_top元素,得到新的向量v1和v2，继续while循环，直至under_top与目标点组成的向量OB左侧没有点之后结束，然后将目标点入栈，成为top点
            top = stack[length - 1]
            under_top = stack[length - 2]
            v1 = [top[0] - under_top[0], top[1] - under_top[1]]  # top元素与under_top元素组成的向量v2
            v2 = [sorted_points[i][0] - under_top[0], sorted_points[i][1] - under_top[1]]  # under_top与目标点组成的向量v1
        stack.append(sorted_points[i])  # 将目标点append进栈
    print(len(stack))
    return stack


def Find_border(one_circle_data, projection_a, projection_b):
    """
    找边界的主要思路：
    1.找到离散点中，保证y坐标最大的情况下，x坐标最小的点，记做A点
    2.以A点为原点，x轴正反向射线顺时针扫描，找到旋转角最小时扫描到的点，记做B点
    3.以B点为原点，AB方向射线顺时针扫描，找到旋转角最小时扫描到的点，记做C点
    4.以C点为原点，BC方向射线顺时针扫描，找到旋转角最小时扫描到的点，记做D点
    5.以此类推，直到找到起始点A
    :param projection_a:
    :param projection_b:
    :return:
    """
    center_coor = [projection_a[projection_b.index(max(projection_b))], max(projection_b)]  # 获取初始点A点坐标
    Paint_2dPoint(projection_a, projection_b, name="one_slice")  # 绘制Point图
    for point in one_circle_data:
        plt.scatter(point[0], point[1], marker='o', c='y')
    result = Graham_scan(one_circle_data.tolist(), center_coor)
    length = len(result)
    for i in range(0, length - 1):
        plt.plot([result[i][0], result[i + 1][0]], [result[i][1], result[i + 1][1]], c='r')
    plt.plot([result[0][0], result[length - 1][0]], [result[0][1], result[length - 1][1]], c='r')
    plt.show()


def Point_number(one_circle_data, center_coor):
    temp_index = 0
    for point in one_circle_data:
        plt.scatter(point[0], point[1], marker='o', c='y')
        plt.scatter(center_coor[0], center_coor[1], marker='v', c='r')
        index_str = str(temp_index)
        plt.annotate(index_str, (point[0], point[1]))
        temp_index = temp_index + 1
    plt.show()

if __name__ == "__main__":
    init_model = Load_Data(".\\data\\A8.ply")  # 读取数据
    np_model_data = O3d_to_Np(init_model)  # 数据转化为np型
    list_model_data = Np_to_List(np_model_data)  # 数据转化为list型
    projection_a, projection_b = Cut_Model(list_model_data, 'y')  # 进行裁剪
    one_circle_data = Merge_Data(projection_a, projection_b)  # 合并数据
    average_distance = Calculate_Averagedistance(one_circle_data)  # 计算平均距离
    Find_border(one_circle_data, projection_a, projection_b)  # 寻找边界