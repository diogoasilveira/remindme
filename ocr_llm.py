import os
import json
from google import genai
from google.genai import types
from datetime import date

api_key = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

system_prompt = """A partir da imagem fornecida, siga os seguintes passos:

1. Extraia todo o texto da imagem com precisão, mantendo a estrutura original (por colunas e dias da semana).
2. Organize o conteúdo extraído em um objeto JSON no seguinte formato: {"dia da semana": ["tarefa 1", "tarefa 2", ...]}
3. Revise os títulos das tarefas, corrigindo erros gramaticais, de capitalização ou clareza. Os dias da semana devem ser escritos em português, com a primeira letra maiúscula e sem o feira .
4. Agrupe tarefas semelhantes (por tema ou objetivo) quando fizer sentido, mantendo o agrupamento dentro do mesmo dia da semana.
5. Interprete termos ambíguos e reescreva de forma mais clara, se possível, mantendo o significado original.

Retorne apenas o JSON final, com os títulos revisados e organizados."""

def parse_response(response):
    try:
        clean_str = response.replace('```json\n', '').replace('\n```', '')
        json_data = json.loads(clean_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

def ocr(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            system_prompt
            ]
    )

    return parse_response(response.text)



if __name__ == "__main__":
    image_path = f"Media/Processed/{date.today().strftime("%Y-%m-%d")}-wet.jpg"
    #image_path = "Media/Fotos/2025-06-24.jpg"
    results = ocr(image_path)
    print(parse_response(results))