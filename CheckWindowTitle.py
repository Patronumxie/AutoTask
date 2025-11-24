from pynput import mouse
import win32gui

def on_click(x, y, button, pressed):
    if pressed:  # 只在鼠标按下时触发
        print(f"你点击了坐标: ({x}, {y})")

        # 根据坐标找到窗口句柄
        hwnd = win32gui.WindowFromPoint((x, y))

        if hwnd:
            # 获取窗口标题
            title = win32gui.GetWindowText(hwnd)
            print(f"窗口句柄: {hwnd}")
            print(f"窗口标题: '{title}'" if title else "窗口没有标题")
        else:
            print("没有找到窗口")

        # 输出后退出监听
        return False  

# 提示
print("脚本已启动。请随便点击屏幕任意位置，我会告诉你该点所在窗口的标题。")

# 启动监听
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
