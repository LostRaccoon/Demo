#!/usr/bin/env python3
"""
骑士巡游问题求解器
给定棋盘大小和起点终点，生成骑士移动路径并输出图片
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque
import argparse
import sys

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

class KnightTour:
    def __init__(self, board_size):
        self.size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                     (1, 2), (1, -2), (-1, 2), (-1, -2)]
    
    def is_valid_move(self, x, y, visited):
        """检查移动是否有效"""
        return (0 <= x < self.size and 0 <= y < self.size and 
                not visited[x][y])
    
    def get_degree(self, x, y, visited):
        """获取位置的度数（可访问的邻居数量）"""
        count = 0
        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny, visited):
                count += 1
        return count
    
    def solve_warnsdorff(self, start_x, start_y, end_x=None, end_y=None):
        """使用Warnsdorff规则求解骑士巡游"""
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]
        path = []
        
        # 从起点开始
        x, y = start_x, start_y
        visited[x][y] = True
        path.append((x, y))
        
        move_count = 1
        
        while move_count < self.size * self.size:
            # 如果指定了终点，且当前只剩一步，检查是否能到达终点
            if (end_x is not None and end_y is not None and 
                move_count == self.size * self.size - 1):
                for dx, dy in self.moves:
                    nx, ny = x + dx, y + dy
                    if nx == end_x and ny == end_y and self.is_valid_move(nx, ny, visited):
                        visited[nx][ny] = True
                        path.append((nx, ny))
                        move_count += 1
                        break
                break
            
            # 找到所有可能的下一步
            next_moves = []
            for dx, dy in self.moves:
                nx, ny = x + dx, y + dy
                if self.is_valid_move(nx, ny, visited):
                    degree = self.get_degree(nx, ny, visited)
                    next_moves.append((degree, nx, ny))
            
            if not next_moves:
                break
            
            # 按度数排序，选择度数最小的位置（Warnsdorff规则）
            next_moves.sort()
            _, x, y = next_moves[0]
            
            visited[x][y] = True
            path.append((x, y))
            move_count += 1
        
        return path
    
    def solve_backtrack(self, start_x, start_y, end_x=None, end_y=None):
        """使用回溯算法求解骑士巡游"""
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]
        path = []
        
        def backtrack(x, y, move_count):
            visited[x][y] = True
            path.append((x, y))
            
            # 如果访问了所有格子
            if move_count == self.size * self.size:
                # 如果没有指定终点，或者当前位置就是终点
                if end_x is None or (x == end_x and y == end_y):
                    return True
                else:
                    path.pop()
                    visited[x][y] = False
                    return False
            
            # 如果指定了终点，且这是最后一步，检查是否能到达终点
            if (end_x is not None and end_y is not None and 
                move_count == self.size * self.size - 1):
                for dx, dy in self.moves:
                    nx, ny = x + dx, y + dy
                    if nx == end_x and ny == end_y and self.is_valid_move(nx, ny, visited):
                        visited[nx][ny] = True
                        path.append((nx, ny))
                        return True
                path.pop()
                visited[x][y] = False
                return False
            
            # 尝试所有可能的移动
            for dx, dy in self.moves:
                nx, ny = x + dx, y + dy
                if self.is_valid_move(nx, ny, visited):
                    if backtrack(nx, ny, move_count + 1):
                        return True
            
            # 回溯
            path.pop()
            visited[x][y] = False
            return False
        
        if backtrack(start_x, start_y, 1):
            return path
        else:
            return None
    
    def generate_image(self, path, filename="knight_tour.png"):
        """生成骑士巡游路径图片"""
        if not path:
            print("没有找到有效路径")
            return
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 绘制棋盘
        for i in range(self.size):
            for j in range(self.size):
                color = 'lightgray' if (i + j) % 2 == 0 else 'white'
                rect = patches.Rectangle((j, self.size - 1 - i), 1, 1, 
                                       linewidth=1, edgecolor='black', 
                                       facecolor=color)
                ax.add_patch(rect)
        
        # 填充移动序号
        for idx, (x, y) in enumerate(path, 1):
            # 在格子中央显示序号
            ax.text(y + 0.5, self.size - 1 - x + 0.5, str(idx),
                   ha='center', va='center', fontsize=12, fontweight='bold',
                   color='red')
        
        # 绘制移动路径
        if len(path) > 1:
            path_x = [y + 0.5 for x, y in path]
            path_y = [self.size - 1 - x + 0.5 for x, y in path]
            ax.plot(path_x, path_y, 'b-', linewidth=2, alpha=0.7)
            
            # 标记起点和终点
            ax.plot(path_x[0], path_y[0], 'go', markersize=10, label='Start')
            ax.plot(path_x[-1], path_y[-1], 'ro', markersize=10, label='End')
        
        # 设置图形属性
        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_aspect('equal')
        ax.set_xticks(range(self.size + 1))
        ax.set_yticks(range(self.size + 1))
        ax.grid(True)
        ax.legend()
        
        # 添加标题
        title = f"Knight's Tour Path ({self.size}x{self.size} Board)"
        if path:
            start = path[0]
            end = path[-1]
            title += f"\nStart: ({start[0]}, {start[1]}) -> End: ({end[0]}, {end[1]})"
        plt.title(title, fontsize=14, fontweight='bold')
        
        # 保存图片
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"图片已保存为: {filename}")


def main():
    parser = argparse.ArgumentParser(description='骑士巡游问题求解器')
    parser.add_argument('size', type=int, help='棋盘大小 (size x size)')
    parser.add_argument('start_x', type=int, help='起点X坐标 (0-based)')
    parser.add_argument('start_y', type=int, help='起点Y坐标 (0-based)')
    parser.add_argument('--end_x', type=int, help='终点X坐标 (可选)')
    parser.add_argument('--end_y', type=int, help='终点Y坐标 (可选)')
    parser.add_argument('--method', choices=['warnsdorff', 'backtrack'], 
                       default='warnsdorff', help='求解方法')
    parser.add_argument('--output', default='knight_tour.png', help='输出图片文件名')
    
    args = parser.parse_args()
    
    # 验证输入
    if not (0 <= args.start_x < args.size and 0 <= args.start_y < args.size):
        print(f"错误: 起点坐标超出棋盘范围 (0, 0) 到 ({args.size-1}, {args.size-1})")
        sys.exit(1)
    
    if args.end_x is not None and args.end_y is not None:
        if not (0 <= args.end_x < args.size and 0 <= args.end_y < args.size):
            print(f"错误: 终点坐标超出棋盘范围 (0, 0) 到 ({args.size-1}, {args.size-1})")
            sys.exit(1)
    
    # 创建骑士巡游求解器
    knight = KnightTour(args.size)
    
    print(f"正在求解 {args.size}x{args.size} 棋盘上的骑士巡游问题...")
    print(f"起点: ({args.start_x}, {args.start_y})")
    if args.end_x is not None and args.end_y is not None:
        print(f"终点: ({args.end_x}, {args.end_y})")
    print(f"使用方法: {args.method}")
    
    # 求解
    if args.method == 'warnsdorff':
        path = knight.solve_warnsdorff(args.start_x, args.start_y, args.end_x, args.end_y)
    else:
        path = knight.solve_backtrack(args.start_x, args.start_y, args.end_x, args.end_y)
    
    if path:
        print(f"找到路径! 总共 {len(path)} 步")
        print("路径:", " -> ".join([f"({x},{y})" for x, y in path]))
        
        # 生成图片
        knight.generate_image(path, args.output)
    else:
        print("未找到有效路径")


if __name__ == "__main__":
    main()