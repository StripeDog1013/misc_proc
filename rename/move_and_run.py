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
ctr = 0;
delay = 1.5

print("\n━━━━━━━━━━━━━━━━━━━━━━━━")
print("Move img ===> 8_upload")
print("========================")

# ファイル移動処理
for src_file in glob.glob(str(src_pattern)):
    
    if os.path.isfile(src_file):
        shutil.move(src_file, dst_dir)
        print(f"Moved: {Path(src_file).name}")
        ctr += 1

if not ctr:
    print("フォルダ内が空です")
    
print("========================")
print(f"Total: {ctr:3d} files")
print("━━━━━━━━━━━━━━━━━━━━━━━━\n")
time.sleep(1.5)
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("run WinMacUnixTinemeRenamer.py")
print("============================================")

# Pythonスクリプトの実行
script_path = Path("C:/Dev/python/misc_proc/rename/WinMacUnixTinemeRenamer.py")
subprocess.run(["python", str(script_path), "-v"], check=True)
