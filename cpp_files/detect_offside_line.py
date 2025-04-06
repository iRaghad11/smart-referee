import cv2
import numpy as np

cap = cv2.VideoCapture("match.mp4")

# فلترت الملعب عشان ما تطلع خطوط على الجمهور
def get_field_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 40, 40])  
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    return mask

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  

    # صغرت الصوره عشان السرعه
    scale_percent = 50
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    frame_resized = cv2.resize(frame, (width, height))

    # إزالة أي شيء برا الملعب
    field_mask = get_field_mask(frame_resized)
    field_only = cv2.bitwise_and(frame_resized, frame_resized, mask=field_mask)

    # تحويل إلى الرمادي و تحسين الحواف
    gray = cv2.cvtColor(field_only, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # اكتشاف الخطوط
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=120, minLineLength=80, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0] * 2  # تعديل الحجم بعد التصغير
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # الأخضر للخطوط

    # اكتشاف الدوائر (الدائرة الوسطى)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=100)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0] * 2, i[1] * 2)  # تعديل الحجم بعد التصغير
            radius = i[2] * 2  # تعديل الحجم بعد التصغير
            cv2.circle(frame, center, radius, (0, 0, 255), 3)  # الأحمر للدوائر

    # عرض الفيديو
    cv2.imshow("Field Detection", frame)

    # انهاء البرنامج ب "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()