#!/usr/bin/env python3
"""
交互式骑士巡游问题求解器
用户可以通过简单的输入来运行程序
"""

from knight_tour import KnightTour
import sys

def get_valid_input(prompt, min_val, max_val):
    """获取有效的用户输入"""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"请输入 {min_val} 到 {max_val} 之间的数字")
        except ValueError:
            print("请输入一个有效的数字")

def main():
    print("=== 骑士巡游问题求解器 ===")
    print()
    
    # 获取棋盘大小
    size = get_valid_input("请输入棋盘大小 (建议4-8): ", 3, 10)
    
    print(f"\n棋盘坐标范围: (0,0) 到 ({size-1},{size-1})")
    
    # 获取起点
    print("\n请输入起点坐标:")
    start_x = get_valid_input(f"起点X坐标 (0-{size-1}): ", 0, size-1)
    start_y = get_valid_input(f"起点Y坐标 (0-{size-1}): ", 0, size-1)
    
    # 询问是否指定终点
    specify_end = input("\n是否指定终点? (y/n): ").lower().strip()
    end_x, end_y = None, None
    
    if specify_end in ['y', 'yes', '是']:
        print("请输入终点坐标:")
        end_x = get_valid_input(f"终点X坐标 (0-{size-1}): ", 0, size-1)
        end_y = get_valid_input(f"终点Y坐标 (0-{size-1}): ", 0, size-1)
    
    # 选择求解方法
    print("\n选择求解方法:")
    print("1. Warnsdorff启发式算法 (快速，适合大棋盘)")
    print("2. 回溯算法 (完整搜索，适合小棋盘)")
    
    method_choice = get_valid_input("请选择方法 (1 或 2): ", 1, 2)
    method = 'warnsdorff' if method_choice == 1 else 'backtrack'
    
    # 创建求解器并求解
    print(f"\n正在求解 {size}x{size} 棋盘上的骑士巡游问题...")
    print(f"起点: ({start_x}, {start_y})")
    if end_x is not None and end_y is not None:
        print(f"终点: ({end_x}, {end_y})")
    print(f"使用方法: {'Warnsdorff启发式' if method == 'warnsdorff' else '回溯算法'}")
    
    knight = KnightTour(size)
    
    if method == 'warnsdorff':
        path = knight.solve_warnsdorff(start_x, start_y, end_x, end_y)
    else:
        path = knight.solve_backtrack(start_x, start_y, end_x, end_y)
    
    if path:
        print(f"\n✓ 找到路径! 总共 {len(path)} 步")
        
        # 显示路径前几步和后几步
        if len(path) <= 10:
            print("完整路径:", " -> ".join([f"({x},{y})" for x, y in path]))
        else:
            path_str = " -> ".join([f"({x},{y})" for x, y in path[:5]])
            path_str += " -> ... -> "
            path_str += " -> ".join([f"({x},{y})" for x, y in path[-5:]])
            print("路径:", path_str)
        
        # 生成图片
        filename = f"knight_tour_{size}x{size}_{start_x}{start_y}.png"
        knight.generate_image(path, filename)
        print(f"\n图片已生成: {filename}")
        
        # 显示是否覆盖了整个棋盘
        if len(path) == size * size:
            print("✓ 成功访问了棋盘上的所有格子!")
        else:
            print(f"访问了 {len(path)}/{size*size} 个格子")
            
    else:
        print("\n✗ 未找到有效路径")
        if method == 'warnsdorff':
            print("提示: 可以尝试使用回溯算法，或者更换起点/终点位置")

if __name__ == "__main__":
    main()