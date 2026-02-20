# 🛠️ Pipeline de Telemetria Industrial com Dapr

> Pipeline de telemetria industrial orientado a eventos utilizando **Dapr (Pub/Sub)**, **Redis** e **Python**, com visualização em tempo real no **Power BI**.

Este projeto demonstra a implementação de uma arquitetura de microsserviços desacoplada para coleta e processamento de dados de sensores. Ele evolui o conceito do projeto `modbus_data_broker`, substituindo a lógica de mensageria manual pelo runtime orientado a eventos **Dapr**.

## 🏗️ Arquitetura

O projeto utiliza o building block de **Publish/Subscribe** do Dapr para garantir escalabilidade e resiliência:

1.  **Publisher (`producer.py`):** Coleta dados de sensores modbus e os publica no tópico `leituras-caldeira` através do sidecar do Dapr.
2.  **Broker (Redis):** Atua como o componente de infraestrutura para mensageria, gerenciando o tráfego de dados entre os serviços.
3.  **Consumer (`consumer.py`):** Um serviço FastAPI que subscreve ao tópico, processa as leituras e realiza o push dos dados para o dashboard.

<img width="1568" height="441" alt="dapr_publisher-subscribe drawio" src="https://github.com/user-attachments/assets/26f73dbe-18ac-42b3-95c6-de95e3a3db5e" />

⭐O Dapr Sidecar é um container/processo que roda junto com a sua aplicação. Em vez de instalar bibliotecas dentro do seu código para conversar com o Redis, você apenas conversa com o Sidecar via protocolos HTTP ou gRPC. O Dapr abstrai a infraestrutura via configuração no arquivo .yaml que armazenamos na pasta components.

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
dapr run --app-id service-publisher --app-port 8000 --resources-path ./components --resources-path ./components/jobs -- python3 producer.py

dapr run --app-id service-consumer --app-port 8001 --resources-path ./components -- python3 consumer.py
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
      <img style="height: 400px; width: auto;" alt="image" src="https://github.com/user-attachments/assets/a5c9805b-d581-4d84-919d-13b4e19222ef" />
    </td>
    <td valign="top">
      <img style="height: 400px; width: auto;" alt="image" src="https://github.com/user-attachments/assets/39b78b96-c959-4682-b963-edf6bbc93f3c" />
    </td>
  </tr>
</table>


