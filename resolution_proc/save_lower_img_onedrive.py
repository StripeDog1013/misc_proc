import os
import shutil
from pathlib import Path
from PIL import Image

def get_onedrive_path():
    home = Path.home()
    # Windows/macOS どちらでも基本的に OneDrive フォルダはこの位置
    onedrive = home / "OneDrive"
    if onedrive.exists():
        return onedrive

# 元の壁紙ディレクトリ
source_dir = get_onedrive_path() / "0_Image/0_WallPaper/desktop"

# コピー先ディレクトリ
dest_dir = source_dir / "lowres_images"
dest_dir.mkdir(exist_ok=True)

# 出力テキストファイル
output_file = source_dir / "low_resolution_images.txt"

# 出力先を初期化
with open(output_file, "w", encoding="utf-8") as f_out:
    for img_path in source_dir.glob("*"):
        if img_path.is_file() and img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}:
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    if width <= 1920 or height <= 1080:
                        # テキストに書き出し
                        f_out.write(f"{img_path.name} ({width}x{height})\n")
                        # ファイルをコピー
                        shutil.copy2(img_path, dest_dir / img_path.name)
            except Exception as e:
                print(f"読み込み失敗: {img_path} ({e})")

print(f"完了: {output_file} にリストを出力し、対象画像を {dest_dir} にコピーしました。")
