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
                # Usando endereços 0, 1 e 2 (que o Master lerá como 40001, 40002 e 40003)
                    base_temp = 4800 # 480.0 °C
                    temp = base_temp + random.randint(-20, 20)
                    self._db.set_holding_registers(0, [temp])

                    base_pressao = 6000 # 60.00 bar
                    pressao = base_pressao + random.randint(-15, 15)
                    self._db.set_holding_registers(1, [pressao])


                    base_vazao = 1800 # 180.0 m³/min
                    vazao = base_vazao + random.randint(-100, 100)
                    self._db.set_holding_registers(2, [vazao])

                    print('----STATUS DA CALDEIRA----')
                    print(f'Temp (40001): {temp/10.0} °C')
                    print(f'Pressao (40002): {pressao/100.0} bar')
                    print(f'Vazao (40003): {vazao/10.0} m³/min')
                    print('--------------------------')

                    sleep(10)

        except Exception as erro:
            logging.error("Erro na execução do servidor:", erro)
            self._server.stop()


if __name__ == "__main__":
    srv = ServidorCaldeira(host_ip='0.0.0.0', port=5020)
    #srv = ServidorCaldeira(host_ip='127.0.0.1', port=5020)
    srv.execute()
