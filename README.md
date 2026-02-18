# 🛠️ Pipeline de Telemetria Industrial com Dapr

> Pipeline de telemetria industrial orientado a eventos utilizando **Dapr (Pub/Sub)**, **Redis** e **Python**, com visualização em tempo real no **Power BI**.

Este projeto demonstra a implementação de uma arquitetura de microsserviços desacoplada para coleta e processamento de dados de sensores. Ele evolui o conceito do projeto `modbus_data_broker`, substituindo a lógica de mensageria manual pelo runtime orientado a eventos **Dapr**.

## 🏗️ Arquitetura

O projeto utiliza o building block de **Publish/Subscribe** do Dapr para garantir escalabilidade e resiliência:

1.  **Publisher (`producer.py`):** Coleta dados de sensores modbus industriais e os publica no tópico `leituras-caldeira` através do sidecar do Dapr.
2.  **Broker (Redis):** Atua como o componente de infraestrutura para mensageria, gerenciando o tráfego de dados entre os serviços.
3.  **Consumer (`consumer.py`):** Um serviço FastAPI que subscreve ao tópico, processa as leituras e realiza o push dos dados para o dashboard.


<img width="1448" height="352" alt="dapr_publisher-subscribe drawio" src="https://github.com/user-attachments/assets/948f0ad9-4b23-47ff-b104-1dca9f6f80f7" />


## 🚀 Tecnologias Utilizadas

* **Dapr:** Runtime para orquestração de microsserviços e abstração de infraestrutura.
* **Redis:** Message Broker para o padrão Pub/Sub.
* **FastAPI / Python:** Processamento lógico e endpoints de consumo.
* **Power BI:** Visualização e monitoramento em tempo real.


## 🛠️ Como Executar

Certifique-se de ter o [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/) instalado e o Docker rodando para o Redis.


## Comandos utilizados

- Para instalar o Dapr no Mac:
````CLI
brew install dapr/tap/dapr-cli
````

- Inicialização do Dapr localmente:
```CLI
dapr init
```
- Uma vez iniciado. Para rodar os scripts do producer e do consumer, execute os seguintes comandos:
```CLI
dapr run --app-id service-publisher \                                                 
         --app-port 8000 \
         --resources-path ./components \
         --resources-path ./components/jobs \
         -- python3 producer.py

dapr run --app-id service-consumer \
         --app-port 8001 \
         --resources-path ./components \
         -- python3 consumer.py
````
- Para visualizar os aplicativos ativos:
```CLI
dapr dashboard -p 8080
```
## Monitor no Power BI
Os dados consumidos no broker pelo consumer.py são enviados diretamente para um conjunto de dados stream do Power BI assim como o projeto anterior.

<table>
  <tr>
    <td valign="top">
      <img src="https://github.com/user-attachments/assets/38780b8e-d24a-4fdf-8f7c-710c06c71748" alt="Mobile View" width="278" />
    </td>
    <td valign="top">
      <img src="https://github.com/user-attachments/assets/aca1705d-8afb-4f76-8c45-f5a4482dce0d" alt="Desktop View" width="722" />
    </td>
  </tr>
</table>


