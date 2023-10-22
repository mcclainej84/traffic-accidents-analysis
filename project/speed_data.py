import configparser
import pandas as pd
import requests
import json
import numpy as np
import os

def get_api_key():
    config = configparser.ConfigParser()
    config.read('api_keys.cfg')
    return config.get('bing', 'bing_api_key')

def geo_speed_vals(num_exp, lat,long):
    url = f'https://dev.virtualearth.net/REST/v1/Routes/SnapToRoad?points={long},{lat}&includeTruckSpeedLimit=true&IncludeSpeedLimit=true&speedUnit=MPH&travelMode=driving&key={get_api_key()}'

    response_trafico = requests.get(url)
    json_response = response_trafico.json()
    json_response['num_expediente'] = num_exp
    json_response['Latitude'] = lat
    json_response['Longitude'] = long    

    return json_response

def mph_to_kph(mph):    
    converter= 1.60934    
    v=mph * converter
    
    if mph in (43,12,62,31,37,6):
        kph = np.ceil(v)
    else:
        kph=np.floor(v)       

    return round(kph)

def write_to_file(dl , filename):
    #Create a new file with data
    with open(filename, "w") as file:
        json.dump(dl, file, indent=4)

def exists_in_dict_list(num_exp,dl_raw):
    exp_list = set(item['num_expediente']for item in dl_raw)

    if num_exp in exp_list:
        return True
    else:
        return False        
    
def get_data_extracted(row):
    try:
        resource = row["resourceSets"][0]["resources"][0]["snappedPoints"][0]
        speedlimit = resource.get("speedLimit")        
    except IndexError:
        resource = {}
        speedlimit= 0

    return (      
        row["num_expediente"],
        row["statusCode"],
        resource.get('coordinate'), 
        resource.get("name"),
        speedlimit
    )

def create_speed_data_set(dl_raw,speed_file_name):  
    column_names= ['num_expediente',
                'statusCode_speed_api', 
                "coordinates_speed_api",
                "road_name_speed_api", 
                "speedlimit_speed_api"]
        
    dl = [  get_data_extracted(item) for item in dl_raw]
    df = pd.DataFrame(dl, columns = column_names)
    df.set_index('num_expediente', inplace=True)
    df['speedlimit_kph_speed_api'] = df['speedlimit_speed_api'].apply(mph_to_kph)
    df.to_csv(speed_file_name)


"""PARAMS:
    call_api => If set to TRUE will call the API. Otherwise just skip the API part and transform raw data into a formatted dataset
"""
def main(call_api ,original_df_filename,speed_file_name, speed_raw_file_json ):
    #Declare variables
    SAVEDATA_THRESHOLD = 50  #Threshold for saving the data into a file after X json calls.
    count_json_calls= 0 #Counter for the json calls to the API. 
    column_list = ['num_expediente', 'latitude' , 'longitude']

    try:
        with open(speed_raw_file_json, "r") as file:
            dl_raw = json.load(file)
    except IOError:
        dl_raw = []


    #API processing step
    if call_api:            
        #read csv file
        df = pd.read_csv(original_df_filename)[column_list].drop_duplicates().reset_index(drop=True)

        for index, row in df.iterrows():     
            num_exp = row.num_expediente
            print(f'Num expediente {num_exp}')

            if not exists_in_dict_list(num_exp, dl_raw):
            
                count_json_calls = count_json_calls+1
                print(count_json_calls)
                json_response = geo_speed_vals(num_exp, row.longitude ,row.latitude)

                if json_response['statusCode'] == 200:
                    dl_raw.append(json_response)

                    #Every time json calls match the threshold save everything
                    if count_json_calls%SAVEDATA_THRESHOLD==0:
                        print('saving data!')
                        write_to_file(dl_raw,speed_raw_file_json )

                else:
                    print(f"ERROR:Incorrect status code received {json_response['status']['code']}:{json_response['status']['message']} ")              
                    break
            else:
                print('already exists:' + num_exp)

        #Every time we call the APi we save it into a raw file so we don't need to call it again if we need to modify the data.
        write_to_file(dl_raw,speed_raw_file_json )                        

    #Data formatting step
    create_speed_data_set(dl_raw,speed_file_name)

