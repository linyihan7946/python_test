'''
Author: LinYiHan
Date: 2025-01-16
Description: 图片裁剪工具 - 将图片裁剪为1080*1920尺寸
Version: 1.0
'''
import os
import glob
from PIL import Image
import logging
from typing import List, Tuple
import shutil

source_dir = 'E:/图片/自然风光-高度1920'
output_dir = 'E:/图片/自然风光-1080x1920'

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageCropper:
    """图片裁剪器"""
    
    def __init__(self, target_width: int = 1080, target_height: int = 1920):
        """
        初始化图片裁剪器
        
        Args:
            target_width (int): 目标宽度
            target_height (int): 目标高度
        """
        self.target_width = target_width
        self.target_height = target_height
        
        # 支持的图片格式
        self.image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
            '.webp', '.tiff', '.tif'
        }
    
    def get_image_files(self, source_directory: str) -> List[str]:
        """
        获取指定目录下的所有图片文件
        
        Args:
            source_directory (str): 源目录路径
            
        Returns:
            List[str]: 图片文件路径列表
        """
        if not os.path.exists(source_directory):
            logger.error(f"源目录不存在: {source_directory}")
            return []
        
        if not os.path.isdir(source_directory):
            logger.error(f"路径不是目录: {source_directory}")
            return []
        
        image_files = []
        
        try:
            logger.info(f"正在扫描目录: {source_directory}")
            for file in os.listdir(source_directory):
                file_path = os.path.join(source_directory, file)
                if os.path.isfile(file_path) and self._is_image_file(file):
                    image_files.append(file_path)
            
            # 按文件名排序
            image_files.sort()
            logger.info(f"找到 {len(image_files)} 个图片文件")
            
        except Exception as e:
            logger.error(f"扫描目录时发生错误: {e}")
        
        return image_files
    
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
    
    def calculate_crop_box(self, image_width: int, image_height: int) -> Tuple[int, int, int, int]:
        """
        计算裁剪框的位置
        
        Args:
            image_width (int): 原图宽度
            image_height (int): 原图高度
            
        Returns:
            Tuple[int, int, int, int]: 裁剪框坐标 (left, top, right, bottom)
        """
        # 计算水平方向的中心位置
        center_x = image_width // 2
        
        # 计算裁剪框的左右边界
        left = center_x - (self.target_width // 2)
        right = center_x + (self.target_width // 2)
        
        # 如果裁剪框超出图片边界，进行调整
        if left < 0:
            left = 0
            right = self.target_width
        elif right > image_width:
            right = image_width
            left = image_width - self.target_width
        
        # 垂直方向从顶部开始裁剪
        top = 0
        bottom = self.target_height
        
        # 如果图片高度不够，调整裁剪高度
        if bottom > image_height:
            bottom = image_height
            top = max(0, image_height - self.target_height)
        
        return (left, top, right, bottom)
    
    def crop_image(self, image_path: str, output_path: str) -> bool:
        """
        裁剪单张图片
        
        Args:
            image_path (str): 输入图片路径
            output_path (str): 输出图片路径
            
        Returns:
            bool: 是否成功
        """
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 转换为RGB模式（处理RGBA等其他模式）
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 获取图片尺寸
                width, height = img.size
                logger.debug(f"原图尺寸: {width}x{height}")
                
                # 检查图片尺寸是否满足要求
                if height < self.target_height:
                    logger.warning(f"图片高度不足: {image_path} (高度: {height}, 需要: {self.target_height})")
                    # 可以选择跳过或调整目标高度
                    return False
                
                if width < self.target_width:
                    logger.warning(f"图片宽度不足: {image_path} (宽度: {width}, 需要: {self.target_width})")
                    return False
                
                # 计算裁剪框
                crop_box = self.calculate_crop_box(width, height)
                logger.debug(f"裁剪框: {crop_box}")
                
                # 裁剪图片
                cropped_img = img.crop(crop_box)
                
                # 确保输出目录存在
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # 保存裁剪后的图片
                cropped_img.save(output_path, quality=95, optimize=True)
                logger.info(f"成功裁剪: {os.path.basename(image_path)} -> {os.path.basename(output_path)}")
                
                return True
                
        except Exception as e:
            logger.error(f"裁剪图片失败 {image_path}: {e}")
            return False
    
    def batch_crop_images(self, source_directory: str, output_directory: str) -> dict:
        """
        批量裁剪图片
        
        Args:
            source_directory (str): 源目录路径
            output_directory (str): 输出目录路径
            
        Returns:
            dict: 处理结果统计
        """
        # 获取所有图片文件
        image_files = self.get_image_files(source_directory)
        
        if not image_files:
            logger.warning("未找到任何图片文件")
            return {'total': 0, 'success': 0, 'failed': 0, 'skipped': 0}
        
        # 确保输出目录存在
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            logger.info(f"创建输出目录: {output_directory}")
        
        # 统计信息
        stats = {
            'total': len(image_files),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        logger.info(f"开始批量裁剪 {len(image_files)} 张图片...")
        
        for i, image_path in enumerate(image_files, 1):
            try:
                # 获取文件名
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                
                # 生成输出文件名（可以添加后缀）
                output_filename = f"{name}{ext}"
                output_path = os.path.join(output_directory, output_filename)
                
                logger.info(f"处理第 {i}/{len(image_files)} 张图片: {filename}")
                
                # 裁剪图片
                if self.crop_image(image_path, output_path):
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
                    
            except Exception as e:
                logger.error(f"处理图片失败 {image_path}: {e}")
                stats['failed'] += 1
        
        # 输出统计结果
        logger.info(f"批量裁剪完成:")
        logger.info(f"  总计: {stats['total']}")
        logger.info(f"  成功: {stats['success']}")
        logger.info(f"  失败: {stats['failed']}")
        logger.info(f"  跳过: {stats['skipped']}")
        
        return stats
    
    def preview_crop(self, image_path: str, preview_path: str = None) -> bool:
        """
        预览裁剪效果（生成预览图）
        
        Args:
            image_path (str): 输入图片路径
            preview_path (str): 预览图输出路径
            
        Returns:
            bool: 是否成功
        """
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                width, height = img.size
                crop_box = self.calculate_crop_box(width, height)
                
                # 创建预览图（在原图上绘制裁剪框）
                preview_img = img.copy()
                
                # 这里可以添加绘制裁剪框的代码
                # 为了简化，直接裁剪并保存
                cropped_img = img.crop(crop_box)
                
                if preview_path is None:
                    name, ext = os.path.splitext(image_path)
                    preview_path = f"{name}_preview{ext}"
                
                cropped_img.save(preview_path, quality=95)
                logger.info(f"预览图已保存: {preview_path}")
                
                return True
                
        except Exception as e:
            logger.error(f"生成预览图失败: {e}")
            return False

def main():
    """主函数"""
    print("=== 图片裁剪工具 ===")
    print(f"目标尺寸: 1080x1920")
    
    # 获取用户输入
    
    
    if not source_dir or not output_dir:
        print("目录路径不能为空！")
        return
    
    if not os.path.exists(source_dir):
        print(f"源目录不存在: {source_dir}")
        return
    
    # 创建裁剪器
    cropper = ImageCropper(target_width=1080, target_height=1920)
    
    try:
        # 批量裁剪
        stats = cropper.batch_crop_images(source_dir, output_dir)
        
        print(f"\n处理完成:")
        print(f"  总计: {stats['total']} 张图片")
        print(f"  成功: {stats['success']} 张")
        print(f"  失败: {stats['failed']} 张")
        print(f"  跳过: {stats['skipped']} 张")
        
        if stats['success'] > 0:
            print(f"\n裁剪后的图片已保存到: {output_dir}")
        
    except Exception as e:
        print(f"处理过程中发生错误: {e}")

if __name__ == "__main__":
    main() 