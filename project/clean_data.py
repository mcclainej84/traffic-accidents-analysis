import pandas as pd
import geopandas as gpd
import json

categorical_columns = ['tipo_vehiculo', 'numero', 'estado_meteorológico', 'cod_lesividad', 'lesividad', 'positiva_alcohol', 'rango_edad', 'sexo']
redundant_columns=["status_code"  , "status_message" , "total_results" , "city" , "country_code" , "suburb" , "confidence" , "api_timestamp" , "statusCode_speed_api" ,  "speedlimit_speed_api"  , "NOMBRE"]
mode_func = lambda x: x.mode().iloc[0]


def main(input_file, schema_file, geojson_file , output_file):
    # Load the schema from the JSON file
    with open(f'{schema_file}', 'r') as file:
        schema = json.load(file)

        df =( pd.read_csv(input_file, sep=";", 
                        parse_dates=['fecha'])
            .query("speedlimit_kph_speed_api > 0")                    
            .merge(
                (
                    gpd.read_file(geojson_file)
                    .assign(cod_distrito=lambda x: x['cod_distrito'].astype(int))
                    [['cod_distrito', 'NOMBRE']]
                ),
                on='cod_distrito',
                how='left'
            )
            .assign(distrito=lambda x: x['NOMBRE'])  # Assign 'NOMBRE' to a new column 'distrito'
            .assign(high_speed_point=(lambda x: (x['speedlimit_kph_speed_api'] > 65).astype(int)))
            .assign(hora_rango=lambda x: pd.to_datetime(x['hora'], format='%H:%M:%S').dt.hour)
            .assign(positiva_droga=lambda x: x['positiva_droga'].fillna(0).astype(int))
            .drop(columns=redundant_columns) 
            .round({'vmed': 2})
            .astype(schema)
        )

        df_clean = (df.fillna(df[categorical_columns].mode().iloc[0])
                    .to_csv(output_file , sep = ";" ,  index= False))

