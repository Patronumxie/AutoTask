from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError
import time
import sys

def detect_and_minimize_window(window_title, checkbox_text, check_interval=1):
    """
    检测指定窗口并勾选其中的复选框，然后最小化窗口
    
    参数:
    window_title (str): 精确匹配的窗口标题
    checkbox_text (str): 复选框旁边的文本
    check_interval (float): 检查间隔时间(秒)
    """
    print(f"开始检测窗口: '{window_title}'")
    print(f"目标复选框文本: '{checkbox_text}'")
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
                    
                    # 查找复选框控件 - 使用更通用的方法
                    checkbox = None
                    
                    # 尝试通过自动化ID或文本查找复选框
                    try:
                        # 先尝试通过文本直接查找
                        checkbox = main_window.child_window(title=checkbox_text, control_type="CheckBox")
                        checkbox.wait('visible', timeout=5)  # 等待控件可见
                    except Exception:
                        # 如果直接查找失败，尝试遍历所有子元素
                        print("通过文本直接查找失败，正在遍历所有子元素...")
                        children = main_window.descendants()
                        for child in children:
                            try:
                                # 检查元素是否为复选框(通过自动化属性判断)
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
                        # 使用更通用的方式检查和设置勾选状态
                        try:
                            # 检查复选框是否已勾选
                            is_checked = checkbox.get_toggle_state() == 1
                            
                            if not is_checked:
                                # 点击复选框
                                checkbox.click_input()
                                print("复选框已成功勾选")
                            else:
                                print("复选框已经是勾选状态")
                            
                            # 最小化窗口
                            main_window.minimize()
                            print(f"窗口 '{title}' 已成功最小化")
                        except Exception as e:
                            print(f"操作复选框时出错: {e}")
                            print("尝试使用替代方法...")
                            
                            # 替代方法：通过坐标点击
                            try:
                                # 获取复选框位置
                                rect = checkbox.rectangle()
                                center_x = (rect.left + rect.right) // 2
                                center_y = (rect.top + rect.bottom) // 2
                                
                                # 点击复选框中心
                                main_window.click_input(coords=(center_x, center_y))
                                print("已通过坐标点击方式尝试勾选复选框")
                                
                                # 最小化窗口
                                main_window.minimize()
                                print(f"窗口 '{title}' 已成功最小化")
                            except Exception as e2:
                                print(f"替代方法也失败: {e2}")
                    else:
                        print(f"未找到匹配的复选框: '{checkbox_text}'")
                    
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
    
    # 开始检测窗口并勾选复选框
    detect_and_minimize_window(target_window_title, target_checkbox_text, check_interval=2)