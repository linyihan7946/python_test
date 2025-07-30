# 图片路径读取器

这是一个用于读取指定目录下所有图片文件路径的Python工具。

## 功能特性

- 支持多种图片格式（jpg, jpeg, png, gif, bmp, webp, svg, ico, tiff, tif, jfif, pjpeg, pjp, avif）
- 递归搜索子目录
- 按扩展名筛选图片
- 使用通配符模式搜索
- 获取图片文件详细信息
- 保存路径列表到文件
- 详细的日志记录

## 使用方法

### 方法1：直接运行主程序

```bash
python image_reader.py
```

程序会提示您输入目录路径和搜索模式。

### 方法2：运行示例程序

```bash
python example_usage.py
```

可以选择示例模式或自定义模式。

### 方法3：作为模块导入

```python
from image_reader import ImageReader

# 创建图片读取器
reader = ImageReader()

# 获取所有图片路径
image_paths = reader.get_image_paths("C:/Pictures", recursive=True)

# 打印结果
for path in image_paths:
    print(path)

# 保存到文件
reader.save_paths_to_file(image_paths, 'my_images.txt')
```

## 主要方法

### 1. get_image_paths()
获取指定目录下的所有图片路径

```python
# 递归搜索所有子目录
image_paths = reader.get_image_paths("C:/Pictures", recursive=True)

# 只搜索当前目录
image_paths = reader.get_image_paths("C:/Pictures", recursive=False)
```

### 2. get_image_paths_by_extensions()
按扩展名筛选图片

```python
# 只获取JPG和PNG图片
jpg_png_paths = reader.get_image_paths_by_extensions(
    "C:/Pictures", 
    extensions=['.jpg', '.jpeg', '.png'], 
    recursive=True
)
```

### 3. get_image_paths_by_pattern()
使用通配符模式搜索

```python
# 搜索所有JPG图片
jpg_paths = reader.get_image_paths_by_pattern(
    "C:/Pictures", 
    pattern="*.jpg", 
    recursive=True
)

# 搜索特定前缀的图片
prefix_paths = reader.get_image_paths_by_pattern(
    "C:/Pictures", 
    pattern="IMG_*", 
    recursive=True
)
```

### 4. get_image_info()
获取图片文件的详细信息

```python
image_info = reader.get_image_info(image_paths)

for info in image_info:
    print(f"文件名: {info['filename']}")
    print(f"路径: {info['path']}")
    print(f"大小: {info['size_mb']} MB")
    print(f"扩展名: {info['extension']}")
    print(f"创建时间: {info['created_time']}")
    print(f"修改时间: {info['modified_time']}")
```

### 5. save_paths_to_file()
保存图片路径到文件

```python
reader.save_paths_to_file(image_paths, 'image_list.txt')
```

## 支持的图片格式

- JPEG: .jpg, .jpeg, .jfif, .pjpeg, .pjp
- PNG: .png
- GIF: .gif
- BMP: .bmp
- WebP: .webp
- SVG: .svg
- ICO: .ico
- TIFF: .tiff, .tif
- AVIF: .avif

## 文件说明

- `image_reader.py` - 主要的图片路径读取器类
- `example_usage.py` - 使用示例
- `README.md` - 说明文档

## 注意事项

1. 路径支持相对路径和绝对路径
2. 递归搜索可能会比较慢，特别是对于包含大量文件的目录
3. 文件大小以字节为单位，MB为计算值
4. 时间戳为Unix时间戳格式

## 错误处理

程序包含完善的错误处理机制：
- 目录不存在检查
- 文件访问权限检查
- 路径有效性验证
- 异常捕获和日志记录

## 许可证

MIT License 