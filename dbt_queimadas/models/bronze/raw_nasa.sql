{{ config(materialized='view') }}

WITH raw AS (
    SELECT *
    FROM read_csv_auto('s3://{{ var("meu-data-lake-queimadas-nasa-2026") }}/bronze/nasa_firms/ano=*/*/*/*.csv', filename=true)
)

SELECT
    latitude,
    longitude,
    bright_ti4 AS temperatura_brilho_i4,
    scan,
    track,
    acq_date AS data_captura_original,
    acq_time AS hora_captura_original,
    satellite AS codigo_satelite,
    instrument AS instrumento,
    confidence AS nivel_confianca,
    version AS versao_algoritmo,
    bright_ti5 AS temperatura_brilho_i5,
    frp AS poder_radiativo_fogo,
    daynight AS periodo_dia_ou_noite
FROM raw