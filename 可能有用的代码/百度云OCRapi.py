import base64
import json
import requests


class BaiduAPI():
    def __init__(self):
        # 请求地址
        self.request_url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        # ！需要修改的配置信息！
        # 网上建议使用.env格式文件保存敏感信息
        # with open("", "r") as f:
        #     msg = f.read()
        # self.loginInfo = json.loads(msg)
        self.loginInfo = {"API_KEY": "",
                          "SECRET_KEY": ""}

    def get_access_token(self):
        # 获得实时刷新的access_token
        host = 'https://aip.baidubce.com/oauth/2.0/token' \
               f'?grant_type=client_credentials&client_id={self.loginInfo["API_KEY"]}' \
               f'&client_secret={self.loginInfo["SECRET_KEY"]}'
        response = requests.get(host)
        response = response.json()["access_token"]
        if response:
            return response
        else:
            return 0

    def ocr(self, img):
        # 接收numpy数组图片,返回[{"word":"识别内容"},...]
        img = str(base64.b64encode(img))[2:-1]
        params = {'image': img}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        access_token = self.get_access_token()
        request_url = self.request_url + "?access_token=" + access_token
        response = requests.post(request_url, data=params, headers=headers)
        response = response.json()["words_result"]
        if response:
            # print("debug,response.json",response.json())
            return response
        else:
            return 0


if __name__ == '__main__':
    import cv2
    # 使用方法
    bd = BaiduAPI()
    img = cv2.imread("./img/798.jpg")
    # 注意编写成流
    img = cv2.imencode('.jpg', img)[1]
    resp = bd.ocr(img)
    print(resp)
