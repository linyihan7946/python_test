'''
Author: LinYiHan
Date: 2025-01-16
Description: 图片提取器使用示例
Version: 1.0
'''
from image_extractor import ImageExtractor

def example_usage():
    """使用示例"""
    # 创建图片提取器
    extractor = ImageExtractor()
    
    # 示例网址
    test_url = "https://www.example.com"
    
    print("=== 图片链接提取器使用示例 ===")
    print(f"目标网址: {test_url}")
    
    try:
        # 提取图片链接
        image_urls = extractor.extract_image_urls(test_url)
        
        if image_urls:
            print(f"\n找到 {len(image_urls)} 个图片链接:")
            for i, url in enumerate(image_urls[:5], 1):  # 只显示前5个
                print(f"{i}. {url}")
            
            if len(image_urls) > 5:
                print(f"... 还有 {len(image_urls) - 5} 个链接")
            
            # 保存到文件
            extractor.save_urls_to_file(image_urls, 'example_images.txt')
        else:
            print("未找到任何图片链接")
            
    except Exception as e:
        print(f"提取过程中发生错误: {e}")

def custom_usage():
    """自定义使用示例"""
    # 自定义请求头
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # 创建自定义提取器
    extractor = ImageExtractor(timeout=15, headers=custom_headers)
    
    # 使用示例
    url = input("请输入要提取图片的网址: ").strip()
    
    if not url:
        print("网址不能为空！")
        return
    
    # 确保URL有协议
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        print(f"正在提取 {url} 中的图片链接...")
        image_urls = extractor.extract_image_urls(url, include_data_urls=True)
        
        if image_urls:
            print(f"\n找到 {len(image_urls)} 个图片链接:")
            for i, url in enumerate(image_urls, 1):
                print(f"{i}. {url}")
            
            # 保存到文件
            filename = input("\n请输入保存文件名 (默认: custom_images.txt): ").strip()
            if not filename:
                filename = 'custom_images.txt'
            
            extractor.save_urls_to_file(image_urls, filename)
        else:
            print("未找到任何图片链接")
            
    except Exception as e:
        print(f"提取过程中发生错误: {e}")

if __name__ == "__main__":
    print("选择使用模式:")
    print("1. 示例模式 (使用预设网址)")
    print("2. 自定义模式 (输入网址)")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        example_usage()
    elif choice == "2":
        custom_usage()
    else:
        print("无效选择，使用自定义模式")
        custom_usage() 