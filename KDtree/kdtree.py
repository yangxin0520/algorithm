# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/11/27 16:35
# @Author : yangxin0520
# @Email : yangxin0520@outlook.com
# @File : KD_tree.py
# @Software: PyCharm
"""
这是一个很难的程序，实现KD-tree！
构建KDtree的参考资料：https://blog.csdn.net/u012422446/article/details/56486342?spm=1001.2101.3001.6650.18&utm_medium
=distribute.pc_relevant.none-task-blog-2%7Edefault%7EOPENSEARCH%7Edefault-18.no_search_link&depth_1-utm_source=
distribute.pc_relevant.none-task-blog-2%7Edefault%7EOPENSEARCH%7Edefault-18.no_search_link
搜索KDtree的参考资料：https://zhuanlan.zhihu.com/p/23966698
"""
from math import sqrt
import random
# from random import random
import datetime


def nearest(tree, target, k):
    """
    用于K临近搜索，注意奥！是K临近！
    :param tree: 构建好的KD-tree
    :param point: 目标点
    :param k: k个距离目标点比较近的点
    :return: 距离目标点最近的k个点以及距离
    """
    Results = []  # 用于储存k个点坐标以及距离

    def distance(node_, _target):  # node_是当前节点，p是目标节点
        if len(Results) < k:  # 判断存储列表中的元素个数是否小于设定值K
            d = sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(node_, _target)))  # 这个写法秒啊！
            Results.append([node_, d])  # 若存储列表中的元素不足K个，那么就把这个结点append进去
            return None
        else:  # 如果存储列表中的元素大于等于k个
            d = sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(node_, _target)))  # 计算当前结点与目标点的距离
            Results.sort(key=lambda a: a[1])  # 使用lambda函数对某一特定列的元素进行排序
            if (Results[-1][1] > d):  # 如果存储列表中距离最大的元素比当前节点的距离要大
                Results.pop()  # 那么把栈顶元素删除掉
                Results.append([node_, d])  # 把当前结点和距离存储进存储列表当中
            return None

    def traversal(kd_node):
        """
        递归函数
        :param kd_node: 已经构建好的kd树
        :return:
        """
        if kd_node is None:
            return None

        s = kd_node.split  # 获取当前的分割超平面的维度
        if kd_node.node[s] > target[s]:  # 如果在当前维度下，目标点的值小于节点值
            closer_node = kd_node.left_child  # 那么最近点在左子树
            futher_node = kd_node.right_child  # 较远的点在右子树
        else:  # 反之
            closer_node = kd_node.right_child  # 最近点在右子树
            futher_node = kd_node.left_child  # 最近点在左子树
        traversal(closer_node)  # 从这一步就是开始迭代
        distance(kd_node.node, target)  # 调用distance函数
        dis1 = abs(kd_node.node[s] - target[s])  # 计算目标点到切割超平面的距离dis1
        dis2 = sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(kd_node.node, target)))  # 最长距离
        if len(Results) < k or dis1 < dis2:  # 如果目标点到分割线的距离小于目标点到当前节点的距离
            traversal(futher_node)  # 那么，在分割线的另一端可能存在有更近的点，去那边看看
        else:
            return None

    traversal(tree.root)  # 从最最最最最最根节点开始
    return Results

from math import sqrt
from collections import namedtuple

# 定义一个namedtuple,分别存放最近坐标点、最近距离
result = namedtuple("Result_tuple", "nearest_point  nearest_dist")


def find_nearest(tree, point):
    k = len(point)  # 数据维度

    def travel(kd_node, target, _dis):
        if kd_node is None:
            return result([0] * k, float("inf"))  # python中用float("inf")和float("-inf")表示正负无穷

        s = kd_node.split  # 进行分割的维度
        pivot = kd_node.node  # 进行分割的“轴”

        if target[s] <= pivot[s]:  # 如果目标点第s维小于分割轴的对应值(目标离左子树更近)
            nearer_node = kd_node.left_child  # 下一个访问节点为左子树根节点
            further_node = kd_node.right_child  # 同时记录下右子树
        else:  # 目标离右子树更近
            nearer_node = kd_node.right_child  # 下一个访问节点为右子树根节点
            further_node = kd_node.left_child

        temp1 = travel(nearer_node, target, _dis)  # 进行遍历找到包含目标点的区域

        nearest = temp1.nearest_point  # 以此叶结点作为“当前最近点”
        dist = temp1.nearest_dist  # 更新最近距离


        if dist < _dis:
            max_dist = dist  # 最近点将在以目标点为球心，max_dist为半径的超球体内

        temp_dist = abs(pivot[s] - target[s])  # 第s维上目标点与分割超平面的距离
        if _dis < temp_dist:  # 判断超球体是否与超平面相交
            return result(nearest, dist)  # 不相交则可以直接返回，不用继续判断

        # ----------------------------------------------------------------------
        # 计算目标点与分割点的欧氏距离
        temp_dist = sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(pivot, target)))

        if temp_dist < dist:  # 如果“更近”
            nearest = pivot  # 更新最近点
            dist = temp_dist  # 更新最近距离
            max_dist = dist  # 更新超球体半径

        # 检查另一个子结点对应的区域是否有更近的点
        temp2 = travel(further_node, target, _dis)

        if temp2.nearest_dist < dist:  # 如果另一个子结点内存在更近距离
            nearest = temp2.nearest_point  # 更新最近点
            dist = temp2.nearest_dist  # 更新最近距离

        return result(nearest, dist)

    return travel(tree.root, point, float("inf"))  # 从根节点开始递归


