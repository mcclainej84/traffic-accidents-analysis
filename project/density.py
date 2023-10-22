import pandas as pd

def prepare_dataset(month,density_folder):
    #This program will join the density data which its density location file for each month

    print(f'start processing month {month}')
    #Open the datasets
    df_ubicacion = pd.read_csv(f'{density_folder}pmed_ubicacion_{month}-2023.csv', sep= ";" ).fillna(0)
    df_densidad = pd.read_csv(f'{density_folder}{month}-2023.csv', sep = ";")  

    df_densidad[['fecha', 'hora']] = df_densidad['fecha'].str.split(' ', expand=True)
    df_densidad['int_real'] = df_densidad['intensidad']/4 #As per documentation "intensidad" is marked as vehicles/hour so to get the real intensidad in 15 min intervals we need to divide by four
    df_ubicacion['cod_distrito'] = df_ubicacion['distrito']  
    
    print(f'before merge month {month}')
    
    df = (
        pd.merge(df_densidad, df_ubicacion, on='id')[['fecha' ,  'cod_distrito'  , 'int_real' , 'ocupacion' , 'vmed' , 'hora']]
        .groupby(['cod_distrito', 'fecha' , 'hora' ]).agg({
                                    'int_real': 'mean',
                                    'ocupacion': 'mean',
                                    'vmed':  lambda x: x[x > 0].mean()})
        .assign(vmed=lambda x: x['vmed'].fillna(0))                                    
        .reset_index()
    )    
    print(f'finish processing month {month}')
    return df

def main(density_folder,original_df_filename,output_file):
    dfs= []
    # TODO: For this consider parallel processing
    
    for i in range(1, 6):
        df = prepare_dataset(f"{i:02}",density_folder)
        dfs.append(df)
        
    if len(dfs)>0:
        dfc = pd.concat(dfs , ignore_index= True)

    #Set the date in the same format to allow to join datasets
    dfc['fecha'] = pd.to_datetime(dfc['fecha'], format='%Y/%m/%d')  

    # #Open source dataframe
    df = pd.read_csv(original_df_filename)

    #Apply transformations
    # TODO: This can be set into only 1 statement.
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')
    df['dia_semana'] = df['fecha'].dt.strftime('%A')
    df['hora_accidente'] = df['hora']
    df['hora'] = (pd.to_datetime(df['hora'], format='%H:%M:%S').dt.round('15min').dt.time.astype(str))
        
    merged_df = pd.merge(
        df, dfc, on=['cod_distrito', 'fecha', 'hora' ], how='inner')
    
    merged_df.to_csv(output_file, sep = ";" , index=False )
    
