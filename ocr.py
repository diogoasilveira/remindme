import cv2
import matplotlib.pyplot as plt
import os
import sys
import easyocr
import torch
from datetime import date

def ocr_image(image_path):
    """
    Realiza OCR em uma imagem fornecida e retorna o texto extraído.
    
    Args:
        image_path (str): Caminho para a imagem.
        
    Returns:
        str: Texto extraído da imagem.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file {image_path} does not exist.")
    
    # Carrega a imagem
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read the image file {image_path}. Please check the file format.")
    # Converte a imagem para RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Inicializa o leitor OCR
    reader = easyocr.Reader(['pt'], gpu=torch.cuda.is_available())
    # Realiza OCR na imagem
    results = reader.readtext(image_rgb)
    return results

def bounding_box(detection):
    """
    Get the bounding box coordinates from the detection result.
    
    Args:
        detection (tuple): A tuple containing the detection result.
        
    Returns:
        tuple: A tuple containing the top-left and bottom-right coordinates of the bounding box.
    """
    top_left = tuple([int(val) for val in detection[0][0]])
    bottom_right = tuple([int(val) for val in detection[0][2]])
    return top_left, bottom_right

def process_detections(detection):
    """
    Process the text from the detection result.
    
    Args:
        detection (tuple): A tuple containing the detection result.
        
    Returns:
        str: The processed text.
    """
    pass

def display_results(image_path, results):
    """
    Display the image with OCR results.
    
    Args:
        image_path (str): Path to the image file.
        results (list): List of OCR results.
    """
    #Lê a imagem
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read the image file {image_path}. Please check the file format.")
    
    # Desenha os resultados do OCR na imagem
    for detection in results:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        image = cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), 5)
        image = cv2.putText(image, text,
                            (bottom_right[0], bottom_right[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    
    # Salva a imagem com os resultados do OCR
    if not os.path.exists('Media/Processed'):
        os.makedirs('Media/Processed')
    #img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'Media/OCR/{date.today().strftime("%Y-%m-%d")}-ocr.jpg', image)

if __name__ == "__main__":
    #imagens até fhd são ok
    #image_path = "Media/2025-06-20.jpg"
    #imagem muito grande
    image_path = "Media/Processed/2025-06-24-wet.jpg"
    results = ocr_image(image_path)
    display_results(image_path, results)
    print(results)