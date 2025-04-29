import cv2
# カメラからビデオをキャプチャ
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()