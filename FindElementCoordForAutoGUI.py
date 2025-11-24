import time
import pygetwindow as gw
import pyautogui

# TARGET_TITLE = "Internet 属性"   # 目标窗口标题，可修改
TARGET_TITLE = "Chrome Legacy Window"   # 目标窗口标题，可修改
CHECK_INTERVAL = 0.5             # 检测间隔

def wait_for_window(title):
    print(f"正在等待窗口：'{title}' ...")
    while True:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            print("窗口已找到！")
            return windows[0]
        print(".", end="", flush=True)
        time.sleep(CHECK_INTERVAL)

# 等待目标窗口出现
window = wait_for_window(TARGET_TITLE)

# 获取窗口位置
window_x, window_y = window.topleft
print(f"\n窗口左上角坐标: ({window_x}, {window_y})")

# 让用户手动标记按钮位置
input("请把鼠标移动到“局域网设置”按钮位置，然后按回车...")

# 读鼠标位置
x_rel, y_rel = pyautogui.position()
print(f"鼠标屏幕坐标: ({x_rel}, {y_rel})")

# 计算相对坐标
x_relative = x_rel - window_x
y_relative = y_rel - window_y
print(f"按钮相对窗口坐标: ({x_relative}, {y_relative})")

# 使用窗口坐标 + 相对坐标点击
absolute_x = window_x + x_relative
absolute_y = window_y + y_relative

print("开始点击按钮...")
pyautogui.click(absolute_x, absolute_y)
print("点击完成！")
