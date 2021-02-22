import numpy as np
import win32gui, win32ui, win32con, win32api
import cv2

'''
getScreen函数使用win32api截屏，返回bitmap对象
main函数有介绍怎么用numpy和opencv操作bitmap，并生成图像
'''
def getScreen(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img


if __name__ == "__main__":
    # 测试截图位置时使用
    windowSize = (960, 0, 1920, 1080)
    while True:
        screen1 = cv2.cvtColor(getScreen(windowSize),cv2.COLOR_BGRA2RGB)
        cv2.imshow('window1', screen1)
        if cv2.waitKey(500) == 27:# 循环功能，输入ascii值为27的esc键退出循环
            cv2.imwrite("img.jpg", screen1, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存
            break
    cv2.destroyAllWindows()
