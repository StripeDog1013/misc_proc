import subprocess
from pathlib import Path
from tqdm import tqdm
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Real-ESRGANによる一括アップスケール処理")
    parser.add_argument("-i", "--input-dir", type=Path, required=True, help="入力画像フォルダのパス")
    parser.add_argument("-o", "--output-dir", type=Path, required=True, help="出力画像フォルダのパス")
    parser.add_argument("-m", "--model", type=str, default="realesrgan-x4plus", help="使用するモデル名 (例: realesrgan-x4plus)")
    parser.add_argument("-s", "--scale", type=str, default="4", help="アップスケール倍率 (例: 2 or 4)")
    parser.add_argument("-g", "--gpu", type=str, default="0", help="使用GPU番号（0 or 1）")
    return parser.parse_args()

def main():
    args = parse_args()

    # Real-ESRGAN 実行ファイルのパス
    realesrgan_exe = r"C:\Apps\realesrgan\realesrgan-ncnn-vulkan.exe"

    input_dir = args.input_dir
    output_dir = args.output_dir
    model = args.model
    scale = args.scale
    gpu = args.gpu

    output_dir.mkdir(exist_ok=True)

    valid_ext = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    image_files = [img_path for img_path in input_dir.glob("*") if img_path.suffix.lower() in valid_ext]

    for img_path in tqdm(image_files, desc="アップスケール進行中", unit="file"):
        output_path = output_dir / img_path.name

        if output_path.exists():
            continue

        cmd = [
            realesrgan_exe,
            "-i", str(img_path),
            "-o", str(output_path),
            "-n", model,
            "-s", scale,
            "-g", gpu
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"エラー発生: {img_path.name} をスキップします。")
            continue

    print("すべての処理が終了しました。")

if __name__ == "__main__":
    main()
