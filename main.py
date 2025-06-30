import cv2
from ReadmindMe.foto import capture_image
from ReadmindMe.pre_process import pre_process_image
from ReadmindMe.ocr import ocr_image

# ReadmindMe - A Python OCR Application
if __name__ == "__main__":
    image_path = "Media/2025-06-20.jpg"
    imagem = pre_process_image(image_path)
    results = ocr_image(imagem)
    print(results)