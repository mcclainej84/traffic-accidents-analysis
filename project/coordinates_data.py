import pandas as pd
import pyproj

def transform_utm_lat_long(utm_easting,utm_northing):
    # Define the UTM zone and hemisphere (Northern Hemisphere: 'N', Southern Hemisphere: 'S')
    utm_zone = 30
    utm_hemisphere = 'N'

    # Create a pyproj transformer for UTM to latitude-longitude conversion
    utm_projection = pyproj.Proj(proj='utm', zone=utm_zone, ellps='WGS84', hemisphere=utm_hemisphere)
    wgs84_projection = pyproj.Proj(proj='latlong', ellps='WGS84')

    # Convert UTM coordinates to latitude and longitude
    long, lat = pyproj.transform(utm_projection, wgs84_projection, utm_easting, utm_northing)

    # Print the resulting latitude and longitude
    return long, lat

def main(original_df_filename, dest_df_filename):
    df = pd.read_csv( original_df_filename, sep= ";" )
    df['coordenada_x_utm'] = df['coordenada_x_utm'].str.replace(',', '.').astype(float)
    df['coordenada_y_utm'] = df['coordenada_y_utm'].str.replace(',', '.').astype(float)
    df['longitude'],df['latitude'] = transform_utm_lat_long(df['coordenada_x_utm'],df['coordenada_y_utm'])

    df.to_csv(dest_df_filename , index=False)