# 🔥 Focos de Queimadas — Pipeline de Dados

Pipeline de dados end-to-end com objetivo de disponibilizar dados da **API Nasa Firm** limpos e tratados. Com foco de 
processamento dos dados utilizando arquitetura medalhão no s3, com a disponibilização no Athena!

![Arquitetura do pipeline](/images/arquitetura.png)

## 📌 Visão geral

O projeto automatiza todo o ciclo de dados: da ingestão diária dos focos de incêndio via API até a entrega de tabelas
analíticas prontas para consumo, com testes de qualidade e deploy contínuo.

**Fluxo do pipeline:**

1. **Ingestão (Python)** — script coleta os focos de calor mais recentes da API
   pública NASA FIRMS e grava o CSV bruto no S3.
2. **Bronze (S3)** — armazenamento dos dados brutos, particionados por ano/mês/dia. **Ex(s3://meu-data-lake-queimadas-2026/bronze/nasa_firms/ano=2026/mes=07/dia=09/)**
3. **Orquestração (Apache Airflow)** — DAG diária que executa a ingestão e, em seguida, dispara as transformações do
   dbt.
4. **Transformação (dbt + DuckDB)** — modelos SQL organizados em Bronze → Silver → Gold, com tipagem, limpeza e
   modelagem dimensional.
5. **Silver / Gold (S3, Parquet)** — dados tratados (Silver) e modelo dimensional fato/dimensão (Gold) prontos para
   análise.
6. **Consulta (Amazon Athena)** — camadas Silver e Gold consultadas via SQL serverless.
7. **Visualização (Power BI)** — dashboard de monitoramento consumindo os dados da camada Gold.

## 🖥️ Dashboard

Dashboard desenvolvido no Power BI para dar uma visão consolidada dos focos processados pelo pipeline: total de focos,
intensidade média e distribuição por período do dia (diurno/noturno).

![Dashboard de monitoramento](/images/dashboard-final.png)

## 🛠️ Stack utilizada

| Camada         | Tecnologia                                                                       |
|----------------|----------------------------------------------------------------------------------|
| Ingestão       | Python (requests, boto3)                                                         |
| Data Lake      | Amazon S3                                                                        |
| Orquestração   | Apache Airflow                                                                   |
| Transformação  | dbt (engine DuckDB, com extensões `httpfs`/`aws` para ler e gravar direto no S3) |
| Consulta       | Amazon Athena                                                                    |
| Infraestrutura | Terraform                                                                        |
| CI/CD          | GitHub Actions                                                                   |
| Visualização   | Power BI                                                                         |

## 🏗️ Arquitetura de dados (Medalhão)

### Bronze — `raw_nasa`

View sobre os arquivos CSV brutos gravados no S3, sem transformação, apenas renomeando colunas.

### Silver — `stg_nasa`

Tabela tratada, materializada como Parquet externo no S3:

- Geração de chave substituta (`id_foco`) via hash MD5 (latitude + longitude + data/hora).
- Conversão de tipos (latitude/longitude, temperaturas, FRP).
- Conversão do horário de captura (UTC) para horário de Brasília.
- Padronização de textos (nível de confiança, período do dia, satélite, instrumento).
- Filtro de registros sem latitude/longitude.

### Gold — modelagem dimensional

- **`dim_satelite`**: dimensão com satélite e instrumento sensor (chave substituta via MD5).
- **`fato_focos_incendio`**: tabela fato com os focos processados, intensidade do fogo (FRP em MW), temperaturas de
  brilho, nível de confiança e período do dia, materializada como Parquet externo no S3.

Os modelos Silver e Gold possuem testes de qualidade (`not_null`, `unique`) definidos via dbt.

## ☁️ Infraestrutura (Terraform)

O bucket S3 que hospeda as camadas Bronze/Silver/Gold é provisionado via Terraform.

```
terraform/
├── main.tf         # bucket S3 + bloqueio de acesso público
└── variables.tf    
```

## 🔄 CI/CD (GitHub Actions)

A cada push/PR na branch `developer`, o workflow `.github/workflows/ci_cd.yml`:

1. Configura credenciais AWS e Python.
2. Executa o script de ingestão (`src/csmd_api.py`), gravando os dados brutos no S3.
3. Configura o profile do dbt (DuckDB + extensões S3).
4. Roda `dbt run` para atualizar as camadas Silver e Gold.
5. Roda `dbt test` para validar a qualidade dos dados.

Em produção, a ingestão e o `dbt run` são orquestrados diariamente pela DAG do Airflow (`pipeline_nasa_queimadas`,
agendada para as 06h).

## 🔎 Fonte de dados

Os dados são coletados da API pública **NASA FIRMS**, sensor **VIIRS_SNPP_NRT**, configurada atualmente com um bounding
box cobrindo o Brasil e a América do Sul (`-74,-34,-34,6`), com uma janela de 1 dia de dados por execução. O bounding
box é facilmente ajustável no script de ingestão para outras regiões.

## 👩‍💻 **Graziele Melo** · [LinkedIn](https://linkedin.com/in/graziele-melo)
