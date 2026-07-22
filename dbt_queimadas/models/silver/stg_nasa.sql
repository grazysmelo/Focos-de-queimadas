{{ config(
    materialized='table',
    external_location='s3://meu-data-lake-queimadas-2026/silver/stg_nasa_queimadas.parquet'
) }}

WITH staging AS (
    SELECT * FROM {{ ref('raw_nasa') }}
),

cleaned AS (
    SELECT
        -- Cria uma surrogate key (lat-lon-data-hora)
        md5(concat_ws('-', CAST(latitude AS VARCHAR), CAST(longitude AS VARCHAR), CAST(data_captura_original AS VARCHAR), CAST(hora_captura_original AS VARCHAR))) AS id_foco,

        CAST(latitude AS DOUBLE) AS latitude,
        CAST(longitude AS DOUBLE) AS longitude,

        -- Tratativa do horario de captura
        CAST(
            strptime(
                concat(
                    CAST(data_captura_original AS VARCHAR),
                    ' ',
                    lpad(CAST (hora_captura_original AS VARCHAR), 4, '0')
                ),
                '%Y-%m-%d %H%M'
                ) AS TIMESTAMP
            ) - INTERVAL '3' HOUR AS data_hora_brasilia,

        -- Métricas
        CAST(temperatura_brilho_i4 AS DOUBLE) AS temperatura_brilho_i4_k,
        CAST(temperatura_brilho_i5 AS DOUBLE) AS temperatura_brilho_i5_k,
        CAST(poder_radiativo_fogo AS DOUBLE) AS intensidade_frp_mw,

        -- Padronização dos textos
        UPPER(TRIM(CAST(nivel_confianca AS VARCHAR))) AS status_confianca,

        CASE UPPER(TRIM(CAST(periodo_dia_ou_noite AS VARCHAR)))
            WHEN 'D' THEN 'DIURNO'
            WHEN 'N' THEN 'NOTURNO'
            ELSE 'N/I'
        END AS periodo_dia,

        UPPER(TRIM(CAST(instrumento AS VARCHAR))) AS instrumento_sensor,
        UPPER(TRIM(CAST(codigo_satelite AS VARCHAR))) AS satelite_origem

    FROM staging
        WHERE
        latitude IS NOT NULL
        AND longitude IS NOT NULL
)

SELECT * FROM cleaned