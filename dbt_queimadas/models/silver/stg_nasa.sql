{{ config(materialized='table') }}

WITH staging AS (
    SELECT * FROM {{ ref('raw_csv') }}
),

cleaned AS (
    SELECT
        CAST(latitude AS DOUBLE) AS latitude,
        CAST(longitude AS DOUBLE) AS longitude,
        -- Métricas
        CAST(temperatura_brilho_i4 AS DOUBLE) AS temperatura_brilho_i4_k,
        CAST(temperatura_brilho_i5 AS DOUBLE) AS temperatura_brilho_i5_k,

        scan,
        track,
        acq_date AS data_captura_original,
        acq_time AS hora_captura_original,
        confidence AS nivel_confianca,
        version AS versao_algoritmo,
        frp AS poder_radiativo_fogo,
        daynight AS periodo_dia_ou_noite

        -- Padronização dos textos
        UPPER(TRIM(CAST(codigo_satelite AS VARCHAR))) AS satelite_origem,
        UPPER(TRIM(CAST(instrumento AS VARCHAR))) AS instrumento_sensor,
    FROM staging
        WHERE
        latitude IS NOT NULL
        AND longitude IS NOT NULL
)

SELECT * FROM cleaned