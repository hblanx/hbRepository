# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 17:06:47 2021
@author: hblanx
"""
'''
Node类为节点
'''
class Node:
    def __init__(self, x, y, deep, childNum):
        self.x = x
        self.y = y
        self.deep = deep
        self.childNum = childNum
        self.left = False
        self.right = False


'''
Tree类为kd树
sortX(),sortY()方法分别对包含xy轴数据的列表进行x排序和y排序
create()方法，使用包含[x,y]坐标数据的列表创建kd树，此方法为接口
createNode()方法，生成节点
knn()方法，进行k的邻近搜索，此方法为接口
search()方法，根据条件遍历子树
compare()方法，比较距离
add()方法，增加节点，注意，此方法会导致熵减速度下降！此方法为接口
rebuild()方法，在增加节点时重建含有一个子节点的分支节点
addNode()方法，递归增加节点
remove()方法，删除节点，注意，此方法会导致熵减速度下降！此方法为接口
removeNode()方法，实现删除功能
searchRemoveNode()方法，寻找需要删除的节点
'''
class Tree:
    def __init__(self):
        self.data = []
        self.head = False
        self.far = 999

    def sortX(self, inputList):
        return inputList[0]

    def sortY(self, inputList):
        return inputList[1]

    '''
    create方法，使用Tree类的data成员变量构造树
    生成成员变量head 无返回值
    '''
    def create(self):
        self.head = self.createNode(self.data, 1)

    def createNode(self, data, deep):
        if len(data) >= 3:  # 有两个子节点
            mid = len(data) // 2  # 如遇偶数，选较小的那个为当前节点
            if deep % 2 == 1:  # 奇数层对X进行排序
                data.sort(key=self.sortX)
            else:  # 偶数层对Y进行排序
                data.sort(key=self.sortY)
            x = data[mid][0]
            y = data[mid][1]
            leftList = data[0:mid]
            rightList = data[mid + 1:]

            node = Node(x, y, deep, 2)
            node.left = self.createNode(leftList, deep + 1)
            node.right = self.createNode(rightList, deep + 1)




        elif len(data) == 2:  # 只有一个子节点
            if deep % 2 == 1:  # 奇数层对X进行排序
                data.sort(key=self.sortX)
            else:  # 偶数层对Y进行排序
                data.sort(key=self.sortY)
            x = data[1][0]  # 将小的放子节点里
            y = data[1][1]
            smallData = [data[0]]

            node = Node(x, y, deep, 1)
            node.left = self.createNode(smallData, deep + 1)


        else:  # 此节点就是叶子节点
            x = data[0][0]
            y = data[0][1]

            node = Node(x, y, deep, 0)

        return node

    def rebuild(self, node, aimX, aimY):
        leaf = node.left
        data = [[leaf.x, leaf.y], [node.x, node.y], [aimX, aimY]]
        return self.createNode(data, node.deep)

    def addNode(self, node, aimX, aimY):
        if (node.childNum == 2):  # 有2个子节点
            if (node.deep % 2 == 1):  # 奇数层
                if (aimX <= node.x):  # 小于等于支节点
                    node.left = self.addNode(node.left, aimX, aimY)
                else:
                    node.right = self.addNode(node.right, aimX, aimY)
            else:  # 偶数层
                if (aimY <= node.y):  # 小于等于支节点
                    node.left = self.addNode(node.left, aimX, aimY)
                else:
                    node.right = self.addNode(node.right, aimX, aimY)

            return node
        elif (node.childNum == 1):  # 只有1个子节点
            node = self.rebuild(node, aimX, aimY)
            node.childNum = 2
            return node

        else:  # 叶子节点
            newNode = Node(aimX, aimY, node.deep + 1, 0)
            node.left = newNode
            node.childNum = 1
            return node

    '''
    add方法，输入新增物体的x值、y值
    无返回值
    '''
    def add(self, aimX, aimY):
        self.head = self.addNode(self.head, aimX, aimY)
        self.data.append([aimX, aimY])

    '''
    knn方法，输入目标物体的x值、y值，搜索的最近目标数量
    返回目标信息元组，信息包含距离、x值、y值
    '''
    def knn(self, aimX, aimY, size):
        S = [[999, 0, 0] for i in range(size)]
        assert self.head, "未生成树"
        self.search(self.head, aimX, aimY, S)
        return tuple(S)

    def search(self, node, aimX, aimY, S):
        if (node.childNum == 2):  # 有2个子节点
            if (node.deep % 2 == 1):  # 奇数层
                if (aimX <= node.x):  # 小于等于支节点
                    self.search(node.left, aimX, aimY, S)
                    if (self.far < pow(abs(aimX - node.x), 2)):
                        self.search(node.right, aimX, aimY, S)
                else:
                    self.search(node.right, aimX, aimY, S)
                    if (self.far < pow(abs(aimX - node.x), 2)):
                        self.search(node.left, aimX, aimY, S)
            else:  # 偶数层
                if (aimY <= node.y):  # 小于等于支节点
                    self.search(node.left, aimX, aimY, S)
                    if (self.far < pow(abs(aimY - node.y), 2)):
                        self.search(node.right, aimX, aimY, S)
                else:
                    self.search(node.right, aimX, aimY, S)
                    if (self.far < pow(abs(aimY - node.y), 2)):
                        self.search(node.left, aimX, aimY, S)
            self.compare(node, aimX, aimY, S)

        elif (node.childNum == 1):  # 有1个子节点
            self.search(node.left, aimX, aimY, S)
            self.compare(node, aimX, aimY, S)

        else:  # 找到叶子节点
            self.compare(node, aimX, aimY, S)

    def compare(self, node, aimX, aimY, S):
        distance = abs(node.x - aimX) + abs(node.y - aimY)
        biggest = 0
        for i in range(1, len(S)):
            if S[biggest][0] < S[i][0]:
                biggest = i
        if distance < S[biggest][0]:
            S[biggest][0] = distance
            S[biggest][1] = node.x
            S[biggest][2] = node.y
            self.far = pow(node.x - aimX, 2) + pow(node.y - aimY, 2)

    '''
    输入需要删除的节点的具体坐标，x值、y值 无返回值
    '''
    def remove(self, aimX, aimY):
        self.head = self.searchRemoveNode(self.head, aimX, aimY)

    def searchRemoveNode(self, node, aimX, aimY):
        if node.x == aimX and node.y == aimY:
            node = self.removeNode(node)
            return node
        if (node.childNum == 2):  # 有2个子节点
            if (node.deep % 2 == 1):  # 奇数层
                if (aimX <= node.x):  # 小于等于支节点
                    node.left = self.searchRemoveNode(node.left, aimX, aimY)
                else:
                    node.right = self.searchRemoveNode(node.right, aimX, aimY)
            else:  # 偶数层
                if (aimY <= node.y):
                    node.left = self.searchRemoveNode(node.left, aimX, aimY)
                else:
                    node.right = self.searchRemoveNode(node.right, aimX, aimY)
        elif (node.childNum == 1):  # 有1个子节点
            node.left = self.searchRemoveNode(node.left, aimX, aimY)
            if not node.left:  # 如果left不存在了
                node.childNum = 0
        return node

    def removeNode(self, node):
        if (node.childNum == 2):  # 有2个子节点
            if node.right:  # 右节点存在
                leftNode = node.left
                node = self.removeNode(node.right)
                node.deep -= 1
                if (node.deep % 2 == 1):  # 奇数层
                    if (leftNode.x < node.left.x):
                        node.left, node.right = leftNode, node.left
                    else:
                        node.left, node.right = node.left
                else:
                    if (leftNode.y < node.left.y):
                        node.left, node.right = leftNode, node.left
                    else:
                        node.left, node.right = node.left

            return node
        elif (node.childNum == 1):  # 只有1个子节点
            node = node.left
            node.deep -= 1
            return node

        else:  # 叶子节点
            return False


if __name__ == "__main__":
    #items = [[6, 5], [1, -3], [-6, -5], [-4, -10], [-2, -1], [-5, 12], [2, 13], [17, -12], [8, -22], [15, -13],
    #         [10, -6], [7, 15], [14, 1]]
    testItmes = [[6, 5], [1, -3], [-6, -5], [-4, -10], [-5, 12], [2, 13], [17, -12], [8, -22], [15, -13],
                 [10, -6], [7, 15], [14, 1]]
    tree = Tree()
    tree.data = testItmes
    tree.create()
    ans1 = tree.knn(-1, -5, 3)
    tree.add(-2, -1)
    ans2 = tree.knn(-1, -5, 3)
    tree.remove(-2, -1)
    ans3 = tree.knn(-1, -5, 3)
