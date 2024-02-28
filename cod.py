import easyocr
import cv2
from datetime import datetime

def draw_label(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.7, thickness=2):
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_origin = (position[0], position[1] + text_size[1])
    cv2.rectangle(image, position, (position[0] + text_size[0], position[1] + text_size[1] + 10), (255,255,255), cv2.FILLED)
    cv2.putText(image, text, text_origin, font, font_scale, (0,0,0), thickness, cv2.LINE_AA)
    return image

def detect_russian_license_plates(image_path):
    # Инициализация EasyOCR с поддержкой русского и английского языков
    reader = easyocr.Reader(['ru', 'en'])
    results = reader.readtext(image_path)

    image = cv2.imread(image_path)
    detected_plates = []

    for (bbox, text, prob) in results:
        # Фильтрация результатов по уровню уверенности
        if prob >= 0.5:
            # Рисуем контур вокруг номерного знака
            top_left = tuple([int(val) for val in bbox[0]])
            bottom_right = tuple([int(val) for val in bbox[2]])
            image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

            # Подготавливаем позицию для текста
            label_position = (top_left[0], top_left[1] - 10)
            # Добавляем текст с контуром
            image = draw_label(image, text, label_position)

            detected_plates.append(text)

    # Получение текущего времени
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cv2.putText(image, current_time, (50, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Сохранение аннотированного изображения
    cv2.imwrite('Путь к вашей фотографии', image)

    # Запись номеров в текстовый файл
    with open('detected_license_plates.txt', 'w') as file:
        for plate in detected_plates:
            file_entry = f"{plate} at {current_time}\n"
            file.write(file_entry)

# Указываем путь к файлу
detect_russian_license_plates('nomer_2.png')
