import os
from datetime import datetime
import logging
from fastapi import FastAPI
import requests
from pyModbusTCP.client import ModbusClient

# FastAPI para fazer o post no Dapr
app = FastAPI()


#Configuração de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#Variáveis globais
DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
PUBSUB_NAME = "industrial-pubsub"
TOPIC_NAME = "leituras-caldeira"
DAPR_URL = f"http://localhost:{DAPR_PORT}/v1.0/publish/{PUBSUB_NAME}/{TOPIC_NAME}"

CALDEIRAS_CONFIG = [
    {"id": "Caldeira_01", "offset": 0},
    {"id": "Caldeira_02", "offset": 10},
    {"id": "Caldeira_03", "offset": 20}
]

# Cliente modbus
cliente = ModbusClient(host='localhost', port=5020, auto_open=True)


def publicar_no_dapr(payload):
    
    try:
        # Enviamos para os dados para o SIDECAR
        response = requests.post(DAPR_URL, json=payload)
        if response.status_code == 204:
            logging.info(f"Publicado no Dapr: {payload}")
        else:
            logging.error(f"Erro no Dapr: {response.text}")
    except Exception as e:
        logging.error(f"Erro de conexão com Sidecar: {e}")


def coletar_e_enviar():
    agora = datetime.now().isoformat()
    batch_payload = []

    for caldeira in CALDEIRAS_CONFIG:
        regs = cliente.read_holding_registers(caldeira["offset"], 3)

        if regs:
            batch_payload.append({
                "sensor_id": caldeira["id"],
                "temperatura": regs[0]/10,
                "pressao": regs[1]/100,
                "vazao": regs[2]/10,
                "timestamp": agora
            })
            
            publicar_no_dapr(batch_payload)
        else:
            logging.error(f"Falha na leitura da {caldeira['id']} no offset {caldeira['offset']}")


@app.post("/agendador-caldeira")
def gatilho_evento():
    coletar_e_enviar()
    return {"status": "coleta_iniciada"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)