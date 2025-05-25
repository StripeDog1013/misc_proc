import os
import subprocess
from pathlib import Path
import glob
import shutil
import time

# ホームディレクトリを取得
home_dir = Path.home()

# 移動元と移動先のパスを作成
src_pattern = home_dir / "Downloads/img/*"
dst_dir = home_dir / "OneDrive" / "8_upload"
cnt_success = cnt_failed = 0
cnt_total = 0
delay = 1.5

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("Move img ===> 8_upload")
print("====================================")

# ファイル移動処理（成功、失敗でそれぞれカウント）
for src_file in glob.glob(str(src_pattern)):
    
    if os.path.isfile(src_file):
        try:
            shutil.move(src_file, dst_dir)
            print(f"Moved: {Path(src_file).name}")
            cnt_success += 1
        except Exception as e:
            cnt_failed += 1

# 処理ファイル数の合算
cnt_total = cnt_success + cnt_failed

if not cnt_total:
    print("フォルダ内が空です")
    
print("====================================")
print(f"成功: {cnt_success:3d}｜失敗: {cnt_failed:3d} ===> 合計: {cnt_total:3d}")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
time.sleep(1.5)
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("run WinMacUnixTinemeRenamer.py")
print("============================================")

# Pythonスクリプトの実行
script_path = Path("C:/Dev/python/misc_proc/rename/WinMacUnixTinemeRenamer.py")
subprocess.run(["python", str(script_path), "-v"], check=True)
