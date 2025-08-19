# 图片水印去除工具

这是一个用于去除图片水印的Python工具，支持指定多个矩形范围来精确去除水印。

## 功能特性

- 支持指定多个矩形区域去除水印
- 提供4种不同的去除方法
- 支持批量处理
- 支持配置文件保存和加载
- 支持多种图片格式
- 详细的处理日志和统计信息

## 去除方法

### 1. inpaint (图像修复) - 推荐
使用OpenCV的图像修复算法，能够智能地填充水印区域，效果最好。

### 2. blur (模糊)
对水印区域进行高斯模糊处理，适合处理半透明水印。

### 3. fill (填充)
使用周围区域的平均颜色填充水印区域，适合处理简单背景。

### 4. clone (克隆)
在图片中寻找最佳匹配区域，复制到水印位置，适合处理重复纹理。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法1：直接运行主程序

```bash
python watermark_remover.py
```

程序会提示您输入图片路径、输出路径和矩形区域。

### 方法2：运行示例程序

```bash
python watermark_example.py
```

可以选择不同的使用模式：
- 示例模式
- 自定义处理
- 批量处理
- 配置文件使用
- 方法对比测试

### 方法3：作为模块导入

```python
from watermark_remover import WatermarkRemover

# 创建水印去除器
remover = WatermarkRemover()

# 定义矩形区域 (x, y, width, height)
rectangles = [
    (100, 50, 200, 80),    # 左上角水印
    (800, 600, 150, 60),   # 右下角水印
]

# 去除水印
success = remover.remove_watermark_by_rectangles(
    "input.jpg", "output.jpg", rectangles, method='inpaint'
)
```

## 主要方法

### 1. remove_watermark_by_rectangles()
去除指定矩形区域的水印

```python
success = remover.remove_watermark_by_rectangles(
    image_path, output_path, rectangles, method='inpaint'
)
```

### 2. batch_remove_watermarks()
批量去除水印

```python
config = {
    'rectangles': [(100, 50, 200, 80)],
    'method': 'inpaint'
}
stats = remover.batch_remove_watermarks(source_dir, output_dir, config)
```

### 3. save_config() / load_config()
保存和加载水印配置

```python
# 保存配置
remover.save_config(config, 'watermark_config.json')

# 加载配置
config = remover.load_config('watermark_config.json')
```

## 矩形区域格式

矩形区域使用 `(x, y, width, height)` 格式：
- `x`: 左上角x坐标
- `y`: 左上角y坐标  
- `width`: 矩形宽度
- `height`: 矩形高度

示例：
```python
rectangles = [
    (100, 50, 200, 80),    # 从(100,50)开始的200x80矩形
    (800, 600, 150, 60),   # 从(800,600)开始的150x60矩形
]
```

## 支持的图片格式

- JPEG: .jpg, .jpeg
- PNG: .png
- BMP: .bmp
- TIFF: .tiff, .tif
- WebP: .webp

## 使用示例

### 单张图片处理

```python
from watermark_remover import WatermarkRemover

remover = WatermarkRemover()

# 定义水印区域
rectangles = [
    (100, 50, 200, 80),    # 左上角水印
    (800, 600, 150, 60),   # 右下角水印
]

# 去除水印
success = remover.remove_watermark_by_rectangles(
    "带水印图片.jpg", 
    "去除水印后.jpg", 
    rectangles, 
    method='inpaint'
)
```

### 批量处理

```python
# 批量处理配置
config = {
    'rectangles': [(100, 50, 200, 80)],
    'method': 'inpaint'
}

# 批量处理
stats = remover.batch_remove_watermarks(
    "源图片目录", 
    "输出目录", 
    config
)

print(f"成功处理: {stats['success']} 张图片")
```

### 配置文件使用

```python
# 保存配置
config = {
    'rectangles': [(100, 50, 200, 80)],
    'method': 'inpaint'
}
remover.save_config(config, 'my_config.json')

# 加载配置
loaded_config = remover.load_config('my_config.json')
rectangles = loaded_config['rectangles']
method = loaded_config['method']
```

## 文件说明

- `watermark_remover.py` - 主要的水印去除器类
- `watermark_example.py` - 使用示例
- `requirements.txt` - 依赖包列表
- `README.md` - 说明文档

## 注意事项

1. 确保矩形区域坐标正确，避免超出图片边界
2. 推荐使用 `inpaint` 方法，效果最好
3. 对于复杂背景，可能需要调整矩形区域大小
4. 批量处理时建议先测试单张图片
5. 处理大图片时可能需要较长时间

## 错误处理

程序包含完善的错误处理机制：
- 图片格式检查
- 坐标边界验证
- 文件权限检查
- 异常捕获和日志记录

## 许可证

MIT License
