import os
import re
import argparse
import shutil

def parse_arguments():
    parser = argparse.ArgumentParser(description="指定フォルダ内のファイルをYYYY/MM形式で整理")
    parser.add_argument("-f", "--folder", type=str, help="対象フォルダのパス")
    return parser.parse_args()

def is_valid_filename(filename):
    name, _ = os.path.splitext(filename)
    return re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{6,}(_\d+)?", name) is not None

def move_file(base_path, filename):
    name, ext = os.path.splitext(filename)
    date_match = re.match(r"(\d{4})-(\d{2})-(\d{2})-\d{6,}", name)
    if not date_match:
        return False

    yyyy, mm, _ = date_match.groups()
    base_name = os.path.basename(os.path.normpath(base_path))
    target_dir = os.path.join(base_path, mm) if base_name == yyyy else os.path.join(base_path, yyyy, mm)

    os.makedirs(target_dir, exist_ok=True)

    src = os.path.join(base_path, filename)
    dst = os.path.join(target_dir, filename)

    count = 1
    base_name_only = name
    while os.path.exists(dst):
        new_name = f"{base_name_only}_{count}{ext}"
        dst = os.path.join(target_dir, new_name)
        count += 1

    try:
        shutil.move(src, dst)
        print(f"Moved: {filename} ===> {dst}")
        return True
    except Exception as e:
        print(f"移動失敗: {filename} ({e})")
        return False

def main():
    args = parse_arguments()
    folder = args.folder

    if not os.path.isdir(folder):
        print("指定されたパスは存在しないか、フォルダではありません。")
        return

    cnt_success = cnt_invalid = cnt_skipped = 0

    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)
        if os.path.isfile(full_path):
            if is_valid_filename(item):
                if move_file(folder, item):
                    cnt_success += 1
                else:
                    cnt_invalid += 1
            else:
                cnt_invalid += 1
        else:
            cnt_skipped += 1

    total = cnt_success + cnt_invalid + cnt_skipped
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"成功: {cnt_success:3d}｜失敗: {cnt_invalid:3d}｜対象外: {cnt_skipped:3d} ===> 合計: {total:3d}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    main()
