import cv2
import argparse
import sys
import torch
from ultralytics import YOLO


def positive_int(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"カメラIDは0以上の整数で指定してください: {value}")
    return ivalue


def select_model(mode):
    models = {
        "n": "./yolo26/yolo26n.pt",
        "s": "./yolo26/yolo26s.pt",
        "m": "./yolo26/yolo26m.pt",
        "l": "./yolo26/yolo26l.pt",
        "x": "./yolo26/yolo26x.pt"
    }
    return models[mode]


def select_device(device):
    if device == "auto":
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    if device == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDAが利用できません。")
        return "cuda"

    if device == "mps":
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPSが利用できません。")
        return "mps"

    return "cpu"


parser = argparse.ArgumentParser(description="カメラIDを指定してYOLO検出")
parser.add_argument("-c", "--cam", type=positive_int, default=0, help="カメラ識別番号 (0以上)")
parser.add_argument("-m", "--mode", choices=["n", "s", "m", "l", "x"], default="n", help="学習モデル")
parser.add_argument(
    "-d",
    "--device",
    choices=["auto", "cpu", "cuda", "mps"],
    default="auto",
    help="推論デバイス: auto, cpu, cuda, mps",
)

args = parser.parse_args()

CAM_ID = args.cam
MODEL_ID = select_model(args.mode)

try:
    DEVICE = select_device(args.device)
except RuntimeError as e:
    print(f"エラー: {e}")
    sys.exit(1)

print(f"Using model : {MODEL_ID}")
print(f"Using device: {DEVICE}")

model = YOLO(MODEL_ID)

cap = cv2.VideoCapture(CAM_ID)
if not cap.isOpened():
    print(f"エラー: カメラID {CAM_ID} に接続できませんでした。")
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("エラー: フレームを取得できませんでした。")
        break

    results = model.predict(
        frame,
        imgsz=640,
        conf=0.5,
        device=DEVICE,
        verbose=False,
    )

    annotated_frame = results[0].plot()

    cv2.imshow("YOLO Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()