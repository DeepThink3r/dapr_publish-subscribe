import httpx
import os
import logging
import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PBI_ENDPOINT = os.getenv('POWER_BI_URL')

@app.get("/dapr/subscribe")
async def subscribe():
    return [{
        "pubsubname": "industrial-pubsub",
        "topic": "leituras-caldeira",
        "route": "/processar-leituras"
    }]


@app.post("/processar-leituras")
async def processar_leituras(event = Body(...)):
    leituras = event.get("data")

    if leituras:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(PBI_ENDPOINT, json=leituras)
                if response.status_code == 200:
                    logging.info(f"Lote enviado com sucesso! ({len(leituras)} registros)")
                else:
                    logging.error(f"Erro PBI: {response.status_code} - {response.text}")

            except Exception as e:
                logging.error(f"Falha de rede: {e}")

    return {"status": "SUCCESS"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)