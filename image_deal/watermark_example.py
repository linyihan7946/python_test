'''
Author: LinYiHan
Date: 2025-01-16
Description: 水印去除工具使用示例
Version: 1.0
'''
from watermark_remover import WatermarkRemover
import os
import json

def example_usage(image_path, output_path, rectangles):
    """使用示例"""
    # 创建水印去除器
    remover = WatermarkRemover()
    
    # # 示例矩形区域（水印位置）
    # rectangles = [
    #     (100, 50, 200, 80),    # 左上角水印
    #     (800, 600, 150, 60),   # 右下角水印
    #     (400, 300, 100, 50)    # 中间水印
    # ]
    
    print("=== 水印去除工具使用示例 ===")
    print(f"输入图片: {image_path}")
    print(f"输出图片: {output_path}")
    print(f"水印区域: {rectangles}")
    
    if not os.path.exists(image_path):
        print(f"❌ 示例图片不存在: {image_path}")
        return
    
    try:
        # 使用图像修复方法去除水印
        success = remover.remove_watermark_by_rectangles(
            image_path, output_path, rectangles, method='inpaint'
        )
        
        if success:
            print(f"✅ 水印去除成功: {output_path}")
        else:
            print("❌ 水印去除失败")
            
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")

if __name__ == "__main__":
    print("=== 水印去除工具使用示例 ===")
    image_path = "E:\\临时目录\\带水印图片.png"
    output_path = "E:\\临时目录\\带水印图片-去水印.png"
    rectangles = [(784, 1498, 846, 1536)]
    example_usage(image_path, output_path, rectangles)
