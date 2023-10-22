import pandas as pd
import coordinates_data as cd
import geolocation_data as gd
import speed_data as sd
import density as dd
import clean_data as cl

#Naming conventions for this project:
#c = coordinates added 
#g = geolocation API applied
#s = speed api applied
#d = density added
#clean = dataset cleansed

CALL_API_ONLY = False # Switch for the API calls
# When TRUE will allow to make all the API calls and process all the data until we complete the data (This needs to happen in multiple days due to API calls limitation to 2500 a day)
# Once all the API data has been retrieved turn to FALSE to process all the API data stored and create the final dataframe

#Folder location
files_folder= './Files/'
density_folder= './Files/density/'

#Coordinates Files
original_df_filename = f'{files_folder}2023_Accidentalidad.csv'
df_filename_c  =  f'{files_folder}2023_Accidentalidad_c.csv'

#Geolocation Files
geodata_raw_file_json = f'{files_folder}geodata_array_raw.json' #File for the raw data.
geolocation_df_filename = f'{files_folder}geodata_array.csv' #File for the formatted data
df_filename_c_g = f'{files_folder}2023_Accidentalidad_c_g.csv'

#Max Speed data Files
speed_raw_file_json = f'{files_folder}speed_array_raw.json' #File for the raw data.
speed_file_name = f'{files_folder}speed_array.csv' #File for the array of formatted data.  
df_filename_c_g_s = f'{files_folder}2023_Accidentalidad_c_g_s.csv'

#Density data Files
df_filename_c_g_s_d = f'{files_folder}2023_Accidentalidad_c_g_s_d.csv'

#Clean data Files
geojson_file = f'{files_folder}Distritos_de_Madrid.geojson'
schema_file = f'{files_folder}2023_Accidentalidad_schema.json'
df_filename_c_g_s_d_clean = f'{files_folder}2023_Accidentalidad_c_g_s_d_clean.csv'


def merge_dataframes(original_df_filename,  api_df_filename, output_name ):
    df_right = pd.read_csv(original_df_filename)
    df_left =  pd.read_csv(api_df_filename)

    #remove any duplicates
    df = pd.merge(df_right, df_left, on='num_expediente', how='left' )
    df.to_csv(output_name, index= False)

#Step 1: Transform coordinates UTM into Latitude-Longitude
cd.main(original_df_filename, df_filename_c)

#Step 2: Generate the geolocation dataset from the opencagedata.com API
gd.main(CALL_API_ONLY, df_filename_c,geolocation_df_filename,geodata_raw_file_json)

# #Step 3: Generate the max speed dataset from the dev.virtualearth.net API
sd.main(CALL_API_ONLY,df_filename_c,speed_file_name,speed_raw_file_json)

if not CALL_API_ONLY:
#Step 4: Merge the geolocation dataset with the accidents DF 
    merge_dataframes(df_filename_c, geolocation_df_filename, df_filename_c_g)

#Step 5: Merge the max speed dataset with the accidents DF 
    merge_dataframes(df_filename_c_g, speed_file_name, df_filename_c_g_s)

    #Step 6: Apply the density data to the accidents DF
    dd.main(density_folder,df_filename_c_g_s, df_filename_c_g_s_d)

    #Step 7: Clean the dataset
    cl.main(df_filename_c_g_s_d, schema_file, geojson_file, df_filename_c_g_s_d_clean)