# 网页图片链接提取器

这是一个用于从网页中提取所有图片链接的Python工具。

## 功能特性

- 提取网页中的所有图片链接（img标签的src属性）
- 支持响应式图片（srcset属性）
- 支持懒加载图片（data-src属性）
- 提取CSS背景图片
- 自动转换为绝对URL
- 支持多种图片格式（jpg, jpeg, png, gif, bmp, webp, svg, ico）
- 可选的data URL支持
- 结果去重
- 保存到文件功能
- 详细的日志记录

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法1：直接运行主程序

```bash
python image_extractor.py
```

程序会提示您输入网址，然后提取并显示所有图片链接。

### 方法2：使用示例程序

```bash
python example.py
```

可以选择示例模式或自定义模式。

### 方法3：作为模块导入

```python
from image_extractor import ImageExtractor

# 创建提取器
extractor = ImageExtractor()

# 提取图片链接
url = "https://example.com"
image_urls = extractor.extract_image_urls(url)

# 打印结果
for url in image_urls:
    print(url)

# 保存到文件
extractor.save_urls_to_file(image_urls, 'images.txt')
```

## 高级用法

### 自定义请求头

```python
custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

extractor = ImageExtractor(timeout=15, headers=custom_headers)
```

### 包含data URL

```python
# 提取包括data URL在内的所有图片
image_urls = extractor.extract_image_urls(url, include_data_urls=True)
```

## 文件说明

- `image_extractor.py` - 主要的图片提取器类
- `example.py` - 使用示例
- `requirements.txt` - 依赖包列表
- `README.md` - 说明文档

## 注意事项

1. 请确保遵守网站的robots.txt规则
2. 某些网站可能有反爬虫机制，可能需要调整请求头
3. 对于需要JavaScript渲染的网站，可能需要使用Selenium等工具
4. 建议在提取大量数据时添加适当的延时

## 错误处理

程序包含完善的错误处理机制：
- 网络连接错误
- 超时处理
- 编码问题
- 文件保存错误

所有错误都会记录到日志中，便于调试。

## 许可证

MIT License 