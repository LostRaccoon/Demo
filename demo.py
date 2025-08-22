#!/usr/bin/env python3
"""
骑士巡游问题演示脚本
展示不同大小棋盘的骑士巡游解决方案
"""

from knight_tour import KnightTour
import os

def demo_knight_tour():
    """演示不同配置的骑士巡游"""
    
    print("=== 骑士巡游问题演示 ===\n")
    
    # 测试用例列表
    test_cases = [
        {"size": 5, "start": (0, 0), "end": None, "method": "warnsdorff", "desc": "5x5棋盘，从(0,0)开始"},
        {"size": 6, "start": (2, 2), "end": (5, 5), "method": "warnsdorff", "desc": "6x6棋盘，从(2,2)到(5,5)"},
        {"size": 8, "start": (0, 0), "end": None, "method": "warnsdorff", "desc": "8x8棋盘，从(0,0)开始"},
        {"size": 4, "start": (0, 0), "end": (3, 3), "method": "backtrack", "desc": "4x4棋盘，从(0,0)到(3,3)，使用回溯算法"}
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"测试 {i}: {case['desc']}")
        print(f"棋盘大小: {case['size']}x{case['size']}")
        print(f"起点: {case['start']}")
        if case['end']:
            print(f"终点: {case['end']}")
        print(f"算法: {case['method']}")
        
        # 创建求解器
        knight = KnightTour(case['size'])
        
        # 求解
        if case['method'] == 'warnsdorff':
            path = knight.solve_warnsdorff(case['start'][0], case['start'][1], 
                                         case['end'][0] if case['end'] else None, 
                                         case['end'][1] if case['end'] else None)
        else:
            path = knight.solve_backtrack(case['start'][0], case['start'][1], 
                                        case['end'][0] if case['end'] else None, 
                                        case['end'][1] if case['end'] else None)
        
        if path:
            print(f"✓ 成功找到路径! 总共 {len(path)} 步")
            
            # 生成图片
            filename = f"demo_case_{i}_{case['size']}x{case['size']}.png"
            knight.generate_image(path, filename)
            
            results.append({
                'case': i,
                'success': True,
                'steps': len(path),
                'filename': filename,
                'complete': len(path) == case['size'] * case['size']
            })
            
            if len(path) == case['size'] * case['size']:
                print("✓ 完整巡游：访问了所有格子!")
            else:
                print(f"部分巡游：访问了 {len(path)}/{case['size']*case['size']} 个格子")
        else:
            print("✗ 未找到有效路径")
            results.append({
                'case': i,
                'success': False,
                'steps': 0,
                'filename': None,
                'complete': False
            })
        
        print("-" * 50)
    
    # 总结结果
    print("\n=== 测试总结 ===")
    successful = sum(1 for r in results if r['success'])
    complete_tours = sum(1 for r in results if r['complete'])
    
    print(f"总测试用例: {len(test_cases)}")
    print(f"成功求解: {successful}")
    print(f"完整巡游: {complete_tours}")
    print(f"生成图片: {successful}")
    
    print("\n生成的图片文件:")
    for result in results:
        if result['filename']:
            print(f"  - {result['filename']} ({result['steps']} 步)")


if __name__ == "__main__":
    demo_knight_tour()