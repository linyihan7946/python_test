'''
Author: LinYiHan
Date: 2025-01-16
Description: 网页图片链接提取器
Version: 1.1
'''
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageExtractor:
    """网页图片链接提取器"""
    
    def __init__(self, timeout=10, headers=None):
        """
        初始化图片提取器
        
        Args:
            timeout (int): 请求超时时间（秒）
            headers (dict): 请求头信息
        """
        self.timeout = timeout
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page_content(self, url):
        """
        获取网页内容
        
        Args:
            url (str): 目标网址
            
        Returns:
            str: 网页HTML内容
        """
        try:
            logger.info(f"正在获取网页内容: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            logger.info(f"网页编码: {response.encoding}")
            logger.info(f"响应状态码: {response.status_code}")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"获取网页内容失败: {e}")
            return None
    
    def extract_image_urls(self, url, include_data_urls=False):
        """
        提取网页中的所有图片链接
        
        Args:
            url (str): 目标网址
            include_data_urls (bool): 是否包含data URL格式的图片
            
        Returns:
            list: 图片链接列表
        """
        html_content = self.get_page_content(url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        image_urls = []
        
        # 查找所有img标签
        img_tags = soup.find_all('img')
        logger.info(f"找到 {len(img_tags)} 个img标签")
        
        for i, img in enumerate(img_tags):
            logger.debug(f"处理第 {i+1} 个img标签: {img}")
            
            # 获取所有可能的图片属性
            image_attrs = ['src', 'data-src', 'data-original', 'data-lazy-src', 'data-srcset', 'data-original-src']
            
            for attr in image_attrs:
                value = img.get(attr)
                if value:
                    logger.debug(f"找到属性 {attr}: {value}")
                    # 转换为绝对URL
                    absolute_url = urljoin(url, value.strip())
                    if self._is_valid_image_url(absolute_url, include_data_urls):
                        image_urls.append(absolute_url)
                        logger.debug(f"添加图片URL: {absolute_url}")
            
            # 获取srcset属性（响应式图片）
            srcset = img.get('srcset')
            if srcset:
                logger.debug(f"处理srcset: {srcset}")
                urls = self._parse_srcset(srcset, url)
                image_urls.extend(urls)
        
        # 查找CSS背景图片
        css_images = self._extract_css_images(html_content, url)
        image_urls.extend(css_images)
        
        # 查找picture标签中的source
        picture_images = self._extract_picture_images(soup, url)
        image_urls.extend(picture_images)
        
        # 查找链接中的图片
        link_images = self._extract_link_images(soup, url)
        image_urls.extend(link_images)
        
        # 查找JavaScript中的图片URL
        js_images = self._extract_js_images(html_content, url)
        image_urls.extend(js_images)
        
        # 去重并返回
        unique_urls = list(set(image_urls))
        logger.info(f"总共提取到 {len(unique_urls)} 个唯一图片链接")
        
        return unique_urls
    
    def _is_valid_image_url(self, url, include_data_urls=False):
        """
        检查是否为有效的图片URL
        
        Args:
            url (str): 图片URL
            include_data_urls (bool): 是否包含data URL
            
        Returns:
            bool: 是否为有效图片URL
        """
        if not url:
            return False
        
        # 检查data URL
        if url.startswith('data:image/'):
            return include_data_urls
        
        # 检查常见图片扩展名
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif']
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        # 检查文件扩展名
        has_extension = any(path.endswith(ext) for ext in image_extensions)
        
        # 检查URL中是否包含图片相关关键词
        image_keywords = ['image', 'img', 'photo', 'picture', 'avatar', 'icon', 'logo']
        has_keyword = any(keyword in url.lower() for keyword in image_keywords)
        
        # 检查URL参数中是否包含图片相关参数
        query_params = ['image', 'img', 'photo', 'picture', 'avatar', 'icon', 'logo']
        has_param = any(param in parsed_url.query.lower() for param in query_params)
        
        # 如果URL包含图片关键词或参数，也认为是有效的
        return has_extension or has_keyword or has_param
    
    def _parse_srcset(self, srcset, base_url):
        """
        解析srcset属性
        
        Args:
            srcset (str): srcset属性值
            base_url (str): 基础URL
            
        Returns:
            list: 图片URL列表
        """
        urls = []
        # 简单的srcset解析
        parts = srcset.split(',')
        for part in parts:
            part = part.strip()
            if part:
                # 提取URL部分（去除宽度描述符）
                url_part = part.split()[0]
                absolute_url = urljoin(base_url, url_part)
                if self._is_valid_image_url(absolute_url):
                    urls.append(absolute_url)
                    logger.debug(f"从srcset添加URL: {absolute_url}")
        return urls
    
    def _extract_css_images(self, html_content, base_url):
        """
        从CSS中提取背景图片
        
        Args:
            html_content (str): HTML内容
            base_url (str): 基础URL
            
        Returns:
            list: 图片URL列表
        """
        urls = []
        # 查找CSS中的背景图片
        css_patterns = [
            r'background(?:-image)?\s*:\s*url\(["\']?([^"\')\s]+)["\']?\)',
            r'background\s*:\s*url\(["\']?([^"\')\s]+)["\']?\)',
            r'content\s*:\s*url\(["\']?([^"\')\s]+)["\']?\)',
        ]
        
        for pattern in css_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                absolute_url = urljoin(base_url, match)
                if self._is_valid_image_url(absolute_url):
                    urls.append(absolute_url)
                    logger.debug(f"从CSS添加URL: {absolute_url}")
        
        return urls
    
    def _extract_picture_images(self, soup, base_url):
        """
        从picture标签中提取图片
        
        Args:
            soup (BeautifulSoup): BeautifulSoup对象
            base_url (str): 基础URL
            
        Returns:
            list: 图片URL列表
        """
        urls = []
        picture_tags = soup.find_all('picture')
        logger.info(f"找到 {len(picture_tags)} 个picture标签")
        
        for picture in picture_tags:
            # 查找source标签
            sources = picture.find_all('source')
            for source in sources:
                srcset = source.get('srcset')
                if srcset:
                    urls.extend(self._parse_srcset(srcset, base_url))
            
            # 查找img标签
            img = picture.find('img')
            if img:
                src = img.get('src')
                if src:
                    absolute_url = urljoin(base_url, src.strip())
                    if self._is_valid_image_url(absolute_url):
                        urls.append(absolute_url)
        
        return urls
    
    def _extract_link_images(self, soup, base_url):
        """
        从链接中提取图片
        
        Args:
            soup (BeautifulSoup): BeautifulSoup对象
            base_url (str): 基础URL
            
        Returns:
            list: 图片URL列表
        """
        urls = []
        # 查找可能指向图片的链接
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            if href and self._is_valid_image_url(href):
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
                logger.debug(f"从链接添加URL: {absolute_url}")
        
        return urls
    
    def _extract_js_images(self, html_content, base_url):
        """
        从JavaScript中提取图片URL
        
        Args:
            html_content (str): HTML内容
            base_url (str): 基础URL
            
        Returns:
            list: 图片URL列表
        """
        urls = []
        # 查找JavaScript中的图片URL
        js_patterns = [
            r'["\']([^"\']*\.(?:jpg|jpeg|png|gif|bmp|webp|svg|ico))["\']',
            r'["\']([^"\']*image[^"\']*)["\']',
            r'["\']([^"\']*img[^"\']*)["\']',
        ]
        
        for pattern in js_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                absolute_url = urljoin(base_url, match)
                if self._is_valid_image_url(absolute_url):
                    urls.append(absolute_url)
                    logger.debug(f"从JS添加URL: {absolute_url}")
        
        return urls
    
    def save_urls_to_file(self, urls, filename='image_urls.txt'):
        """
        将图片链接保存到文件
        
        Args:
            urls (list): 图片链接列表
            filename (str): 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for url in urls:
                    f.write(url + '\n')
            logger.info(f"图片链接已保存到文件: {filename}")
        except Exception as e:
            logger.error(f"保存文件失败: {e}")

def main():
    """主函数示例"""
    # 创建图片提取器
    extractor = ImageExtractor()
    
    # 获取用户输入的网址
    url = input("请输入要提取图片的网址: ").strip()
    
    if not url:
        print("网址不能为空！")
        return
    
    # 确保URL有协议
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        # 提取图片链接
        print(f"正在提取 {url} 中的图片链接...")
        image_urls = extractor.extract_image_urls(url, include_data_urls=True)
        
        if image_urls:
            print(f"\n找到 {len(image_urls)} 个图片链接:")
            for i, url in enumerate(image_urls, 1):
                print(f"{i}. {url}")
            
            # 保存到文件
            save_to_file = input("\n是否保存到文件？(y/n): ").lower().strip()
            if save_to_file == 'y':
                filename = input("请输入文件名 (默认: image_urls.txt): ").strip()
                if not filename:
                    filename = 'image_urls.txt'
                extractor.save_urls_to_file(image_urls, filename)
        else:
            print("未找到任何图片链接")
            print("可能的原因:")
            print("1. 网页需要JavaScript渲染")
            print("2. 网站有反爬虫机制")
            print("3. 图片使用了特殊的加载方式")
            print("4. 网络连接问题")
            
    except Exception as e:
        print(f"提取过程中发生错误: {e}")

if __name__ == "__main__":
    main() 