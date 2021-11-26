import matplotlib.pyplot as plt
import numpy as np

'''
卡尔曼滤波:
将一个预测结果和一个观测结果进行"加权"评估，得到一个"加权"结果。不涉及预测功能!
目前的想法是对位移进行评估，在将位移添加回位置中
输入参数:
realPosition:传感器输入的带噪音的位置
o:过程噪声，在跟踪任务当中，过程噪声来自于目标移动的不确定性（突然加速、减速、转弯等）
a:测量噪声
返回值：
预测位置的列表
'''


class Kalman():
    def __init__(self, realPosition, o, a):
        self.realPosition = realPosition
        self.predicts = [realPosition[0]]  # 预测位置列表
        self.position_predict = realPosition[0]  # 最后的预测位置
        self.predict_var = 0  # 预测误差方差
        self.odo_var = o ** 2
        self.v_std = a

    def predict(self):
        for i in range(1, len(self.realPosition)):  # 迭代实际位置-1次
            self.predict_var += self.v_std ** 2  # 更新预测数据的方差
            # 下面是Kalman滤波
            # 预测期望
            self.position_predict = self.position_predict * self.odo_var / (self.predict_var + self.odo_var) + \
                                    self.realPosition[i] * self.predict_var / (self.predict_var + self.odo_var)
            # 预测方差
            self.predict_var = (self.predict_var * self.odo_var) / (self.predict_var + self.odo_var)
            # 卡尔曼增益参数似乎需要额外计算且不参与评估,这里就没写了
            self.predicts.append(self.position_predict)


# 使用范例
if __name__ == '__main__':
    length = 50
    # position为目标方程
    position = np.linspace(1, 10, length)
    position = np.square(position) - 8 * position + 12
    position /= 3
    # position_noise为误差方差在sigma内带噪音目标方程
    sigma = 6
    position_noise = position + np.random.random([length]) * sigma - sigma / 2

    t = np.linspace(1, length, length)
    plt.plot(t, position, label='truth position')
    plt.plot(t, position_noise, label='input position')
    # 进行预测
    km = Kalman(position_noise, 12, 5)  # 这两个参数建议根据实际情况调参
    km.predict()

    plt.plot(t, km.predicts, label='kalman filtered position')
    plt.legend()
    plt.show()
