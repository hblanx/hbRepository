# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 17:06:47 2021
@author: hblanx
"""
import time

class Node:
    def __init__(self,x,y,deep,childNum):
       self.x = x
       self.y = y
       self.deep = deep
       self.childNum = childNum

class Tree:
    def __init__(self):
        self.data = []
        self.head = False
    
    def sortX(self,inputList):
        return inputList[0]
    
    def sortY(self,inputList):
        return inputList[1]
    
    def create(self):
        self.head = self.createNode(self.data,1)
        
    def createNode(self,data,deep):
        if len(data)>=3:# 有两个子节点
            mid = len(data)//2# 如遇偶数，选较大的那个为当前节点
            if deep%2 == 1:# 奇数层对X进行排序
                data.sort(key = self.sortX) 
            else:# 偶数层对Y进行排序
                data.sort(key = self.sortY) 
            x = data[mid][0]
            y = data[mid][1]
            leftList = data[0:mid]
            rightList = data[mid+1:]
            
            node = Node(x, y, deep, 2)
            node.left = self.createNode(leftList,deep+1)
            node.right = self.createNode(rightList,deep+1)

            
        elif len(data)==2:# 只有一个子节点
            if deep%2 == 1:# 奇数层对X进行排序
                data.sort(key = self.sortX) 
            else:# 偶数层对Y进行排序
                data.sort(key = self.sortY) 
            x = data[1][0]# 将小的放子节点里
            y = data[1][1] 
            smallData = [data[0]]
            
            node = Node(x, y, deep, 1)
            node.left=self.createNode(smallData, deep+1)
            node.right=False
            
        else:# 此节点就是叶子节点
            x = data[0][0]
            y = data[0][1]
            
            node = Node(x, y, deep, 0)
            node.left = False
            node.right = False
            
        return node
    
    def knn(self,aimX,aimY,size):
        S = size * [[999,0,0]]
        self.search(self.head, aimX, aimY, S)
        return tuple(S)
        
    def search(self,node,aimX,aimY,S):
        if(node.childNum == 2):# 有2个子节点
            if(node.deep%2 == 1):# 奇数层
                if(aimX<=node.x):# 小于等于支节点
                    self.search(node.left, aimX, aimY, S)
                    if(pow(aimX,2)+pow(aimY,2) < pow(abs(aimX-node.x),2)):
                        self.search(node.right, aimX, aimY, S)
                else:
                    self.search(node.right, aimX, aimY, S)
                    if(pow(aimX,2)+pow(aimY,2) < pow(abs(aimX-node.x),2)):
                        self.search(node.left, aimX, aimY, S)
            else:# 偶数层
                if(aimY<=node.y):# 小于等于支节点
                    self.search(node.left, aimX, aimY, S)
                    if(pow(aimX,2)+pow(aimY,2) < pow(abs(aimY-node.y),2)):
                        self.search(node.right, aimX, aimY, S)
                else:
                    self.search(node.right, aimX, aimY, S)
                    if(pow(aimX,2)+pow(aimY,2) < pow(abs(aimY-node.y),2)):
                        self.search(node.left, aimX, aimY, S)
            self.compare(node, aimX, aimY, S)
            
        elif(node.childNum == 1):# 有1个子节点
            self.search(node.left, aimX, aimY, S)
            self.compare(node, aimX, aimY, S)
        
        else:# 找到叶子节点
            self.compare(node, aimX, aimY, S)
                   
    def compare(self,node,aimX,aimY,S):
        distance = abs(node.x+node.y-aimX-aimY)
        for i in range(0,len(S)):
            if distance < S[i][0]:
                S[i][0] = distance
                S[i][1] = node.x
                S[i][2] = node.y
                break
            
            
        
if __name__ == "__main__":
    start = time.time()
    items = [[1,3],[4,6],[2,5],[8,4],[1,2],[1,4]]
    tree = Tree()
    tree.data = items
    tree.create()
    ans = tree.knn(1, 5, 1)
    useTime = time.time()-start
    print(f"用时{useTime*1000}秒")
    
    
