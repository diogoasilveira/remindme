from datetime import timedelta, date
import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def parse_json(json: dict) -> list:
    hoje = date.today()
    diasdaSemana = {
      0: "Segunda",
      1: "Terça",
      2: "Quarta",
      3: "Quinta",
      4: "Sexta",
      5: "Fim de Semana",
      6: "Fim de Semana",
    }

    eventos = []

    for i in range(7):
      dia = (hoje + timedelta(days=i))
      dia_semana = diasdaSemana.get((hoje + timedelta(days=i)).weekday())
      tarefas = json.get(dia_semana, [])
      eventos.append({
        "dia": dia,
        "tarefas": tarefas,
        })
      
    return eventos


def create_events(tarefas: dict, creds):
    eventos = tarefas
    service = build("calendar", "v3", credentials=creds)
    
    for tarefa in eventos:
        dia = tarefa["dia"]
        tarefas_dia = tarefa["tarefas"]

        for evento in tarefas_dia:
            event = {
                'summary': evento,
                'start': {
                    'date': dia.isoformat(),
                },
                'end': {
                    'date': dia.isoformat(),
                },
            }
            
            try:
                event = service.events().insert(calendarId='primary', body=event).execute()
                print(f"Event created: {event.get('htmlLink')}")
            
            except HttpError as error:
                print(f"An error occurred: {error}")
                return None
            
    