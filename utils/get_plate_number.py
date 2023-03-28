import re
import pytesseract
import cv2
from imutils import contours


def reader_plate(cnts, fileimage: object, plate_namders: list, carplate_image_RGB):
    for contur in cnts:
        area = cv2.contourArea(contur)
        x, y, w, h = cv2.boundingRect(contur)

        if area > 5000:
            img = fileimage[y:y+h, x:x+w]
            result = pytesseract.image_to_string(image=img, lang='rus+eng')
            if len(result) > 5:
                databl = re.findall(r'\d{4} \w{2}-\d', result)
                databl_legal_namber = re.findall(r'\w{2} \d{4}-\d', result)
                if databl:
                    plate_namders.append(databl[0])
                    carplate_image_RGB = cv2.rectangle(carplate_image_RGB, (x, y), (x + w, y + h), (0, 255, 0), 2)
                elif databl_legal_namber:
                    databl = databl_legal_namber[0:6] + ' ' + databl_legal_namber[0:1] + '-' + databl_legal_namber[8]
                    plate_namders.append(databl[0])
                    carplate_image_RGB = cv2.rectangle(carplate_image_RGB, (x, y), (x + w, y + h), (0, 255, 0), 2)

    img = cv2.resize(carplate_image_RGB, (800, 600))
    cv2.imshow('test', img)
    cv2.waitKey()
    return plate_namders, carplate_image_RGB


def car_plate_number():
    carplate_image_RGB = cv2.imread('photo/12902935.jpg')
    height, width, _ = carplate_image_RGB.shape
    gray = cv2.cvtColor(carplate_image_RGB, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    gaus = cv2.GaussianBlur(thresh, (5, 5), 0)
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts, _ = contours.sort_contours(cnts[0])

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    plate_namders = []

    plate_namders, carplate_image_RGB\
        = reader_plate(cnts=cnts, fileimage=gray,carplate_image_RGB=carplate_image_RGB, plate_namders=plate_namders)

    print(plate_namders)
    if not plate_namders:
        plate_namders, carplate_image_RGB \
            = reader_plate(cnts=cnts, fileimage=gaus, carplate_image_RGB=carplate_image_RGB,
                           plate_namders=plate_namders)
        print(plate_namders[0])