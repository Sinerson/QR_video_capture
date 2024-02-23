import cv2
from pyzbar.pyzbar import decode


# video = cv2.VideoCapture(0)
video = cv2.VideoCapture('http://89.207.64.58:8080/rtsp/25213/24a1a32552c827a266cb')
# зададим размеры картинки прочитаем ее и изменим размер
im_height = 50
im_width = 50
im = cv2.resize(cv2.imread("test_image.png"), (im_width, im_height))
# зададим шрифт
font = cv2.FONT_HERSHEY_SIMPLEX
# пустой список, в который будем складывать найденные значения кодов
somelist = []
# обозначим переменную для хранения найденных данных
my_data = None
# крутимся в бесконечном цикле
while True:
    # читаем видеопоток
    ret, frame1 = video.read()
    ret, frame2 = video.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 100:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, f"Found {len(contours)} moving polygons", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

    if not ret:
        break
    # добавляем в каждый кадр нашу картинку
    frame1[0:im_width, 0:im_height] = im
    # декодируем каждый код
    for barcode in decode(frame1):
        # и помещаем его в переменную
        my_data = barcode.data.decode('utf-8')
        # проверяем, есть ли данные в переменной, и добавляем отсутствующие
        if my_data in somelist:
            print("Такой код уже есть!")
            for el in somelist:
                print(el)
        else:
            print(f"Обнаружен новый код: {my_data}, добавляю в список")
            somelist.append(my_data)
    # Постоянно ожидаем нажация "q" и прерываем цикл
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    cv2.putText(frame1, my_data, (50, 50), font, 0.6, (0, 255, 255), 2, cv2.LINE_4)
    cv2.imshow("Barcode/QR Code Scanner", frame1)
    frame1 = frame2
    ret, frame2 = video.read()
# Освобождаем видеоустройство и закрываем все окна
video.release()
cv2.destroyAllWindows()
