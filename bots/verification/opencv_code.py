import re

from PIL import Image
import cv2
import numpy as np

import pytesseract as pytesseract
import os


class OpencvCode:
    def __init__(self, image_path=None):
        self.image_path = image_path

    def read_code(self):
        img = cv2.imread(self.image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)
        # 固定阈值二值化
        ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        # 自适应二值化
        # binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 25, 10)
        # cv2.imshow("binary", binary)

        # 形态学的处理，滤除噪点
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
        dilate_image = cv2.dilate(binary, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        erode_image = cv2.erode(dilate_image, kernel)
        # cv2.imshow("erode_image", erode_image)

        # 将dilate_image转为Image
        text_image = Image.fromarray(erode_image)
        # 识别
        char = pytesseract.image_to_string(text_image, lang='eng', config="--psm 6 --tessdata-dir tessdata")
        char = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", char)  # 去除识别出来的特殊字符
        char = char[0:4]  # 只获取前4个字符
        print(char)
        return char
