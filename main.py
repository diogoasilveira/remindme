import datetime
import os
import cv2
import time
import numpy as np
import pandas as pd
import streamlit as st
from pre_process import pre_process_image
from ocr_llm import ocr
from create_events import create_events, parse_json
from auth import auth_user

# --- Utils de Gerenciamento de Telas ---
def clear_all_elements():
    """Clears all elements from the main container."""
    st.session_state.container.empty()

# --- Funções de Telas ---

def upload_image_screen():
    with st.session_state.container.container():  #Usa um sub-container dentro do principal
        st.subheader("Carregar Imagem")
        input_method = st.selectbox("Carregue uma imagem por:", ["Upload", "Câmera"], key="upload_method")
        image = None

        if input_method == "Câmera":
            image = st.camera_input("Tire uma foto do Quadro", key="camera_input")
        else:
            image = st.file_uploader("Selecione uma foto", type=["jpg", "jpeg", "png"], key="file_uploader")

        if image is not None:
            image_path = "Media/Temp/temp_image.jpg"
            os.makedirs("Media/Temp", exist_ok=True)
            cv2.imwrite(image_path, cv2.cvtColor(cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR),
                                                cv2.COLOR_RGB2BGR))
            st.image(image, caption="Imagem carregada")
            if st.button("Confirmar Imagem", key="confirm_image_button"):
                st.session_state['confirmed_image'] = True
                st.session_state['image_path'] = image_path
                st.rerun() 

def ocr_processing_screen():
    with st.session_state.container.container(): #Usa um sub-container dentro do principal
        st.subheader("Processando Imagem")
        image_path = st.session_state.get('image_path')
        if image_path:
            pre_processed_path = pre_process_image(image_path)
            with st.spinner("Extraindo texto da imagem..."):
                ocr_data = ocr(pre_processed_path)
            st.success("Texto extraído com sucesso!")
            time.sleep(1) 
            st.session_state['ocr_data'] = ocr_data
            st.session_state['ocr_complete'] = True
            st.rerun() 

def display_json_screen():
    with st.session_state.container.container(): #Usa um sub-container dentro do principal
        st.subheader("Tarefas Reconhecidas")
        ocr_data = st.session_state.get('ocr_data')
        if ocr_data:
            tarefas = parse_json(ocr_data)
            if tarefas:
                for i, dia_tarefas in enumerate(tarefas):
                    st.subheader(f"Tarefas para {dia_tarefas['dia'].strftime('%d/%m/%Y')}")
                    # Criar um DataFrame a partir da lista de tarefas para o dia, transformando cada tarefa em uma linha editável
                    df_single_day_tasks = pd.DataFrame({'Tarefa': dia_tarefas['tarefas']})
                    # Usar st.data_editor no DataFrame das tarefas do dia, num_rows="dynamic" permite adicionar/remover linhas (tarefas)
                    edited_df_single_day_tasks = st.data_editor(
                        df_single_day_tasks,
                        num_rows="dynamic",
                        key=f"editor_tasks_{i}"
                    )
                    # Atualizar a lista de tarefas original com as edições e filtra valores vazios que podem surgir de linhas deletadas ou novas vazias
                    tarefas[i]['tarefas'] = edited_df_single_day_tasks['Tarefa'].dropna().tolist()

                st.write("---")
                st.subheader("Tarefas Editadas")
                
                for dia in tarefas:
                    st.write(f"**{dia['dia'].strftime('%d/%m/%Y')}**: {', '.join(dia['tarefas'])}")

                if st.button("Criar Eventos no Google Calendar", key="create_events_button"):
                    st.session_state['ocr_data'] = tarefas
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
                creds = auth_user()
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

    # Autenticação de usuário
    if not os.path.exists("token.json"):
        st.warning("Autenticando com o Google Calendar pela primeira vez...")
        auth_user()

    st.title("RemindMe")
    st.header("Crie eventos no Google Calendar a partir de imagens de tarefas.", divider='gray')
    st.set_page_config(layout="centered", page_title="RemindMe")

    # Inicializa container principal
    if 'container' not in st.session_state:
        st.session_state.container = st.empty()

    # Session state para gerenciar telas
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