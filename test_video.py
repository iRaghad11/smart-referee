import cv2
from ultralytics import YOLO

# تحميل نموذج YOLO
model = YOLO("yolov8n.pt")  

# فتح ملف الفيديو
video_path = "match.mp4"  # اسم الفيد
cap = cv2.VideoCapture(video_path)


if not cap.isOpened():
    print("Error: Unable to open video file")
    exit()

frame_skip = 3  #يحلل كل 3 فريمات 
frame_id = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break 

    frame_id += 1
    if frame_id % frame_skip != 0:  
        continue  # التحليل وتسريع الأداء

    # تشغيل YOLO على الإطار الحالي
    results = model(frame)

    # يرسم صندوق على الاجسام المكتشفة
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # استخراج إحداثيات الصندوق
            conf = box.conf[0]
            cls = int(box.cls[0])  # فئة الكائن

            # رسم المستطيل حول الكائن
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{model.names[cls]}: {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # عرض الفيديو مع التحليل
    cv2.imshow("YOLO Detection", frame)

    # يقفل البرنامج بالضغط علىQ
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()