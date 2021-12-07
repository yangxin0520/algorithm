# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/6 17:30
# @Author : yangxin0520
# @Email : yangxin0520@outlook.com
# @File : KDtree.py
# @Software: PyCharm
"""
实现KDtree
本程序由三大部分构成：
                1 构建KDtree部分
                2 搜索KDtree部分
                3 辅助验证部分
这里实现的暂时是最临近，K临近还没有实现！
"""
import numpy as np
import time
import random
import datetime
from math import sqrt
from collections import namedtuple


# 1 构建KDtree
# 1.1 定义KDtree结点属性
class Node:
    def __init__(self, node, split, left_child, right_child):
        self.node = node  # 定义根节点
        self.split = split  # 定义分割超平面维度
        self.left_child = left_child  # 定义左子树
        self.right_child = right_child  # 定义右子树


# 1.2 构造KDtree
class CreateTree:
    def __init__(self, data):
        k = len(data[0])  # 获取传入数据的维度

        def createnode(split, dataset):
            """
            构建KDtree
            :param split: 分割超平面的维度
            :param data: 用于构建KDtree的数据集
            :return: tree
            """
            if not dataset:  # 判断数据集是否为空（递归的边界）
                return None

            # 分割数据集
            dataset.sort(key=lambda x: x[split])  # 按照分割维度对数据集进行排序
            length = len(dataset)  # 获取数据集dataset的长度
            if length % 2 == 0:  # 那么这个列表有偶数个元素
                median_site = (length // 2) - 1
            else:  # 否则这个列表有奇数个元素
                median_site = length // 2
            median = dataset[median_site]  # 中位数坐标
            split_next = (split + 1) % k  # 更新下一次的分割维度

            # 重点来了，递归的关键组件
            return Node(median, split,
                        createnode(split_next, dataset[:median_site]),
                        createnode(split_next, dataset[median_site + 1:]))

        self.root = createnode(0, data)


# 2 搜索KDtree部分
# 首先，定义一个nametuple，分别存储最近点坐标和最近距离
Nearest_result = namedtuple("Nearest_rstult", "nearest_point nearest_dis")
# 下面构建搜索函数
def Nearest(kdtree, target, k):
    """
    搜索函数
    :param tree: 前面构建好的tree
    :param target: 目标点
    :param k: k个最临近点
    :return: 最近点
    """
    Result = []  # 用于存储k
    dimension = len(target)  # 数据的维度

    # def distance(_node, target):
    #     """
    #     计算距离函数，尝试获取K临近
    #     :param _node: 节点
    #     :param target: 目标点
    #     :return: 返回什么我还没想好
    #     """
    #     if len(Result) < k:  # 判断当前存储列表中的元素个数是否小于设定值k
    #         pass




    def traversal(tree, target, _dis):
        """
        搜索函数的递归比分
        :param tree: 构建好的KDtree
        :param target: 目标点
        :param max_dis: 最大距离
        :return: ~
        """
        if tree is None:  # 如果tree是空的，那么就返回~
            return Nearest_result([0] * dimension, float("inf"))

        # 如果tree不是空的，那么就执行下面的程序
        split_d = tree.split  # 获取当前分割的维度
        split_axis = tree.node  # 获取当前分割的“轴”
        # 判断target点在左右哪个子树当中，这里也是递归的重点
        if target[split_d] <= split_axis[split_d]:  # 如果在当前分割维度下，目标点的值小于等于轴的值
            closer_node = tree.left_child  # 那么更近的点大概率在左子树
            futher_node = tree.right_child  # 也不排除在右子树的可能，右子树也记录一下
        else:  # 反之
            closer_node = tree.right_child
            futher_node = tree.left_child

        # 下面进行递归
        # 1. 首先计算与叶节点的距离
        trav_node1 = traversal(closer_node, target, _dis)  # 能一直递归到叶节点，trav_node1就是叶点
        nearest = trav_node1.nearest_point  # 暂时以叶点为“当前最近点”
        dis = trav_node1.nearest_dis  # 获取目标点到“当前最近点”的距离

        # 试验：
        # if nearest not in [i[0] for i in Result]:
        #     if len(Result) < k:
        #         Result.append([nearest, dis])
        #     else:
        #         Result.sort(key=lambda x: x[1])
        #         Result.pop()
        #         Result.append([nearest, dis])



        if len(Result) < k and nearest not in [i[0] for i in Result]:
            Result.append([nearest, dis])
        else:
            Result.sort(key=lambda x: x[1])
            if Result[-1][1] > dis and nearest not in [i[0] for i in Result]:
                Result.pop()
                Result.append([nearest, dis])

        # 判断当前叶点距离与超球体半径的大小关系
        if dis < _dis:  # 若小于
            _dis = dis  # 更新超球体半径

        # 2.计算到分割超平面的距离
        axis_dis = abs(split_axis[split_d] - target[split_d])  # 计算到分割超平面的距离
        if _dis < axis_dis:  # 如果“当前最近点”形成的超球体与超平面不相交
            return Nearest_result(nearest, dis)  # 那么“当前最近点”就是实际最近点了，可以直接返回

        # 3.计算目标点到分割点的距离
        point_dist = sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(split_axis, target)))

        if point_dist < _dis:  # 如果“更近”
            nearest = split_axis  # 更新最近点
            dis = point_dist  # 更新最近距离
            _dis = dis  # 更新超球体半径
            if len(Result) < k and nearest not in [i[0] for i in Result]:
                Result.append([nearest, dis])
            else:
                Result.sort(key=lambda x: x[1])
                if Result[-1][1] > dis and nearest not in [i[0] for i in Result]:
                    Result.pop()
                    Result.append([nearest, dis])

        # 4.检查另一个分支内是否存在更近的点
        trav_node2 = traversal(futher_node, target, _dis)  # 能一直递归到叶节点，trav_node2就是叶点

        if trav_node2.nearest_dis < _dis:  # 如果另一个叶点的距离更小
            nearest = trav_node2.nearest_point  # 更新最近点
            dis = trav_node2.nearest_dis  # 更新最近距离

            #  试验：
            if len(Result) < k and nearest not in [i[0] for i in Result]:
                Result.append([nearest, dis])
            else:
                Result.sort(key=lambda x: x[1])
                if Result[-1][1] > dis and nearest not in [i[0] for i in Result]:
                    Result.pop()
                    Result.append([nearest, dis])

        return Nearest_result(nearest, dis)  # 这样就全部计算完了，可以返回值了

    _dis = float("inf")  # float("inf")的意思是无穷大，主要用在<和>比较当中，所有的数都比无穷大要小
    return traversal(kdtree.root, target, _dis)  # 从根节点开始递归，_dis为随机初始化的超球体的半径，这里赋值无穷大


# 3.辅助验证部分





if __name__ == "__main__":
    data = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2], [8, 5], [4, 4], [6, 7], [1, 9]]
    kd = CreateTree(data)
    # print(kd.root)
    ret = Nearest(kd, (6, 5), 3)
    print(ret)
