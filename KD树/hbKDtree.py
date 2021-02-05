# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 17:06:47 2021
@author: root
"""
import time

class Node:
    def __init__(self,data,deep):
        if len(data)>=3:# 有两个子节点
            self.deep = deep
            mid = len(data)//2# 如遇偶数，选较大的那个为当前节点
            if deep%2 == 1:# 奇数层对X进行排序
                data.sort(key = self.sortX) 
            else:# 偶数层对Y进行排序
                data.sort(key = self.sortY) 
            self.x = data[mid][0]
            self.y = data[mid][1]

            leftList = data[0:mid]
            rightList = data[mid+1:]
            self.left = Node(leftList,deep+1)
            self.right = Node(rightList,deep+1)
            self.child = 2
            
        elif len(data)==2:# 只有一个子节点
            self.deep = deep
            if deep%2 == 1:# 奇数层对X进行排序
                data.sort(key = self.sortX) 
            else:# 偶数层对Y进行排序
                data.sort(key = self.sortY) 
            self.x = data[1][0]# 将小的放子节点里
            self.y = data[1][1]
            
            small = [data[0]]
            self.left=Node(small, deep+1)
            self.right=False
            self.child = 1
            
        else:# 此节点就是叶子节点
            self.deep = deep
            self.x = data[0][0]
            self.y = data[0][1]
            self.left = False
            self.right = False
            self.child = 0
        
    def sortX(self,inputList):
        return inputList[0]
    
    def sortY(self,inputList):
        return inputList[1]

class Tree:
    def __init__(self):
        self.data = []
    
    def sortX(self,inputList):
        return inputList[0]
    
    def sortY(self,inputList):
        return inputList[0]
        
    #def createTree(self):
if __name__ == "__main__":
    start = time.time()
    t = Node([[1,3],[4,6],[2,5],[8,4],[1,2],[1,4]], 1)
    useTime = time.time()-start
    print(f"用时{useTime*1000}秒")
    
    