# 下面的程序用于构建KD树
class Node(object):
    def __init__(self, node, split, left_child, right_child):
        self.node = node
        self.split = split
        self.left_child = left_child
        self.right_child = right_child


class CreateTree(object):
    def __init__(self, data):
        # 获取传入数据的维度
        k = len(data[0])
        def createNode(split, dataset):
            """
            作用：
                1.分割数据集
                2.获取节点
                3.更新分割轴
            :param split: 分割维度
            :param dataset: 待分割的数据集
            :return: 节点
            """
            # 判断数据集是否为空
            if not dataset:
                return None
            # 1.分割数据集
            dataset.sort(key=lambda x: x[split])  # 对数据集按照分割维度进行排序(1.lambda匿名函数的使用；2.list.sort(key=)的使用)
            length = len(dataset)  # 获取数据集dataset的长度
            # 1.1获取中位数坐标的位置
            if length % 2 == 0:  # 那么这个列表有偶数个元素
                median_site = (length//2) - 1
            else:  # 否则这个列表有奇数个元素
                median_site = length//2
            # 1.2 中位数的坐标
            median = dataset[median_site]
            # 1.2 将下一次的分割维度+1
            split_next = (split + 1) % k
            # 2. 铛铛铛！重点来了！使用递归创建一棵kd树
            return Node(median, split,
                              createNode(split_next, dataset[:median_site]),
                              createNode(split_next, dataset[median_site + 1:]))
        self.root = createNode(0, data)

def preorder(root):
    print(root.node)
    if root.left_child:  # 节点不为空
        preorder(root.left_child)
    if root.right_child:
        preorder(root.right_child)


def Random_points(k, N):
    """
    随机构建N个K维度的点
    :param k: 维度
    :param N: 需要构建的点个数
    :return: 列表
    """
    def random_points(k):
        return [random.random() for i in range(k)]
    demo = [random_points(k) for i in range(N)]
    return demo


def ordinary_dis(data, point) -> object:
    """
    计算最小距离常规算法
    :param data:
    :param point:
    :return:
    """
    L = []
    for i in data:
        d = sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(i, point)))
        L.append([i, d])
    L.sort(key=lambda x: x[1])
    return L[0]


if __name__ == '__main__':  # 用于验证程序是否能够正常走通
    # 准备实验数据
    random.seed(10)
    data = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
    k = 3
    N = 25388  # 一千万个点
    NN = 25388
    ret_ = []
    ordinary_ = []
    start_produce_data = datetime.datetime.now()
    demo_data = Random_points(k, N)
    target_data = Random_points(k, NN)
    end_produce_data = datetime.datetime.now()
    print("随机产生" + str(N) + "个点耗时：" + str(((end_produce_data - start_produce_data) * 1000).seconds) + "毫秒！")
    # 根据CreateTree类创建一个对象kd
    start_createtree = datetime.datetime.now()
    kd = CreateTree(demo_data)
    end_createtree = datetime.datetime.now()
    print("构建KDtree耗时：" + str(((end_createtree - start_createtree) * 1000).seconds) + "毫秒！")
    start_nearest = datetime.datetime.now()
    for i in target_data:
        # ret = nearest(kd, i, 1)
        ret = find_nearest(kd, i)
        ret_.append(ret)
    end_nearest = datetime.datetime.now()
    print("搜索KDtree耗时：" + str(((end_nearest - start_nearest)*1000).seconds) + "毫秒！")
    print(ret_[0])
    start_ordinary = datetime.datetime.now()
    for i in target_data:
        ordinary_dis_ = ordinary_dis(demo_data, i)
        ordinary_.append(ordinary_dis_)
    end_ordinary = datetime.datetime.now()
    print("暴力遍历耗时：" + str(((end_ordinary - start_ordinary) * 1000).seconds) + "毫秒！")
    print(ordinary_)