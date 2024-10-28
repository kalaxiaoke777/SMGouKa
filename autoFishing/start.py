import cv2
import numpy as np
import pyautogui
import time
# import keyboard  # 用于监听键盘事件


class ButtonClicker:
    def __init__(self, button_image_path):
        # 加载按钮图像
        self.button_image = cv2.imread(button_image_path)
        self.button_height, self.button_width = self.button_image.shape[:2]
        self._start = False

    @property
    def status(self):
        """关闭循环"""
        return self._start


    def start_fishing(self):
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)

        # 转换颜色格式从RGB到BGR
        screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # 在屏幕上查找按钮
        result = cv2.matchTemplate(screen_bgr, self.button_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 设置匹配阈值
        loc = np.where(result >= threshold)

        # 如果找到按钮，点击按钮的中心位置
        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):  # (x, y)坐标
                center_x = pt[0] + self.button_width // 2
                center_y = pt[1] + self.button_height // 2

                # 使用 PyAutoGUI 点击按钮
                pyautogui.click(center_x, center_y)
                print("开始钓鱼，进入循环步骤。。。。")
                self._start = True
                return True
        return False

class Tettisonin:
    def __init__(self,button_image_path):
        self.button_image = cv2.imread(button_image_path)
        self.button_height, self.button_width = self.button_image.shape[:2]
        self._start = False


    @property
    def status(self):
        return self._start
    def find_button(self):
        """查找按钮"""
        # 截取游戏窗口的屏幕
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)

        # 转换颜色格式从RGB到BGR
        screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # 在屏幕上查找按钮
        result = cv2.matchTemplate(screen_bgr, self.button_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 设置匹配阈值
        loc = np.where(result >= threshold)

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):  # (x, y)坐标
                center_x = pt[0] + self.button_width // 2
                center_y = pt[1] + self.button_height // 2
                return center_x, center_y
        return None

    def tettisonin_drag(self):
        """查找按钮并点击，然后向上拖拽一段距离"""
        # 查找按钮
        button_position = self.find_button()
        if button_position:
            center_x, center_y = button_position
            # 使用 PyAutoGUI 点击按钮
            pyautogui.mouseDown(center_x, center_y)
            print(f"Clicked at: ({center_x}, {center_y})")

            # 向上拖拽一段距离
            drag_distance = 80  # 拖拽的距离，可以调整
            pyautogui.moveTo(center_x, center_y - drag_distance, duration=0.5)
            pyautogui.mouseUp()
            self._start = True

class Pull:
    def __init__(self, button_image_path,pull_hook_button):
        # 加载按钮图像
        self.button_image = cv2.imread(button_image_path)
        self.pull_button_image = cv2.imread(pull_hook_button)
        self.button_height, self.button_width = self.button_image.shape[:2]
        self.pull_button_height, self.pull_button_width = self.pull_button_image.shape[:2]
        self._start = False
    @property
    def status(self):
        return self._start

    def find_button(self):

        """查找按钮"""
        # 截取游戏窗口的屏幕
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)

        # 转换颜色格式从RGB到BGR
        screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # 在屏幕上查找按钮
        result = cv2.matchTemplate(screen_bgr, self.button_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.4  # 设置匹配阈值
        loc = np.where(result >= threshold)

        if loc[0].size > 0:
            print("开始提纲")
            self.find_pull_button()
        return None

    def find_pull_button(self):
        """查找按钮"""
        # 截取游戏窗口的屏幕
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)

        # 转换颜色格式从RGB到BGR
        screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # 在屏幕上查找按钮
        result = cv2.matchTemplate(screen_bgr, self.pull_button_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 设置匹配阈值
        loc = np.where(result >= threshold)

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):  # (x, y)坐标
                center_x = pt[0] + self.button_width // 2
                center_y = pt[1] + self.button_height // 2
                return center_x, center_y
        return None

    def pull_hook(self):
        button_position = self.find_pull_button()
        if button_position:
            center_x, center_y = button_position
            # 使用 PyAutoGUI 点击按钮
            pyautogui.mouseDown(center_x, center_y)
            print(f"Clicked at: ({center_x}, {center_y})")

            # 向上拖拽一段距离
            drag_distance = 80  # 拖拽的距离，可以调整
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

