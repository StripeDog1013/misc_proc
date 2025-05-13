import os
from pathlib import Path
from PIL import Image

def get_onedrive_path():
    home = Path.home()
    # Windows/macOS どちらでも基本的に OneDrive フォルダはこの位置
    onedrive = home / "OneDrive"
    if onedrive.exists():
        return onedrive

# 走査対象ディレクトリ
target_dir = get_onedrive_path() / "0_Image/0_WallPaper/desktop"

# 出力するテキストファイル
output_file = target_dir / "low_resolution_images.txt"

# 出力先を初期化
with open(output_file, "w", encoding="utf-8") as f_out:
    for img_path in target_dir.glob("*"):
        if img_path.is_file() and img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}:
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    if width <= 1920 or height <= 1080:
                        f_out.write(f"{img_path.name} ({width}x{height})\n")
            except Exception as e:
                print(f"読み込み失敗: {img_path} ({e})")

print(f"完了: {output_file} に出力しました。")