import cv2
#from foto import capture_image
from pre_process import pre_process_image
from ocr_llm import ocr
from create_events import create_events
from auth import auth_user


# ReadmindMe - A Python OCR Application
if __name__ == "__main__":
    #Captura uma imagem da câmera e realiza o pré-processamento
    image_path = "Media/Processed/2025-07-01-wet.jpg"
    #imagem = pre_process_image(image_path)
    #Realiza a extração de texto da imagem pré-processada
    ocr_data = ocr(image_path)
    #print(ocr_data)
    #Faz a criação de eventos no Google Calendar com as tarefas reconhecidas
    print("Criando eventos no Google Calendar...")
    creds = auth_user()
    create_events(ocr_data, creds)

