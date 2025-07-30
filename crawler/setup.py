'''
Author: LinYiHan
Date: 2025-01-16
Description: 安装脚本
Version: 1.0
'''
import subprocess
import sys
import os

def install_requirements():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 图片提取器安装脚本 ===")
    
    # 检查requirements.txt是否存在
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt 文件不存在！")
        return
    
    # 安装依赖
    if install_requirements():
        print("\n安装完成！现在可以运行以下命令：")
        print("1. python image_extractor.py - 运行主程序")
        print("2. python test_extractor.py - 运行测试")
        print("3. python example.py - 运行示例")
    else:
        print("\n安装失败，请手动安装依赖包：")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main() 