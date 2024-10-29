import cv2
import pyautogui
import numpy as np

def find_button_center(button_image, threshold=0.7, min_matches=10):
    # 加载按钮图像并创建SIFT对象
    sift = cv2.SIFT_create()
    button_keypoints, button_descriptors = sift.detectAndCompute(button_image, None)

    # 截图并转换为灰度图像
    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

    # 检测屏幕中的特征点
    screen_keypoints, screen_descriptors = sift.detectAndCompute(screen_gray, None)

    # 使用FLANN进行特征匹配
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(button_descriptors, screen_descriptors, k=2)

    # 应用Lowe's ratio test过滤匹配
    good_matches = []
    for m, n in matches:
        if m.distance < threshold * n.distance:
            good_matches.append(m)

    # 如果有足够的好匹配，找到按钮位置
    if len(good_matches) > min_matches:
        # 获取匹配点的坐标
        src_pts = np.float32([button_keypoints[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([screen_keypoints[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算变换矩阵
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if M is not None:
            h, w = button_image.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            # 计算按钮的中心位置
            center_x = int(np.mean(dst[:, 0, 0]))
            center_y = int(np.mean(dst[:, 0, 1]))

            return center_x, center_y
    return None