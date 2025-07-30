'''
Author: LinYiHan
Date: 2025-01-16
Description: 图片提取器测试脚本
Version: 1.0
'''
from image_extractor import ImageExtractor
import logging

# 设置更详细的日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def test_extractor():
    """测试图片提取器"""
    # 创建提取器
    extractor = ImageExtractor()
    
    # 测试网址列表
    test_urls = [
        "https://www.baidu.com",
        "https://www.qq.com", 
        "https://www.163.com",
        "https://www.sina.com.cn"
    ]
    
    print("=== 图片提取器测试 ===")
    
    for url in test_urls:
        print(f"\n正在测试: {url}")
        try:
            image_urls = extractor.extract_image_urls(url, include_data_urls=True)
            
            if image_urls:
                print(f"✅ 成功提取到 {len(image_urls)} 个图片链接")
                print("前5个链接:")
                for i, img_url in enumerate(image_urls[:5], 1):
                    print(f"  {i}. {img_url}")
                
                if len(image_urls) > 5:
                    print(f"  ... 还有 {len(image_urls) - 5} 个链接")
            else:
                print("❌ 未提取到任何图片链接")
                
        except Exception as e:
            print(f"❌ 测试失败: {e}")

def test_specific_url():
    """测试特定网址"""
    extractor = ImageExtractor()
    
    url = input("请输入要测试的网址: ").strip()
    if not url:
        print("网址不能为空！")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n正在测试: {url}")
    
    try:
        image_urls = extractor.extract_image_urls(url, include_data_urls=True)
        
        if image_urls:
            print(f"✅ 成功提取到 {len(image_urls)} 个图片链接")
            print("\n所有图片链接:")
            for i, img_url in enumerate(image_urls, 1):
                print(f"{i}. {img_url}")
            
            # 保存到文件
            save = input("\n是否保存到文件？(y/n): ").lower().strip()
            if save == 'y':
                filename = f"test_{url.replace('://', '_').replace('/', '_').replace('.', '_')}.txt"
                extractor.save_urls_to_file(image_urls, filename)
                print(f"已保存到: {filename}")
        else:
            print("❌ 未提取到任何图片链接")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("选择测试模式:")
    print("1. 批量测试预设网址")
    print("2. 测试特定网址")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        test_extractor()
    elif choice == "2":
        test_specific_url()
    else:
        print("无效选择，使用批量测试")
        test_extractor() 