from pyModbusTCP.server import DataBank, ModbusServer
import logging
from time import sleep
import random

# Definindo parâmetros de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ServidorCaldeira():

    def __init__(self, host_ip, port):
        self._db = DataBank()
        self._server = ModbusServer(
            host=host_ip, port=port, no_block=True, data_bank=self._db)

    def execute(self):
        try:
            self._server.start()
            logging.info(f"Servidor Caldeira ativo em {self._server.host}:{self._server.port}")

            while True:
                # --- Caldeira 01 (Registros de 0 a 2) ---
                c1_data = [
                    4800 + random.randint(-20, 20), # Temp
                    6000 + random.randint(-15, 15), # Pressão
                    1800 + random.randint(-100, 100) # Vazão
                ]
                # Carrega os dados para a memória do servidor
                self._db.set_holding_registers(0, c1_data)

                # --- Caldeira 02 (Registros de 10 a 12)
                c2_data = [
                    5200 + random.randint(-30, 30),
                    800 + random.randint(-10, 10),
                    1500 + random.randint(-50, 50)
                ]
                self._db.set_holding_registers(10, c2_data)

                # --- CALDEIRA 03 (Endereço 20) ---
                c3_data = [
                    6100 + random.randint(-40, 40), 
                    6200 + random.randint(-20, 20), 
                    2000 + random.randint(-120, 120)
                ]
                self._db.set_holding_registers(20, c3_data)


                logging.info(
                    f"Ciclo Completo | "
                    f"C1: {c1_data[0]/10}°C, {c1_data[1]/100}bar, {c1_data[2]/10}m³/m | "
                    f"C2: {c2_data[0]/10}°C, {c2_data[1]/100}bar, {c2_data[2]/10}m³/m | "
                    f"C3: {c3_data[0]/10}°C, {c3_data[1]/100}bar, {c3_data[2]/10}m³/m"
                    )

                sleep(10)

        except Exception as erro:
            logging.error("Erro na execução do servidor:", erro)
            self._server.stop()


if __name__ == "__main__":
    try:
        srv = ServidorCaldeira(host_ip='0.0.0.0', port=5020)
        #srv = ServidorCaldeira(host_ip='127.0.0.1', port=5020)
        srv.execute()
    except KeyboardInterrupt:
        print("\n[!] Finalizando o servidor Modbus...")
