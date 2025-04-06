import cv2

image_path = "C:/Users/Fajr2/OneDrive/سطح المكتب/test1pic.jpg"
image = cv2.imread(image_path)

if image is None:
    print("لم يتم العثور على الصورة، تأكد من المسار!")
else:
    cv2.imshow("Test Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()