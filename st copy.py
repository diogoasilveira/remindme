import datetime
import os
import cv2
import time
import numpy as np
import streamlit as st
from pre_process import pre_process_image
from ocr_llm import ocr
from create_events import create_events, parse_json
from auth import auth_user

# --- Helper Functions for Screen Management ---
def clear_all_elements():
    """Clears all elements from the main container."""
    st.session_state.container.empty()

# --- Screen Functions ---

def upload_image_screen():
    with st.session_state.container.container():  # Use a sub-container within the main one
        st.subheader("Carregar Imagem")
        input_method = st.selectbox("Carregue uma imagem por:", ["Upload", "Câmera"], key="upload_method")
        image = None

        if input_method == "Câmera":
            image = st.camera_input("Tire uma foto do Quadro", key="camera_input")
        else:
            image = st.file_uploader("Selecione uma foto", type=["jpg", "jpeg", "png"], key="file_uploader")

        if image is not None:
            image_path = "Media/Temp/temp_image.jpg"
            # Ensure the Media/Temp directory exists
            os.makedirs("Media/Temp", exist_ok=True)
            cv2.imwrite(image_path, cv2.cvtColor(cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR),
                                                cv2.COLOR_RGB2BGR))
            st.image(image, caption="Imagem carregada")
            if st.button("Confirmar Imagem", key="confirm_image_button"):
                st.session_state['confirmed_image'] = True
                st.session_state['image_path'] = image_path
                st.rerun() # Rerun to switch to the next screen

def ocr_processing_screen():
    with st.session_state.container.container(): # Use a sub-container within the main one
        st.subheader("Processando Imagem")
        image_path = st.session_state.get('image_path')
        if image_path:
            pre_processed_path = pre_process_image(image_path)
            with st.spinner("Extraindo texto da imagem..."):
                ocr_data = ocr(pre_processed_path)
            st.success("Texto extraído com sucesso!")
            time.sleep(1) # Wait for 1 second as requested
            st.session_state['ocr_data'] = ocr_data
            st.session_state['ocr_complete'] = True
            st.rerun() # Rerun to switch to the next screen

def display_json_screen():
    with st.session_state.container.container(): # Use a sub-container within the main one
        st.subheader("Tarefas Reconhecidas")
        ocr_data = st.session_state.get('ocr_data')
        if ocr_data:
            tarefas = parse_json(ocr_data)
            if tarefas:
                for tarefa in tarefas:
                    st.write(f"**Dia:** {tarefa.get('dia', 'N/A')}")
                    for item in tarefa.get('tarefas', []):
                        st.write(f"- {item}")
                if st.button("Criar Eventos no Google Calendar", key="create_events_button"):
                    st.session_state['create_events'] = True
                    st.rerun()
            else:
                st.warning("Nenhuma tarefa reconhecida na imagem.")
        else:
            st.error("Nenhum dado OCR disponível para exibição.")

def create_events_screen():
    with st.session_state.container.container():
        st.subheader("Criando Eventos")
        ocr_data = st.session_state.get('ocr_data')
        if ocr_data:
            try:
                creds = auth_user() # Ensure credentials are fresh or loaded
                with st.spinner("Criando eventos no Google Calendar..."):
                    create_events(ocr_data, creds)
                st.success("Eventos criados com sucesso no Google Calendar!")
            except Exception as e:
                st.error(f"Erro ao criar eventos: {e}")
        else:
            st.warning("Nenhum dado OCR disponível para criação de eventos.")
        if st.button("Voltar ao Início", key="reset_button"):
            st.session_state.clear() # Clear all session state to restart
            st.rerun()

# --- Main Application Logic ---
if __name__ == "__main__":

    # Authentication (run once)
    if not os.path.exists("token.json"):
        st.warning("Autenticando com o Google Calendar pela primeira vez...")
        auth_user() # This will likely open a browser for authentication

    st.title("RemindMe")
    st.header("Crie eventos no Google Calendar a partir de imagens de tarefas.", divider='gray')
    st.set_page_config(layout="centered", page_title="RemindMe")

    # Initialize main container if not already in session state
    if 'container' not in st.session_state:
        st.session_state.container = st.empty()

    # Session state to manage screens
    if 'confirmed_image' not in st.session_state:
        st.session_state['confirmed_image'] = False
    if 'ocr_complete' not in st.session_state:
        st.session_state['ocr_complete'] = False
    if 'create_events' not in st.session_state:
        st.session_state['create_events'] = False

    if not st.session_state['confirmed_image']:
        upload_image_screen()
    elif not st.session_state['ocr_complete']:
        ocr_processing_screen()
    elif not st.session_state['create_events']:
        display_json_screen()
    else:
        create_events_screen()