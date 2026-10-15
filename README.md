# bulk_image_process_script_

抠图 · 美颜 · 祛痘 · 人脸识别 · 批量 P 图（Python）

说明
本仓库提供一个用于批量处理图片的 Python 脚本，功能包括：自动压缩至目标宽度、可选的人脸美颜（磨皮、祛痘、美白）、保留并写回原始 EXIF 信息、可选抠图（背景去除），并将处理结果保存到 `new` 子目录下。

A. 需要的环境 & 依赖（Environment & Requirements）
- 支持的 Python 版本：
  - Python 3.10
  - Python 3.11
- 建议使用虚拟环境（venv / virtualenv / conda）
- 依赖库（见 `requirements.txt`，可以使用 `pip install -r requirements.txt` 安装）
  - Pillow（图像读取/保存）
  - opencv-python（图像处理）
  - numpy（数值运算）
  - face_recognition（人脸检测/识别，需 dlib 支持）
  - dlib（face_recognition 的底层依赖）
  - rembg（可选：背景移除 / 抠图）
  - piexif（读取/写入 EXIF）
  - tqdm（处理进度条）
  - scikit-image（可选的额外图像算法）

注意：`dlib` 在某些系统上需要 CMake、编译工具链或预编译包（Windows / Linux / macOS 不同）。若遇到安装问题，可优先参考 dlib/face_recognition 的安装说明或使用预编译的 wheel。

B. 如何使用（Usage / What it does）
这个脚本能做什么：
- 批量读取指定文件夹内的图片文件；
- 将图片等比压缩到目标宽度（例如 1920px），高按比例调整；
- 对检测到的人脸区域做美颜处理（磨皮、祛痘、微调亮度/美白）；
- 可选对前景抠图（去背景），但仅对需要时启用；
- 读取原图 EXIF 信息，并将 EXIF 写回处理后的图片（保留拍摄时间、相机信息、地理信息等）；
- 将处理后文件统一保存到输入目录下的 `new/` 子目录（保持原文件不变）。

快速示例（假定脚本名为 `bulk_process.py`）：
1. 安装依赖：
   pip install -r requirements.txt
2. 运行脚本：
   python bulk_process.py --input /path/to/images --output ./new \
       --target-width 1920 --dist 20 --brighten 1.15

（如果脚本以不同参数或配置文件运行，请参照仓库内脚本的实际 CLI 参数。上面示例仅为说明。）

C. 脚本说明（Process / Flow / 关键变量）
处理流程（典型）：
1. 扫描输入目录，列出支持的图片格式（jpg, jpeg, png, webp 等）。
2. 对每张图片：
   - 读取并保存原始 EXIF（如果存在）；
   - 等比压缩到目标宽度（target_width，默认 1920）；
   - 人脸检测：若检测到人脸，定位人脸区域并对人脸区域应用美颜算法（磨皮、祛痘、亮度调整等）；如果未检测到人脸则跳过美颜；
   - （可选）抠图 / 背景移除（只在启用时对前景进行处理）；
   - 将修改后的 EXIF 写回到输出图片；
   - 将输出图片保存到 `output/new/`（或你指定的输出目录）；
3. 输出处理日志/进度。

关键环境变量 / 配置（示例默认值）：
- target_width = 1920
- dist = 20              # 磨皮力度（数值越大，磨皮越明显，范围与脚本实现有关）
- brighten_factor = 1.15 # 美白/提亮系数（1.0 = 不变，1.15 = 提亮 15%）

你可以在脚本命令行参数或配置文件中调整这些值以获得所需效果。

D. 这个脚本的好处（Advantages）
- 保留并写回 EXIF：处理后仍保留拍摄时间、相机信息、地理位置等，方便导入 immich / PhotoPrism / 其它照片管理工具；
- 人脸识别驱动：只对检测到的人脸做美颜，避免误操作动物或风景；
- 一键美颜与祛痘、美白：自动化批量修图，节省大量人工时间；
- 适配低配置机器：默认处理流程和参数适用于大多数普通 PC/笔记本，不一定需要 GPU（但支持加速）；
- 节省时间：适合需要处理大量照片（如旅行照片、婚礼、社交媒体素材）的人或团队。

E. 初衷（Motivation）
此脚本的目标是节省重复手动修图的时间，同时保留照片原始的 EXIF 元数据以便后续使用。网上没找到符合需求的开源批量“美颜 + 保留 EXIF”的脚本，于是自行研究并实现，方便自己和大家快速处理大量照片并保持照片元数据完整。

附：常见问题与建议
- EXIF 无法写回或丢失：请确认源文件确实包含 EXIF，且目标格式支持 EXIF（例如 JPEG 支持，但有些 PNG/WEBP 的 EXIF 支持差异较大）。
- face_recognition/dlib 安装问题：可尝试使用 conda 安装预编译包，或在支持的系统上使用预构建的 wheel。
- 抠图效果与 rembg 等工具相关，可能对某些复杂背景效果不佳，建议先在小批量上试验参数。

许可证
本项目已选择 MIT 许可证（参见仓库根目录的 LICENSE 文件）。

贡献
欢迎提出 issue 或 pull request；若你改进了某些美颜算法或加速实现，请保留 README 中的使用说明并补充示例。
