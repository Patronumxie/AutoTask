import time
import subprocess
import pywinauto

# 使用 control 命令打开 Internet 属性窗口
subprocess.run('control inetcpl.cpl')

# 等待窗口打开
time.sleep(2)

# 使用 pywinauto 获取 "Internet 属性" 窗口
app = pywinauto.Application().connect(title='Internet 属性')  # 连接到"Internet 属性"窗口
window = app.window(title='Internet 属性')

# 切换到 "连接" 选项卡 (按下 Ctrl + Tab 4 次)
window.type_keys('^t' * 4)  # 使用 Ctrl + Tab 切换选项卡

# 点击“局域网设置”按钮
window.child_window(title="局域网设置", control_type="Button").click()
time.sleep(2)  # 等待“局域网设置”窗口打开

# 获取“局域网设置”窗口
lan_window = app.window(title='局域网设置')

# 查找复选框并点击（按控件名称定位复选框）
# 假设复选框的文本是 "自动检测设置"，你可以通过控件的名称来定位
checkbox = lan_window.child_window(title="自动检测设置", control_type="CheckBox")

# 点击复选框
checkbox.click()

print("已点击复选框")
