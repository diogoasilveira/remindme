import cv2
from datetime import date


def pre_process_image(image_path):
    """
    Função para pré-processar a imagem capturada.
    Lê a imagem do diretório Media e aplica filtros de pré-processamento.
    """
    dia = date.today().strftime("%Y-%m-%d")
    #image_path = f'Media/{dia}.jpg'
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not read image from {image_path}")
    else:
        print(f"Image {image_path} loaded successfully.")

    # Converte imagem para escala de cinza, depois binário e aplica filtro de ruído
    imagem_cinza = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    imagem_eq = clahe.apply(imagem_cinza)
    _, imagem_binaria = cv2.threshold(imagem_eq, 127, 255, cv2.THRESH_BINARY)
    imagem_ruido = cv2.medianBlur(imagem_binaria, 5)

    # Equaliza a imagem para melhorar o contraste
    alpha = 1.5
    beta = 50
    imagem_processada = cv2.convertScaleAbs(imagem_ruido, alpha=alpha, beta=beta)
    cv2.imwrite(f'Media/Processed/{dia}-wet.jpg', imagem_processada)
    return f'Media/Processed/{dia}-wet.jpg'

#cv2.imshow('Imagem Original', image)
#cv2.imshow('Imagem Processada', imagem_processada)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#pre_process_image(f"Media/Fotos/{date.today().strftime('%Y-%m-%d')}.jpg")