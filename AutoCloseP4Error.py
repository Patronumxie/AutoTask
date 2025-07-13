from pywinauto.application import Application
from pywinauto import Desktop
import time
import sys

def detect_and_close_window(window_title_pattern, check_interval=1):
    """
    检测并关闭包含指定标题的窗口
    
    参数:
    window_title_pattern (str): 窗口标题的正则表达式模式
    check_interval (float): 检查间隔时间(秒)
    """
    print(f"开始检测窗口: {window_title_pattern}")
    print(f"检测间隔: {check_interval}秒")
    print("按 Ctrl+C 停止程序")
    
    try:
        while True:
            # 获取所有顶级窗口
            windows = Desktop(backend="uia").windows()
            
            # 检查是否存在匹配的窗口
            matched_windows = []
            for window in windows:
                if window_title_pattern in window.window_text():
                    matched_windows.append(window)
            
            if matched_windows:
                print(f"\n找到 {len(matched_windows)} 个匹配的窗口")
                
                for window in matched_windows:
                    title = window.window_text()
                    print(f"正在关闭窗口: {title}")
                    
                    try:
                        # 尝试关闭窗口
                        window.close()
                        
                        # 验证窗口是否已关闭 (UIAutomation 后端的正确方式)
                        time.sleep(0.5)  # 等待窗口关闭
                        try:
                            # 尝试获取窗口的属性，如果失败则表示窗口已关闭
                            window.window_text()
                            print(f"窗口 '{title}' 未能关闭，尝试强制关闭")
                            window.set_focus()
                            window.type_keys("%{F4}")  # Alt+F4
                        except Exception:
                            print(f"窗口 '{title}' 已成功关闭")
                    except Exception as e:
                        print(f"关闭窗口时出错: {e}")
            else:
                # 打印点号表示检测中，不换行
                print(".", end="", flush=True)
            
            # 等待指定的间隔时间
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n程序已停止")
        sys.exit(0)

if __name__ == "__main__":
    # 设置要检测的窗口标题关键词
    target_title = "计算器"
    
    # 开始检测并关闭窗口
    detect_and_close_window(target_title, check_interval=2)