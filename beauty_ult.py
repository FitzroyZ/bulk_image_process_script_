import os
import sys
import cv2
import numpy as np
from PIL import Image
import pillow_heif
from tqdm import tqdm
import mediapipe as mp
import piexif

pillow_heif.register_heif_opener()

def select_folder():
    """交互式选择文件夹或手动输入路径"""
    print("========================================")
    print("    Ultimate 美颜与美白脚本 (保留EXIF)    ")
    print("========================================")
    
    folders = []
    i = 1
    for dir in os.listdir('.'):
        if os.path.isdir(dir) and not dir.startswith('.'):
            folders.append(dir)
            print(f"[{i}] {dir}")
            i += 1

    print("----------------------------------------")
    print("提示: 你可以直接输入完整路径（如 ~/photos），")
    print("      或者直接输入上面对应的序号来选择文件夹。")
    print("========================================")

    input_choice = input("请输入路径或序号: ").strip()
    
    if not input_choice:
        print("错误: 输入不能为空。")
        sys.exit(1)

    if input_choice.isdigit():
        index = int(input_choice) - 1
        if 0 <= index < len(folders):
            target_path = f"./{folders[index]}"
            print(f"已选择文件夹: {folders[index]}")
        else:
            print("错误: 无效的序号选择。")
            sys.exit(1)
    else:
        target_path = input_choice

    expanded_path = os.path.expanduser(target_path)
    if not os.path.isdir(expanded_path):
        print(f"错误: 路径不存在或不是一个目录: {target_path}")
        sys.exit(1)
        
    return expanded_path

def process_images():
    input_path = select_folder()
    output_path = os.path.join(input_path, 'new')
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.heic', '.HEIC')
    files = [f for f in os.listdir(input_path) if f.lower().endswith(valid_extensions)]
    
    if not files:
        print("未在指定路径下找到支持的图片文件。")
        return

    target_width = 1920
    dist = 20          # 磨皮力度
    brighten_factor = 1.15  # 美白亮度系数 (提亮 8%)

    mp_face_detection = mp.solutions.face_detection
    
    print(f"开始处理目录: {input_path} ...")
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        
        for filename in tqdm(files, desc="处理进度"):
            file_path = os.path.join(input_path, filename)
            try:
                # 1. 使用 PIL 打开原图并提取 EXIF 信息
                pil_img = Image.open(file_path).convert('RGB')
                
                exif_bytes = None
                try:
                    # 尝试从原图获取 EXIF 字典字节流
                    exif_bytes = pil_img.info.get('exif')
                except Exception:
                    pass

                orig_width, orig_height = pil_img.size
                
                # 2. 如果图片宽度大于目标宽度，进行等比例缩小以加速
                if orig_width > target_width:
                    ratio = target_width / float(orig_width)
                    target_height = int(orig_height * ratio)
                    pil_img_resized = pil_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                else:
                    pil_img_resized = pil_img
                
                img = cv2.cvtColor(np.array(pil_img_resized), cv2.COLOR_RGB2BGR)
                h, w, _ = img.shape
                
                # 3. 人脸检测与保护（猫猫和背景不受影响）
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = face_detection.process(img_rgb)
                
                img_final = img.copy()
                
                if results.detections:
                    mask = np.zeros((h, w), dtype=np.float32)
                    
                    for detection in results.detections:
                        bbox = detection.location_data.relative_bounding_box
                        xmin = int(bbox.xmin * w)
                        ymin = int(bbox.ymin * h)
                        box_w = int(bbox.width * w)
                        box_h = int(bbox.height * h)
                        
                        padding_x = int(box_w * 0.15)
                        padding_y = int(box_h * 0.15)
                        
                        x1 = max(0, xmin - padding_x)
                        y1 = max(0, ymin - padding_y)
                        x2 = min(w, xmin + box_w + padding_x)
                        y2 = min(h, ymin + box_h + padding_y)
                        
                        mask[y1:y2, x1:x2] = 1.0
                    
                    # 边缘羽化，使过渡自然
                    kernel_size = int(w * 0.05) | 1
                    mask = cv2.GaussianBlur(mask, (kernel_size, kernel_size), 0)
                    
                    # 4. 双边滤波磨皮
                    img_beauty = cv2.bilateralFilter(img, dist, int(dist * 2), int(dist / 2))
                    
                    # 5. LAB 空间轻度人脸美白
                    lab = cv2.cvtColor(img_beauty, cv2.COLOR_BGR2Lab)
                    l_channel, a_channel, b_channel = cv2.split(lab)
                    l_channel = np.clip(l_channel.astype(np.float32) * brighten_factor, 0, 255).astype(np.uint8)
                    lab_bright = cv2.merge([l_channel, a_channel, b_channel])
                    img_whitened = cv2.cvtColor(lab_bright, cv2.COLOR_Lab2BGR)
                    
                    # 6. 融合人脸（保护猫和背景）
                    mask_3ch = cv2.merge([mask, mask, mask])
                    img_final = (img_whitened * mask_3ch + img * (1.0 - mask_3ch)).astype(np.uint8)
                
                # 7. 转回 PIL Image 并保存，同时植入原图的 EXIF
                final_pil_img = Image.fromarray(cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))
                
                base_name, _ = os.path.splitext(filename)
                output_file_path = os.path.join(output_path, f"{base_name}_compressed.jpg")
                
                if exif_bytes:
                    try:
                        final_pil_img.save(output_file_path, "JPEG", quality=95, exif=exif_bytes)
                    except Exception:
                        # 若 EXIF 注入失败则降级直接保存
                        final_pil_img.save(output_file_path, "JPEG", quality=95)
                else:
                    final_pil_img.save(output_file_path, "JPEG", quality=95)
                
            except Exception as e:
                print(f"\n处理文件 {filename} 时出错: {e}")

    print(f"所有图片处理完成！新图片已保存在: {output_path}")

if __name__ == '__main__':
    process_images()
