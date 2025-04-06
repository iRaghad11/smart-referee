from ultralytics import YOLO
import cv2
import os

# تحميل النموذج
model = YOLO('models/best.pt')

def process_image(image_path):
    # يعالج صورة ويحدد الكائنات عليها
    img = cv2.imread(image_path)
    results = model(img)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0].item()
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'{class_name} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow('Image Detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_video(video_path):
    # يعالج فيديو ويحدد الكائنات
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video stream")
            break

        results = model(frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0].item()
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{class_name} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Video Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    file_path = 'test_image1.jpg'  #مسار الفيديو او الصورة

    if os.path.isfile(file_path):
        name, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            process_image(file_path)
        elif ext in ['.mp4', '.avi', '.mov']:
            process_video(file_path)
        else:
            print("Unsupported file format.")
    else:
        print("File not found.")