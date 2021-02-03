#inputList保存了训练的4个人，其中第一位是训练目标，其他三人是训练参数
inputList=["zh","gg","zh","sz"]
#saveUrl为保存和读取时权重路径，如果不想保存则设为False
saveUrl = "./weights.npz"
#testList为进行预测时其他三人的成绩/100，成绩顺序不得更改
testList=[0.83,0.71,0.76]
