import configparser
import pandas as pd
import requests
import json
import os

def get_api_key():
    config = configparser.ConfigParser()
    config.read('api_keys.cfg')
    return config.get('opendata', 'opendata_api_key')

def geo_reverse(num_exp, long, lat):
    geo = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{long}&key={get_api_key()}").json()
    geo["num_expediente"] = num_exp
    return(geo)

def get_data_extracted(row):
    #return item['num_expediente']
    return (
        row['num_expediente'],
        row['status']['code'],
        row['status']['message'],
        row['timestamp']['created_http'],
        row['total_results']         ,
        row['results'][0]['annotations'].get('geohash'),
        row['results'][0]['annotations']['roadinfo']['road'],
        row['results'][0]['components'].get('city'),
        row['results'][0]['components']['country_code'],
        row['results'][0]['components']['_category'],
        row['results'][0]['components']['_type'],
        row['results'][0]['components'].get('house_number'),
        row['results'][0]['components'].get('postcode') ,
        row['results'][0]['components'].get('suburb'),
        row['results'][0]['components'].get('quarter'),
        row['results'][0]['components']['road'],
        row['results'][0]['formatted'],
        row['results'][0]['confidence'],
        row['results'][0]['geometry']['lat'],
        row['results'][0]['geometry']['lng']
    )

def create_geodata_set(dl_raw ,geodata_file_name ):
    column_names= ['num_expediente',
            'status_code',
            'status_message',
            'api_timestamp',
            'total_results',
            'geohash',
            'road_info',
            'city',
            'country_code',
            'category',
            'type',
            'house_number',
            'postcode',
            'suburb',
            'quarter',
            'road',
            'formatted',
            'confidence',
            'latitude_api',
            'longitude_api']    

    dl = [  get_data_extracted(item) for item in dl_raw]
    df = pd.DataFrame(dl, columns = column_names)
    df.set_index('num_expediente', inplace=True)
    df.to_csv(geodata_file_name)


def exists_in_dict_list(num_exp,dl_raw):
    exp_list = set(item['num_expediente']for item in dl_raw)

    if num_exp in exp_list:
        return True
    else:
        return False

def write_to_file(dl , filename):
    #Create a new file with data
    with open(filename, "w") as file:
        json.dump(dl, file, indent=4)

"""PARAMS:
    call_api => If set to TRUE will call the API. Otherwise just skip the API part and transform raw data into a formatted dataset
"""
def main(call_api, original_df_filename,geodata_file_name,geodata_raw_file_json):
    #Declare variables
    SAVEDATA_THRESHOLD = 50  #Threshold for saving the data into a file after X json calls.
    TOTAL_CALLS= 2450
    count_json_calls= 0 #Counter for the json calls to the API. 
    column_list = ['num_expediente', 'latitude' , 'longitude']

    try:
        with open(geodata_raw_file_json, "r") as file:
            dl_raw = json.load(file)
    except IOError:
        dl_raw = []

    #API processing step
    if call_api:            
        #read csv file
        df = pd.read_csv(original_df_filename)[column_list].drop_duplicates().reset_index(drop=True)

        for index, row in df.iterrows():     
            num_exp = row.num_expediente

            if not exists_in_dict_list(num_exp, dl_raw):
                
                count_json_calls = count_json_calls+1
                print(count_json_calls)
                json_response = geo_reverse(num_exp, row.longitude ,row.latitude)

                if json_response['status']['code'] == 200:
                    dl_raw.append(json_response)

                    #Every time json calls match the threshold save everything
                    if count_json_calls%SAVEDATA_THRESHOLD==0:
                        print('saving data!')
                        write_to_file(dl_raw,geodata_raw_file_json )

                else:
                    print(f"ERROR:Incorrect status code received {json_response['status']['code']}:{json_response['status']['message']} ")              
                    break
            else:
                print('already exists:' + num_exp)

            if count_json_calls >=TOTAL_CALLS:
                break
            
        #Every time we call the APi we save it into a raw file so we don't need to call it again if we need to modify the data.
        write_to_file(dl_raw,geodata_raw_file_json )


    #Data formatting step
    create_geodata_set(dl_raw,geodata_file_name)

