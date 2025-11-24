import time
import pyautogui

# 你要点击的绝对坐标
TARGET_X = 285      # ← 根据你的需求修改
TARGET_Y = 733      # ← 根据你的需求修改

INTERVAL = 1.0       # 点击间隔（秒）

print(f"开始自动点击，坐标=({TARGET_X}, {TARGET_Y})，每 {INTERVAL} 秒一次。")
print("按 Ctrl + C 可随时停止。\n")

try:
    while True:
        pyautogui.click(TARGET_X, TARGET_Y)
        print(f"点击：({TARGET_X}, {TARGET_Y})")
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\n已停止自动点击。")
