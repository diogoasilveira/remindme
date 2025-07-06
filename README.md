# RemindMe: Sincronize Suas Tarefas de Quadro Branco com o Google Calendar\!

O RemindMe é uma aplicação que utiliza **visão computacional** e **inteligência artificial** para ler e sincronizar suas tarefas escritas em um quadro branco diretamente com o Google Calendar.

-----

## Como Funciona?

O processo acontece com as seguintes etapas:

1.  **Pré-processamento de Imagem:** A imagem do seu quadro branco é aprimorada usando algoritmos de Visão Computacional com **OpenCV**, como CLAHE, binarização e redução de ruídos. Isso garante que o texto esteja nítido e pronto para ser lido.

2.  **Reconhecimento Inteligente de Texto (ICR):** Utilizamos a capacidade multimodal de **Large Language Models (LLMs)**, especificamente o **Gemini**, para reconhecer os caracteres e inscrições no quadro branco com alta precisão.

3.  **Organização e Estruturação:** O texto reconhecido é então processado e organizado, gerando um arquivo **JSON** estruturado com as datas e suas respectivas tarefas.

4.  **Edição Flexível:** Antes da sincronização, a aplicação permite que você **edite o JSON**, adicionando, modificando ou removendo tarefas de qualquer dia.

5.  **Sincronização com Google Calendar:** Com um clique, suas tarefas são sincronizadas de forma contínua com seu **Google Calendar** utilizando a **API do Google Calendar**.

-----

## Interface

A interface interativa do RemindMe foi desenvolvida com **Streamlit**, proporcionando uma experiência de usuário simples e eficaz.

-----

## Demonstração

Veja o RemindMe em ação:

[https://github.com/user-attachments/assets/d68bc78a-2606-4967-b40f-a3f0135afdcb](https://github.com/user-attachments/assets/d68bc78a-2606-4967-b40f-a3f013afdcb)

-----
