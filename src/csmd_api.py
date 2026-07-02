import requests

def exec_api(data_exec):
    #airflow passa uma string "YYYY-MM-DD" como arg

    url = "https://queimadas.dgi.inpe.br/api/focos/"
    parametros = {
        "pais_id": 33,
        "inicio": data_exec,
        "fim": data_exec
    }
    response = requests.get(url, params=parametros)
    data = response.json()