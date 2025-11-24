from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:  # 鼠标按下瞬间触发
        print(f"你点击的绝对坐标是：({x}, {y})")

        # 输出后退出监听
        return False

print("脚本已启动，请点击屏幕任意位置，我会告诉你点击的绝对坐标。")

# 启动监听
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
