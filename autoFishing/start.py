import cv2
import numpy as np
import pyautogui
import time
from utils.flann import find_button_center
class ButtonClicker:
    def __init__(self, button_image_path):
        # 加载按钮图像
        self.button_image = cv2.imread(button_image_path, cv2.IMREAD_GRAYSCALE)
        self._start = False

    @property
    def status(self):
        """关闭循环"""
        return self._start

    def start_fishing(self):
        # 截图并转换为灰度图像
        center = find_button_center(self.button_image)
        if center:
            center_x, center_y = center
            # 点击按钮
            pyautogui.click(center_x, center_y)
            print("开始钓鱼，进入循环步骤。。。。")
            self._start = True
            return True
        return False

class Tettisonin:
    def __init__(self, button_image_path):
        self.button_image = cv2.imread(button_image_path, cv2.IMREAD_GRAYSCALE)
        self._start = False

    @property
    def status(self):
        return self._start

    def tettisonin_drag(self):
        """查找按钮并点击，然后向上拖拽一段距离"""
        # 查找按钮
        button_position = find_button_center(self.button_image)
        if button_position:
            center_x, center_y = button_position
            # 使用 PyAutoGUI 点击按钮
            pyautogui.mouseDown(center_x, center_y)
            print(f"Clicked at: ({center_x}, {center_y})")

            # 向上拖拽一段距离
            drag_distance = 50  # 拖拽的距离，可以调整
            pyautogui.moveTo(center_x, center_y - drag_distance, duration=0.5)
            pyautogui.mouseUp()
            self._start = True

class Pull:
    def __init__(self, button_image_path,pull_hook_button):
        # 加载按钮图像
        self.button_image = cv2.imread(button_image_path, cv2.IMREAD_GRAYSCALE)
        self.pull_button_image = cv2.imread(pull_hook_button, cv2.IMREAD_GRAYSCALE)
        self._start = False
    @property
    def status(self):
        return self._start

    def find_button(self):

        """查找按钮"""
        button_position = find_button_center(self.button_image)
        if button_position:
            self.pull_hook()

    def pull_hook(self):
        button_position = find_button_center(self.pull_button_image)
        if button_position:
            center_x, center_y = button_position
            # 使用 PyAutoGUI 点击按钮
            pyautogui.mouseDown(center_x, center_y)
            print(f"Clicked at: ({center_x}, {center_y})")

            # 向上拖拽一段距离
            drag_distance = 50  # 拖拽的距离，可以调整
            pyautogui.moveTo(center_x, center_y - drag_distance, duration=0.5)
            pyautogui.mouseUp()
            self._start = True




start_image_path = './images/start.png'
jettisonin_image_path = './images/jettisonin.png'
pull_image_path = './images/pull.png'
pull_hook_image_path = './images/pull_hook.png'
startFishing = ButtonClicker(start_image_path)
jettisonin = Tettisonin(jettisonin_image_path)
pullHook = Pull(pull_image_path,pull_hook_image_path)
while True:
    if not startFishing.status:
        isStart = startFishing.start_fishing()
        time.sleep(0.5)  # 避免重复点击
        continue
    if not jettisonin.status:
        print("执行抛竿")
        jettisonin.tettisonin_drag()
        time.sleep(0.5)
        continue
    if not pullHook.status:
        print("点击抛竿")
        pullHook.find_button()
        time.sleep(0.5)
        continue
    print("钓鱼逻辑")

