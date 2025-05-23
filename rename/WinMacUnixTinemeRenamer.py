import argparse
from pathlib import Path
from datetime import datetime
import platform

def get_onedrive_path():
    home = Path.home()
    # Windows/macOS どちらでも基本的に OneDrive フォルダはこの位置
    onedrive = home / "OneDrive"
    if onedrive.exists():
        return onedrive
    raise FileNotFoundError("OneDrive フォルダが見つかりません")

def get_unique_path(base_path):
    counter = 1
    new_path = base_path
    while new_path.exists():
        new_name = f"{base_path.stem}_{counter}{base_path.suffix}"
        new_path = base_path.parent / new_name
        counter += 1
    return new_path

# === メイン処理 ===
parser = argparse.ArgumentParser(description="エラー詳細表示")
parser.add_argument("-v","--verbose", action='store_true', help="エラー内容表示")
args = parser.parse_args()

try:
    trg_dir = get_onedrive_path() / "8_upload"
    
    files = [f for f in trg_dir.glob("*") if f.is_file()] # フォルダは除外

    if not files:
        print("フォルダ内が空です")
        exit()
    cnt_success = cnt_skip = cnt_err = 0 # 処理数カウンタ
    for file in files:
        try:
            timestamp = int(file.stem) / 1000  # UNIXミリ秒を秒に変換
            dt = datetime.fromtimestamp(timestamp)
            base_name = dt.strftime("%Y-%m-%d-%H%M%S")
            target_path = trg_dir / f"{base_name}{file.suffix}"
            unique_path = get_unique_path(target_path)
            print(f"{file.name} ===> {unique_path.name}")
            file.rename(unique_path)
            cnt_success += 1
        except Exception as e:
            if args.verbose == True:
                print(f"フォーマット形式対象外:{file.name} ")
                cnt_skip += 1
            else:
                print(f"フォーマット形式対象外:{file.name} --> {e}")
                cnt_err += 1
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"成功:{cnt_success:3d}、失敗:{cnt_err:3d}、除外:{cnt_skip:3d} ===> 合計:{cnt_success+cnt_err+cnt_skip:3d}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
except Exception as e:
    print(f"初期化エラー: {e}")
