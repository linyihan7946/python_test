# 文件处理工具集

这个目录包含了多个文件处理工具，包括图片路径读取器和图片裁剪工具。

## 工具列表

### 1. 图片路径读取器 (image_reader.py)
用于读取指定目录下所有图片文件路径的Python工具。

### 2. 图片裁剪工具 (image_cropper.py)
用于将图片裁剪为指定尺寸的Python工具，特别适用于将宽屏图片裁剪为手机壁纸尺寸。

## 图片裁剪工具

### 功能特性

- 将图片裁剪为1080*1920尺寸（手机壁纸尺寸）
- 以图片水平方向的中间位置为中心进行裁剪
- 支持批量处理
- 支持多种图片格式（jpg, jpeg, png, gif, bmp, webp, tiff, tif）
- 自动处理图片模式转换
- 详细的处理日志和统计信息
- 预览功能

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用方法

#### 方法1：直接运行主程序

```bash
python image_cropper.py
```

程序会提示您输入源目录和输出目录路径。

#### 方法2：运行示例程序

```bash
python crop_example.py
```

可以选择不同的使用模式：
- 示例模式（使用预设路径）
- 自定义批量裁剪
- 预览裁剪效果
- 单张图片裁剪

#### 方法3：作为模块导入

```python
from image_cropper import ImageCropper

# 创建裁剪器
cropper = ImageCropper(target_width=1080, target_height=1920)

# 批量裁剪
stats = cropper.batch_crop_images("源目录", "输出目录")

# 单张图片裁剪
success = cropper.crop_image("输入图片.jpg", "输出图片.jpg")

# 预览裁剪效果
cropper.preview_crop("图片.jpg")
```

### 主要方法

#### 1. batch_crop_images()
批量裁剪图片

```python
stats = cropper.batch_crop_images("源目录", "输出目录")
print(f"成功: {stats['success']} 张")
print(f"失败: {stats['failed']} 张")
```

#### 2. crop_image()
裁剪单张图片

```python
success = cropper.crop_image("input.jpg", "output.jpg")
```

#### 3. preview_crop()
预览裁剪效果

```python
cropper.preview_crop("image.jpg")
```

### 裁剪逻辑

1. **水平居中**：以图片水平方向的中间位置为中心
2. **垂直裁剪**：从图片顶部开始裁剪1920像素高度
3. **边界处理**：如果裁剪框超出图片边界，会自动调整
4. **尺寸检查**：会检查原图是否满足最小尺寸要求

### 支持的图片格式

- JPEG: .jpg, .jpeg
- PNG: .png
- GIF: .gif
- BMP: .bmp
- WebP: .webp
- TIFF: .tiff, .tif

### 文件说明

- `image_cropper.py` - 主要的图片裁剪器类
- `crop_example.py` - 使用示例
- `requirements.txt` - 依赖包列表
- `README.md` - 说明文档

### 注意事项

1. 确保原图尺寸满足要求（宽度≥1080，高度≥1920）
2. 输出目录会自动创建（如果不存在）
3. 裁剪后的图片会添加"_cropped"后缀
4. 支持批量处理大量图片
5. 处理过程中会显示详细进度

### 错误处理

程序包含完善的错误处理机制：
- 图片格式检查
- 尺寸验证
- 文件权限检查
- 异常捕获和日志记录

---

## 图片路径读取器

### 功能特性

- 支持多种图片格式
- 递归搜索子目录
- 按扩展名筛选图片
- 使用通配符模式搜索
- 获取图片文件详细信息
- 保存路径列表到文件
- 详细的日志记录

### 使用方法

```python
from image_reader import ImageReader

reader = ImageReader()
image_paths = reader.get_image_paths("目录路径", recursive=True)
```

详细使用方法请参考之前的文档。

## 许可证

MIT License 