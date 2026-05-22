import cv2
from ultralytics import YOLO

# YOLOモデル読み込み（nanoが軽量で安定）
model = YOLO("./yolo8/yolov8n.pt")

# カメラ起動（0 = 内蔵カメラ）
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラが開けません")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレーム取得失敗")
        break

    # 推論（OpenCVのBGR画像をそのまま渡す）
    results = model(frame)[0]  # results[0]で1枚分の結果を取得

    # 結果を描画（OpenCV画像形式で返る）
    annotated_frame = results.plot()

    # 画面に表示
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
