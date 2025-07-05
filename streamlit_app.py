import datetime
import cv2
import time
import numpy as np
import streamlit as st
from pre_process import pre_process_image
from ocr_llm import ocr
from create_events import create_events, parse_json
from auth import auth_user
#from foto import capture_image


# ReadmindMe - A Python OCR Application
if __name__ == "__main__":
    st.title("RemindMe")
    st.header("Crie eventos no Google Calendar a partir de imagens de tarefas.", divider='gray')
    #Captura uma imagem da câmera e realiza o pré-processamento
    input = st.selectbox("Carregar imagem", ["Upload", "Câmera"])
    if input == "Câmera":
        image = st.camera_input("Tire uma foto do Quadro")
    else:
        image = st.file_uploader("Carregar imagem", type=["jpg", "jpeg", "png"])

    if image is not None:
        # Salva a imagem carregada em um caminho temporário
        image_path = "Media/Temp/temp_image.jpg"
        cv2.imwrite(image_path, cv2.cvtColor(cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR),
                                             cv2.COLOR_RGB2BGR))    
        st.image(image, caption="Imagem de entrada")
        
        # Realiza o pré-processamento da imagem
        pre_processed_path = pre_process_image(image_path)

        # Realiza a extração de texto da imagem pré-processada
        #with st.spinner("Extraindo texto da imagem..."):
        #    ocr_data = ocr(pre_processed_path)

        # Exibe os resultados do OCR
        st.subheader("Tarefas reconhecidas:")
        #tarefas = parse_json(ocr_data)
        tarefas = [{'dia': datetime.date(2025, 7, 3),
                    'tarefas': ['Revisar HTTP', 'API Google', 'Agenda']},
                    {'dia': datetime.date(2025, 7, 4),
                    'tarefas': ['TCC Match', 'Reunião CI Herman']},
                    {'dia': datetime.date(2025, 7, 5), 'tarefas': ['Desejo de Menina']},
                    {'dia': datetime.date(2025, 7, 6), 'tarefas': ['Desejo de Menina']},
                    {'dia': datetime.date(2025, 7, 7), 'tarefas': ['Muita Coisa']},
                    {'dia': datetime.date(2025, 7, 8),
                    'tarefas': ['Fotos para OCR', 'Parágrafo', 'Decidir Arquitetura']},
                    {'dia': datetime.date(2025, 7, 9),
                    'tarefas': ['Organizar Main', 'Heurística']}]
        for tarefa in tarefas:
            st.write(f"{tarefa['dia']}: {', '.join(tarefa['tarefas'])}")        
        
    #image_path = "Media/Processed/2025-07-01-wet.jpg"
    #image = pre_process_image(image_path)
    #Realiza a extração de texto da imagem pré-processada
    #ocr_data = ocr(image_path)
    #print(ocr_data)
    #Faz a criação de eventos no Google Calendar com as tarefas reconhecidas
    #print("Criando eventos no Google Calendar...")
    #creds = auth_user()
    #create_events(ocr_data, creds)
