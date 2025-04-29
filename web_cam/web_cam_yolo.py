import cv2
import argparse
import sys
from ultralytics import YOLO

def positive_int(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"カメラIDは0以上の整数で指定してください: {value}")
    return ivalue

parser = argparse.ArgumentParser(description="カメラIDを指定してYOLO検出")
parser.add_argument("-c", "--cam", type=positive_int, default=0, help="カメラ識別番号 (0以上)")
args = parser.parse_args()

CAM_ID = args.cam

# YOLOモデル読み込み (軽量版: yolov8n.pt)
model = YOLO('yolov8n.pt')

# カメラ起動
cap = cv2.VideoCapture(CAM_ID)
if not cap.isOpened():
    print(f"エラー: カメラID {CAM_ID} に接続できませんでした。")
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("エラー: フレームを取得できませんでした。")
        break

    # YOLO推論（直接OpenCV画像を渡せる）
    results = model.predict(frame, imgsz=640, conf=0.5, verbose=False)

    # 推論結果を描画
    annotated_frame = results[0].plot()

    cv2.imshow('YOLO Detection', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
