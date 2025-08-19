'''
Author: LinYiHan
Date: 2025-01-16
Description: 图片水印去除工具 - 支持多个矩形范围
Version: 1.0
'''
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import logging
from typing import List, Tuple, Dict, Optional
import json

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WatermarkRemover:
    """图片水印去除器"""
    
    def __init__(self):
        """初始化水印去除器"""
        # 支持的图片格式
        self.image_extensions = {
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'
        }
    
    def remove_watermark_by_rectangles(self, image_path: str, output_path: str, 
                                     rectangles: List[Tuple[int, int, int, int]], 
                                     method: str = 'inpaint') -> bool:
        """
        通过指定矩形区域去除水印
        
        Args:
            image_path (str): 输入图片路径
            output_path (str): 输出图片路径
            rectangles (List[Tuple]): 矩形区域列表，每个矩形为 (x, y, width, height)
            method (str): 去除方法 ('inpaint', 'blur', 'fill', 'clone')
            
        Returns:
            bool: 是否成功
        """
        try:
            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                print("OpenCV读取失败，尝试PIL...")
                from PIL import Image
                import numpy as np
                pil_image = Image.open(image_path)
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                print(f"PIL读取成功，图片尺寸: {image.shape}")
            
            height, width = image.shape[:2]
            logger.info(f"图片尺寸: {width}x{height}")
            
            # 创建掩码
            mask = np.zeros((height, width), dtype=np.uint8)
            
            # 在掩码上绘制矩形区域
            for rect in rectangles:
                x, y, w, h = rect
                # 确保矩形在图片范围内
                x = max(0, min(x, width - 1))
                y = max(0, min(y, height - 1))
                w = min(w, width - x)
                h = min(h, height - y)
                
                if w > 0 and h > 0:
                    mask[y:y+h, x:x+w] = 255
                    logger.info(f"添加矩形区域: ({x}, {y}, {w}, {h})")
            
            # 根据方法处理水印
            if method == 'inpaint':
                result = self._inpaint_watermark(image, mask)
            elif method == 'blur':
                result = self._blur_watermark(image, mask, rectangles)
            elif method == 'fill':
                result = self._fill_watermark(image, mask, rectangles)
            elif method == 'clone':
                result = self._clone_watermark(image, mask, rectangles)
            else:
                logger.error(f"不支持的方法: {method}")
                return False
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 保存结果
            success = cv2.imwrite(output_path, result)
            if not success:
                try:
                    from PIL import Image
                    import numpy as np
                    # 转换BGR到RGB
                    rgb_result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(rgb_result)
                    pil_image.save(output_path)
                    logger.info(f"水印去除完成: {output_path}")
                    return True
                except Exception as e:
                    logger.error(f"去除水印失败: {e}")
                    return False
            else:
                logger.info(f"水印去除完成: {output_path}")
                return True
            
        except Exception as e:
            logger.error(f"去除水印失败: {e}")
            return False
    
    def _inpaint_watermark(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        使用图像修复算法去除水印
        
        Args:
            image (np.ndarray): 输入图片
            mask (np.ndarray): 掩码
            
        Returns:
            np.ndarray: 处理后的图片
        """
        # 使用TELEA算法进行图像修复
        result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
        logger.info("使用图像修复算法去除水印")
        return result
    
    def _blur_watermark(self, image: np.ndarray, mask: np.ndarray, 
                       rectangles: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        使用模糊方法去除水印
        
        Args:
            image (np.ndarray): 输入图片
            mask (np.ndarray): 掩码
            rectangles (List[Tuple]): 矩形区域列表
            
        Returns:
            np.ndarray: 处理后的图片
        """
        result = image.copy()
        
        for rect in rectangles:
            x, y, w, h = rect
            if w > 0 and h > 0:
                # 对矩形区域进行高斯模糊
                roi = result[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)
                result[y:y+h, x:x+w] = blurred_roi
        
        logger.info("使用模糊方法去除水印")
        return result
    
    def _fill_watermark(self, image: np.ndarray, mask: np.ndarray, 
                       rectangles: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        使用填充方法去除水印
        
        Args:
            image (np.ndarray): 输入图片
            mask (np.ndarray): 掩码
            rectangles (List[Tuple]): 矩形区域列表
            
        Returns:
            np.ndarray: 处理后的图片
        """
        result = image.copy()
        
        for rect in rectangles:
            x, y, w, h = rect
            if w > 0 and h > 0:
                # 计算周围区域的平均颜色
                surrounding_pixels = []
                
                # 收集周围像素
                for i in range(max(0, y-5), min(image.shape[0], y+h+5)):
                    for j in range(max(0, x-5), min(image.shape[1], x+w+5)):
                        if not (y <= i < y+h and x <= j < x+w):
                            surrounding_pixels.append(image[i, j])
                
                if surrounding_pixels:
                    # 计算平均颜色
                    avg_color = np.mean(surrounding_pixels, axis=0)
                    # 填充矩形区域
                    result[y:y+h, x:x+w] = avg_color.astype(np.uint8)
        
        logger.info("使用填充方法去除水印")
        return result
    
    def _clone_watermark(self, image: np.ndarray, mask: np.ndarray, 
                        rectangles: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        使用克隆方法去除水印
        
        Args:
            image (np.ndarray): 输入图片
            mask (np.ndarray): 掩码
            rectangles (List[Tuple]): 矩形区域列表
            
        Returns:
            np.ndarray: 处理后的图片
        """
        result = image.copy()
        
        for rect in rectangles:
            x, y, w, h = rect
            if w > 0 and h > 0:
                # 寻找最佳匹配区域
                best_match = self._find_best_match(image, x, y, w, h)
                if best_match:
                    src_x, src_y = best_match
                    # 复制匹配区域到水印位置
                    result[y:y+h, x:x+w] = image[src_y:src_y+h, src_x:src_x+w]
        
        logger.info("使用克隆方法去除水印")
        return result
    
    def _find_best_match(self, image: np.ndarray, x: int, y: int, w: int, h: int) -> Optional[Tuple[int, int]]:
        """
        寻找最佳匹配区域
        
        Args:
            image (np.ndarray): 输入图片
            x, y, w, h (int): 水印区域坐标和尺寸
            
        Returns:
            Optional[Tuple[int, int]]: 最佳匹配区域的坐标
        """
        height, width = image.shape[:2]
        best_score = float('inf')
        best_match = None
        
        # 在图片中搜索最佳匹配区域
        step = 10  # 搜索步长
        for i in range(0, height - h, step):
            for j in range(0, width - w, step):
                # 跳过水印区域本身
                if (y <= i < y+h and x <= j < x+w):
                    continue
                
                # 计算区域相似度（这里使用简单的颜色差异）
                region1 = image[y:y+h, x:x+w]
                region2 = image[i:i+h, j:j+w]
                
                if region1.shape == region2.shape:
                    diff = np.mean(np.abs(region1.astype(float) - region2.astype(float)))
                    if diff < best_score:
                        best_score = diff
                        best_match = (j, i)
        
        return best_match
    
    def batch_remove_watermarks(self, source_directory: str, output_directory: str, 
                               watermark_config: Dict) -> dict:
        """
        批量去除水印
        
        Args:
            source_directory (str): 源目录路径
            output_directory (str): 输出目录路径
            watermark_config (Dict): 水印配置，包含矩形区域和方法
            
        Returns:
            dict: 处理结果统计
        """
        # 获取所有图片文件
        image_files = self._get_image_files(source_directory)
        
        if not image_files:
            logger.warning("未找到任何图片文件")
            return {'total': 0, 'success': 0, 'failed': 0}
        
        # 确保输出目录存在
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            logger.info(f"创建输出目录: {output_directory}")
        
        # 统计信息
        stats = {
            'total': len(image_files),
            'success': 0,
            'failed': 0
        }
        
        logger.info(f"开始批量去除水印 {len(image_files)} 张图片...")
        
        for i, image_path in enumerate(image_files, 1):
            try:
                # 获取文件名
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                
                # 生成输出文件名
                output_filename = f"{name}_no_watermark{ext}"
                output_path = os.path.join(output_directory, output_filename)
                
                logger.info(f"处理第 {i}/{len(image_files)} 张图片: {filename}")
                
                # 去除水印
                rectangles = watermark_config.get('rectangles', [])
                method = watermark_config.get('method', 'inpaint')
                
                if self.remove_watermark_by_rectangles(image_path, output_path, rectangles, method):
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
                    
            except Exception as e:
                logger.error(f"处理图片失败 {image_path}: {e}")
                stats['failed'] += 1
        
        # 输出统计结果
        logger.info(f"批量去除水印完成:")
        logger.info(f"  总计: {stats['total']}")
        logger.info(f"  成功: {stats['success']}")
        logger.info(f"  失败: {stats['failed']}")
        
        return stats
    
    def _get_image_files(self, directory: str) -> List[str]:
        """
        获取指定目录下的所有图片文件
        
        Args:
            directory (str): 目录路径
            
        Returns:
            List[str]: 图片文件路径列表
        """
        if not os.path.exists(directory):
            logger.error(f"目录不存在: {directory}")
            return []
        
        image_files = []
        
        try:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
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
    
    def save_config(self, config: Dict, config_path: str):
        """
        保存水印配置到文件
        
        Args:
            config (Dict): 水印配置
            config_path (str): 配置文件路径
        """
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"配置已保存到: {config_path}")
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
    
    def load_config(self, config_path: str) -> Dict:
        """
        从文件加载水印配置
        
        Args:
            config_path (str): 配置文件路径
            
        Returns:
            Dict: 水印配置
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"配置已从文件加载: {config_path}")
            return config
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            return {}

def main():
    """主函数"""
    print("=== 图片水印去除工具 ===")
    
    # 创建水印去除器
    remover = WatermarkRemover()
    
    # 获取用户输入
    image_path = input("请输入图片路径: ").strip()
    output_path = input("请输入输出路径: ").strip()
    
    if not image_path or not output_path:
        print("路径不能为空！")
        return
    
    if not os.path.exists(image_path):
        print(f"图片不存在: {image_path}")
        return
    
    # 获取矩形区域
    print("\n请输入矩形区域 (格式: x,y,width,height)")
    print("输入 'done' 完成输入")
    
    rectangles = []
    while True:
        rect_input = input(f"矩形区域 {len(rectangles)+1}: ").strip()
        if rect_input.lower() == 'done':
            break
        
        try:
            x, y, w, h = map(int, rect_input.split(','))
            rectangles.append((x, y, w, h))
            print(f"已添加矩形: ({x}, {y}, {w}, {h})")
        except ValueError:
            print("格式错误，请使用 x,y,width,height 格式")
    
    if not rectangles:
        print("未输入任何矩形区域！")
        return
    
    # 选择去除方法
    print("\n选择去除方法:")
    print("1. inpaint (图像修复)")
    print("2. blur (模糊)")
    print("3. fill (填充)")
    print("4. clone (克隆)")
    
    method_choice = input("请选择 (1/2/3/4): ").strip()
    method_map = {'1': 'inpaint', '2': 'blur', '3': 'fill', '4': 'clone'}
    method = method_map.get(method_choice, 'inpaint')
    
    try:
        # 去除水印
        success = remover.remove_watermark_by_rectangles(image_path, output_path, rectangles, method)
        
        if success:
            print(f"✅ 水印去除成功: {output_path}")
        else:
            print("❌ 水印去除失败")
            
    except Exception as e:
        print(f"处理过程中发生错误: {e}")

if __name__ == "__main__":
    main()
