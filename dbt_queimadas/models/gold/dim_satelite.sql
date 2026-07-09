{{ config(materialized='table') }}

WITH silver AS (
    SELECT DISTINCT
        satelite_origem,
        instrumento_sensor
    FROM {{ ref('stg_nasa') }}
    ),

dimensao AS (
    SELECT
        md5(concat_ws('-', satelite_origem, instrumento_sensor)) AS sk_satelite,
        satelite_origem AS nome_satelite,
        instrumento_sensor AS nome_sensor
    FROM silver
    )

SELECT * FROM dimensao