import uiautomation as auto

def check_and_print_controls(ctrl, x, y, depth=0, found_flag=None):
    """
    递归打印控件信息，并检查是否存在 ButtonControl 名称包含 '预约'
    """
    if found_flag is None:
        found_flag = [False]

    rect = ctrl.BoundingRectangle
    indent = "  " * depth

    # 点击点是否在控件矩形内
    if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
        # 打印控件信息
        print(f"{indent}- 类型: {ctrl.ControlTypeName}, 名称: '{ctrl.Name}', "
              f"AutomationId: '{ctrl.AutomationId}', 矩形: {rect}")

        # 判断是否是目标按钮（去掉空格并部分匹配）
        if ctrl.ControlTypeName == "ButtonControl" and "预约" in ctrl.Name.strip():
            found_flag[0] = True

        # 递归遍历子控件
        try:
            for child in ctrl.GetChildren():
                check_and_print_controls(child, x, y, depth + 1, found_flag)
        except Exception as e:
            print(f"{indent}  无法获取子控件: {e}")

    return found_flag

if __name__ == "__main__":
    # 点击坐标（替换为实际屏幕坐标）
    x, y = 778, 300

    try:
        # 获取点击位置对应的控件
        root_ctrl = auto.ControlFromPoint(x, y)
        # 开始递归检测并打印
        found_flag = check_and_print_controls(root_ctrl, x, y)

        # 输出最终判断
        if found_flag[0]:
            print("\n结果: 可以预约")
        else:
            print("\n结果: 无法预约")

    except Exception as e:
        print(f"检测控件失败: {e}")
