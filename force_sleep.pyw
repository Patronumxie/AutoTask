import datetime
import tkinter as tk
from tkinter import font
import setproctitle
import random
import string
from ctypes import windll

# 生成随机字符串
random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
# 设置进程名称
setproctitle.setproctitle(random_string)


class SleepAlertApp(tk.Tk):
    def __init__(self, width, height, message):
        super().__init__()
        self.title('睡眠提醒')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f'{width}x{height}+{x}+{y}')  # 设置窗口大小并居中显示
        self.resizable(False, False)  # 禁止调整窗口大小
        self.attributes('-topmost', True)  # 窗口置顶显示
        self.attributes('-toolwindow', True)  # 禁止窗口最小化
        self.overrideredirect(True)  # 隐藏窗口标题栏和边框

        self.protocol("WM_DELETE_WINDOW", self.on_close)  # 捕获窗口关闭事件
        self.show_sleep_alert(message)

    def show_sleep_alert(self, message):
        # 创建自定义字体对象
        custom_font = font.Font(family='Microsoft YaHei', size=30)

        label = tk.Label(self, text=message, font=custom_font)

        # 使用place方法手动放置标签部件
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.transient(self.master)  # 设置窗口为模态对话框
        self.grab_set()  # 阻止对其他窗口进行操作

        # 禁用鼠标事件，阻止窗口的移动
        label.bind('<ButtonPress-1>', lambda event: 'break')
        label.bind('<B1-Motion>', lambda event: 'break')

    def on_close(self):
        pass  # 阻止窗口关闭

    def on_close_and_open_new_window(self):
        self.destroy()  # 关闭当前窗口

        # 创建新的窗口，大小为700x500，文本不变
        app = SleepAlertApp(width=3840, height=2160,
                            message="快点睡觉！\n\n熬夜很危险！\n\n熬夜会影响健康，免疫力下降，\n\n脑子变迟钝，情绪失控，连外貌都受影响！\n\n睡眠很重要！照顾自己，多睡觉！")
        app.mainloop()


class Detect:
    def __init__(self):
        now = datetime.datetime.now()
        if 2 <= now.hour < 8:
            # app = SleepAlertApp(width=3840, height=200, message="1分钟后电脑无法使用，请关闭所有工作并关机")
            # app.after(60000, app.on_close_and_open_new_window)  # 5秒后关闭当前窗口，并弹出新窗口
            # app.mainloop()

            # 创建新的窗口，大小为700x500，文本不变
            app = SleepAlertApp(width=3840 * 3, height=2160 * 3,
                                message="除却生死，人世间再无大事！")
            app.mainloop()


if __name__ == '__main__':
    user32 = windll.user32
    user32.SetProcessDPIAware()
    detect = Detect()