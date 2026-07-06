import os
import sys
import requests
import boto3
from datetime import datetime

def csmd_api():
    # 1. Configurações de Segurança e Ambiente
    map_key = os.getenv("NASA_MAP_KEY")
    bucket_name = os.getenv("AWS_DATA_LAKE_BUCKET", "meu-data-lake-queimadas-2026")

    if not map_key:
        raise ValueError("ERRO: A variável de ambiente NASA_MAP_KEY não foi definida.")

    # 2. URL que funcionou no seu teste (Bounding Box do Brasil e América do Sul)
    # Traz os focos do último 1 dia
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{map_key}/VIIRS_SNPP_NRT/-74,-34,-34,6/1"

    print(f"[{datetime.now()}] Coletando dados da NASA FIRMS via Bounding Box...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        dados_csv = response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar na API da NASA: {e}")
        sys.exit(1)

    # 3. Particionamento dinâmico baseado na data de hoje para automação diária
    hoje = datetime.today()
    ano = hoje.strftime('%Y')
    mes = hoje.strftime('%m')
    dia = hoje.strftime('%d')

    s3_key = f"bronze/nasa_firms/ano={ano}/mes={mes}/dia={dia}/focos_{ano}_{mes}_{dia}.csv"

    # 4. Upload do texto do CSV direto para o S3
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=dados_csv.encode('utf-8')
        )
        print(f"[{datetime.now()}] CSV salvo com sucesso no S3: {s3_key}")
    except Exception as e:
        print(f"Erro ao fazer upload para o S3: {e}")
        sys.exit(1)

if __name__ == "__main__":
    csmd_api()