from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError
import time
import sys

def detect_and_minimize_window(window_title, checkbox_text, button_text, check_interval=1):
    """
    检测指定窗口并勾选其中的复选框，然后点击按钮
    
    参数:
    window_title (str): 精确匹配的窗口标题
    checkbox_text (str): 复选框旁边的文本
    button_text (str): 按钮上的文本
    check_interval (float): 检查间隔时间(秒)
    """
    print(f"开始检测窗口: '{window_title}'")
    print(f"目标复选框文本: '{checkbox_text}'")
    print(f"目标按钮文本: '{button_text}'")
    print(f"检测间隔: {check_interval}秒")
    print("按 Ctrl+C 停止程序")
    
    try:
        while True:
            # 获取所有顶级窗口
            windows = Desktop(backend="uia").windows()
            
            # 检查是否存在完全匹配标题的窗口
            target_window = None
            for window in windows:
                if window.window_text() == window_title:
                    target_window = window
                    break
            
            if target_window:
                title = target_window.window_text()
                print(f"\n找到匹配窗口: '{title}'")
                print("正在尝试勾选复选框...")
                
                try:
                    # 获取窗口进程ID
                    process_id = target_window.process_id()
                    
                    # 通过进程ID连接到应用程序
                    app = Application(backend="uia").connect(process=process_id)
                    
                    # 获取主窗口
                    main_window = app.window(title_re=title)
                    main_window.set_focus()  # 设置窗口焦点
                    
                    # 查找复选框控件
                    checkbox = None
                    try:
                        checkbox = main_window.child_window(title=checkbox_text, control_type="CheckBox")
                        checkbox.wait('visible', timeout=5)  # 等待控件可见
                    except Exception:
                        print("通过文本直接查找复选框失败，正在遍历所有子元素...")
                        children = main_window.descendants()
                        for child in children:
                            try:
                                if child.element_info.control_type == "CheckBox":
                                    child_text = child.window_text()
                                    if checkbox_text in child_text:
                                        checkbox = child
                                        print(f"找到匹配复选框: '{child_text}'")
                                        break
                            except Exception:
                                continue
                    
                    if checkbox:
                        # 勾选复选框
                        try:
                            is_checked = checkbox.get_toggle_state() == 1
                            
                            if not is_checked:
                                checkbox.click_input()
                                print("复选框已成功勾选")
                            else:
                                print("复选框已经是勾选状态")
                            
                            # 查找并点击Connect按钮
                            print("正在查找并点击Connect按钮...")
                            connect_button = None
                            
                            try:
                                # 尝试通过文本直接查找按钮
                                connect_button = main_window.child_window(title=button_text, control_type="Button")
                                connect_button.wait('enabled', timeout=5)  # 等待按钮可用
                            except Exception:
                                # 如果直接查找失败，尝试遍历所有按钮
                                print("通过文本直接查找按钮失败，正在遍历所有按钮...")
                                buttons = main_window.descendants(control_type="Button")
                                for btn in buttons:
                                    try:
                                        btn_text = btn.window_text()
                                        if button_text in btn_text:
                                            connect_button = btn
                                            print(f"找到匹配按钮: '{btn_text}'")
                                            break
                                    except Exception:
                                        continue
                            
                            if connect_button:
                                # 点击按钮
                                connect_button.click_input()
                                print(f"'{button_text}' 按钮已成功点击")
                                
                                # 最小化窗口(可选，根据实际需求决定是否保留)
                                # main_window.minimize()
                                # print(f"窗口 '{title}' 已成功最小化")
                            else:
                                print(f"未找到匹配的按钮: '{button_text}'")
                                # 如果没找到按钮，仍然最小化窗口
                                main_window.minimize()
                                print(f"窗口 '{title}' 已成功最小化")
                            
                        except Exception as e:
                            print(f"操作复选框或按钮时出错: {e}")
                    else:
                        print(f"未找到匹配的复选框: '{checkbox_text}'")
                        # 如果没找到复选框，仍然尝试查找并点击按钮
                        print("正在尝试直接查找并点击Connect按钮...")
                        connect_button = None
                        
                        try:
                            connect_button = main_window.child_window(title=button_text, control_type="Button")
                            connect_button.wait('enabled', timeout=5)
                        except Exception:
                            print("通过文本直接查找按钮失败，正在遍历所有按钮...")
                            buttons = main_window.descendants(control_type="Button")
                            for btn in buttons:
                                try:
                                    btn_text = btn.window_text()
                                    if button_text in btn_text:
                                        connect_button = btn
                                        print(f"找到匹配按钮: '{btn_text}'")
                                        break
                                except Exception:
                                    continue
                        
                        if connect_button:
                            connect_button.click_input()
                            print(f"'{button_text}' 按钮已成功点击")
                        else:
                            print(f"未找到匹配的按钮: '{button_text}'")
                            # 如果按钮也没找到，最小化窗口
                            main_window.minimize()
                            print(f"窗口 '{title}' 已成功最小化")
                    
                except ElementNotFoundError:
                    print(f"找不到目标窗口元素: {title}")
                except Exception as e:
                    print(f"操作窗口时出错: {e}")
            else:
                # 打印点号表示检测中，不换行
                print(".", end="", flush=True)
            
            # 等待指定的间隔时间
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n程序已停止")
        sys.exit(0)

if __name__ == "__main__":
    # 设置要检测的窗口标题(精确匹配)
    target_window_title = "Perforce Fingerprint Required"
    # 设置要查找的复选框文本
    target_checkbox_text = "Trust this fingerprint for future connections"
    # 设置要查找的按钮文本
    target_button_text = "Connect"
    
    # 开始检测窗口、勾选复选框并点击按钮
    detect_and_minimize_window(target_window_title, target_checkbox_text, target_button_text, check_interval=2)