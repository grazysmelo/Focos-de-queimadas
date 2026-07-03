import os
import sys
import requests
import boto3
import json
import datetime


def exec_api(data_exec):
    #airflow passa uma string "YYYY-MM-DD" como arg

    url = "https://queimadas.dgi.inpe.br/api/focos/"
    parametros = {
        "pais_id": 33,
        "inicio": data_exec,
        "fim": data_exec
    }

    #passagem de parâmetros dinâmicos
    response = requests.get(url, params=parametros)

    print(f"Iniciando o processamento da remessa do dia: {data_exec}")

    if response.status_code != 200:
       raise Exception (f"Erro: {response.status_code}")

    json_data = response.json()

    #Particionamento para maior controle no s3
    ano, mes, dia = data_exec.split("-")
    s3_key = f"bronze/ano={ano}/mes={mes}/dia={dia}/focos_{data_exec}.json"

    s3_client = boto3.client('s3')
    bucket_name = os.getenv("AWS_BRONZE_BUCKET", "BUCKET_QUEIMADAS_BRONZE")

    #Conversão para string e envio direto para s3 sem salvamento local
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=json.dumps(json_data)
    )
    print(f"Dados salvos no s3: {s3_key}")

#Processo para receber args pela linha de comando. Caso não possua args será utilizado a data atual de execução
if __name__ == "__main__":
    if len(sys.argv) > 1:
        data_rodada = sys.argv[1]
    else:
        data_rodada = datetime.today().strftime('%Y-%m-%d')

exec_api(data_rodada)