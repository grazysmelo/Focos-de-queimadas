{{ config(
    materialized='external',
    location='s3://meu-data-lake-queimadas-2026/gold/fato_focos_incendio.parquet'
) }}

WITH silver AS(
    SELECT * FROM {{ ref('stg_nasa') }}
    ),

dim_satelite AS(
    SELECT * FROM {{ ref('dim_satelite') }}
    ),

fato_final AS (
    SELECT
        s.id_foco,
        d.sk_satelite,
        s.data_hora_brasilia,
        CAST(strftime(s.data_hora_brasilia, '%Y%m%d') AS INT) AS fk_data,
        s.latitude,
        s.longitude,
        s.intensidade_frp_mw AS intensidade_fogo_mw,
        s.temperatura_brilho_i4_k,
        s.temperatura_brilho_i5_k,
        s.status_confianca,
        s.periodo_dia
    FROM silver s
    LEFT JOIN dim_satelite d
        ON s.satelite_origem = d.nome_satelite
        AND s.instrumento_sensor = d.nome_sensor
        )

SELECT * FROM fato_final
