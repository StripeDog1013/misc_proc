import os
import re
import argparse
import shutil
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description="指定フォルダ内のファイルをYYYY/MM形式で整理")
    parser.add_argument("-f", "--folder", type=str, help="対象フォルダのパス")
    return parser.parse_args()

def is_valid_filename(filename):
    # 拡張子除去
    name, _ = os.path.splitext(filename)
    # 正規表現でYYYY-MM-DD-hhmmss（6桁以上）またはその末尾に_連番がある形式に一致するか確認
    return re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{6,}(_\d+)?", name) is not None

def move_file(base_path, filename):
    name, ext = os.path.splitext(filename)
    date_match = re.match(r"(\d{4})-(\d{2})-(\d{2})-\d{6,}", name)
    if not date_match:
        return

    yyyy, mm, _ = date_match.groups()

    # フォルダの末尾が対象年(yyyy)と一致する場合はMMだけで振り分け
    base_name = os.path.basename(os.path.normpath(base_path))
    if base_name == yyyy:
        target_dir = os.path.join(base_path, mm)
    else:
        target_dir = os.path.join(base_path, yyyy, mm)

    os.makedirs(target_dir, exist_ok=True)

    src = os.path.join(base_path, filename)
    dst = os.path.join(target_dir, filename)

    # 名前の衝突を避けるために末尾に連番を付加
    count = 1
    base_name = name
    while os.path.exists(dst):
        new_name = f"{base_name}_{count}{ext}"
        dst = os.path.join(target_dir, new_name)
        count += 1

    shutil.move(src, dst)
    print(f"Moved: {filename} ===> {dst}")

def main():
    args = parse_arguments()
    folder = args.folder

    if not os.path.isdir(folder):
        print("指定されたパスは存在しないか、フォルダではありません。")
        return

    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)
        if os.path.isfile(full_path) and is_valid_filename(item):
            move_file(folder, item)

if __name__ == "__main__":
    main()
