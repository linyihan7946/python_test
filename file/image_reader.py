'''
Author: LinYiHan
Date: 2025-01-16
Description: 图片路径读取器
Version: 1.0
'''
import os
import glob
from typing import List, Optional
import logging

# 获取用户输入的目录路径
directory = "E:\图片\自然风光-高度1920"
# 图片路径前缀
prefix = "https://linyihan-1312729243.cos.ap-guangzhou.myqcloud.com/%E8%87%AA%E7%84%B6%E9%A3%8E%E5%85%89-%E9%AB%98%E5%BA%A61920/"

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageReader:
    """图片路径读取器"""
    
    def __init__(self):
        """初始化图片读取器"""
        # 支持的图片格式
        self.image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
            '.webp', '.svg', '.ico', '.tiff', '.tif',
            '.jfif', '.pjpeg', '.pjp', '.avif'
        }
    
    def get_image_paths(self, directory_path: str) -> List[str]:
        """
        获取指定目录下的所有图片路径
        
        Args:
            directory_path (str): 目录路径
            recursive (bool): 是否递归搜索子目录
            
        Returns:
            List[str]: 图片路径列表
        """
        if not os.path.exists(directory_path):
            logger.error(f"目录不存在: {directory_path}")
            return []
        
        if not os.path.isdir(directory_path):
            logger.error(f"路径不是目录: {directory_path}")
            return []
        
        image_paths = []
        image_names = []
        
        try:
            # 只搜索当前目录
            logger.info(f"正在搜索目录: {directory_path}")
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path) and self._is_image_file(file):
                    image_paths.append(file_path)
                    image_names.append(prefix + file)

            # 按文件名排序
            image_paths.sort()
            logger.info(f"总共找到 {len(image_paths)} 个图片文件")
            
        except Exception as e:
            logger.error(f"搜索图片时发生错误: {e}")
        
        return image_names
    
    def _is_image_file(self, filename: str) -> bool:
        """
        检查文件是否为图片文件
        
        Args:
            filename (str): 文件名
            
        Returns:
            bool: 是否为图片文件
        """
        if not filename:
            return False
        
        # 获取文件扩展名
        ext = os.path.splitext(filename)[1].lower()
        
        # 检查是否为支持的图片格式
        return ext in self.image_extensions
    
    def get_image_info(self, image_paths: List[str]) -> List[dict]:
        """
        获取图片文件的详细信息
        
        Args:
            image_paths (List[str]): 图片路径列表
            
        Returns:
            List[dict]: 图片信息列表
        """
        image_info = []
        
        for path in image_paths:
            try:
                stat = os.stat(path)
                info = {
                    'path': path,
                    'filename': os.path.basename(path),
                    'extension': os.path.splitext(path)[1].lower(),
                    'size': stat.st_size,  # 文件大小（字节）
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),  # 文件大小（MB）
                    'created_time': stat.st_ctime,
                    'modified_time': stat.st_mtime,
                    'directory': os.path.dirname(path)
                }
                image_info.append(info)
            except Exception as e:
                logger.error(f"获取文件信息失败 {path}: {e}")
        
        return image_info
    
    def save_paths_to_file(self, image_paths: List[str], filename: str = 'image_paths.txt'):
        """
        将图片路径保存到文件
        
        Args:
            image_paths (List[str]): 图片路径列表
            filename (str): 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for path in image_paths:
                    f.write('"' + path + '",' + '\n')
            logger.info(f"图片路径已保存到文件: {filename}")
        except Exception as e:
            logger.error(f"保存文件失败: {e}")

def main():
    """主函数示例"""
    reader = ImageReader()
    
    print("=== 图片路径读取器 ===")
    
    if not directory:
        print("目录路径不能为空！")
        return
    
    if not os.path.exists(directory):
        print(f"目录不存在: {directory}")
        return
    
    try:
        image_paths = reader.get_image_paths(directory)
        
        if image_paths:
            print(f"\n找到 {len(image_paths)} 个图片文件:")
            for i, path in enumerate(image_paths, 1):
                print(f"{i}. {path}")
            
            # 保存到文件
            filename = 'file/image_paths.txt'
            reader.save_paths_to_file(image_paths, filename)
        else:
            print("未找到任何图片文件")
            
    except Exception as e:
        print(f"搜索过程中发生错误: {e}")

if __name__ == "__main__":
    main() 