import pandas as pd
import geopandas as gpd
import os
import requests
from ftplib import FTP
import re
import io

# Local directory to save the files
local_directory = "datasets"
os.makedirs(local_directory, exist_ok=True)  # Ensure the local directory exists

# FTP details and environment variables
ftp_host = os.getenv("FTP_HOST")
ftp_directory = os.getenv("FTP_DIRECTORY")
height_file_pattern = r"IDZ65910_\d+\.hcs"
height_file_path = os.path.join(local_directory, 'IDZ65910.csv')
height_file_header = [
    "IndexNo", "SensorType", "SensorDataType", "SiteIdType", "SiteId",
    "ObservationTimestamp", "RealValue", "Unit", "SensorParam1",
    "SensorParam2", "Quality", "Comment"
]

# Station file details
station_file_path = os.path.join(local_directory, 'rain_river_station_list.csv')
station_url = os.getenv("STATION_URL")


# Output filenames
geojson_file_path = os.path.join(local_directory, 'au_stream_gauges.geojson')
nsw_geojson_file_path = os.path.join(local_directory, 'nsw_stream_gauges.geojson')
gpkg_file_path = os.path.join(local_directory, 'au_stream_gauges.gpkg')

def get_stations():
    station_file_path = "datasets/rain_river_station_list.csv"
    if os.path.isfile(station_file_path):
        print(f"Found local file: {station_file_path}")
    else:
        print(f"File not found: {station_file_path}. Please ensure it is stored in the 'datasets' directory.")

def get_height():
    # Connect to FTP
    with FTP(ftp_host) as ftp:
        ftp.login()
        ftp.cwd(ftp_directory)
        files = ftp.nlst()

        # Match the latest file by pattern
        matching_files = [file_name for file_name in files if re.match(height_file_pattern, file_name)]
        latest_file = sorted(matching_files)[-1] if matching_files else None

        if latest_file:
            print(f"Downloading latest height file: {latest_file}")
            # Retrieve the file content into memory
            with io.BytesIO() as file_in_memory:
                ftp.retrbinary(f"RETR {latest_file}", file_in_memory.write)
                file_in_memory.seek(0)  # Reset pointer to the beginning of the file
                # Load directly into a DataFrame, skipping the first 8 rows
                df = pd.read_csv(file_in_memory, skiprows=8, header=None)
                df.columns = height_file_header
                print("Height data loaded into memory.")
                return df
        else:
            print("No matching files found on FTP server.")
            return None  # Return None if no file was found

def load_height():
    # Call get_height and return the data if available
    height_data = get_height()
    if height_data is None:
        print("Height data could not be loaded. Please check the FTP server and file pattern.")
    return height_data

def load_stations():
    station_file_path = "datasets/rain_river_station_list.csv"
    station_info = pd.read_csv(station_file_path)
    if 'SensorType' in station_info.columns:
        return station_info[station_info['SensorType'] == 'water level gauge']
    else:
        print("Error: 'SensorType' column not found.")
        return station_info  # Adjust as needed based on actual structure

def join_stations_with_height(stream_height_data, station_info):
    return pd.merge(stream_height_data, station_info, left_on="SiteId", right_on="SiteId")

def create_spatial_files(merged_data):
    gdf = gpd.GeoDataFrame(
        merged_data,
        geometry=gpd.points_from_xy(merged_data['Longitude'], merged_data['Latitude'])
    )
    gdf = gdf.set_crs("EPSG:4326")
    gdf.to_file(geojson_file_path, driver="GeoJSON")
    gdf[gdf['State'] == 'NSW'].to_file(nsw_geojson_file_path, driver="GeoJSON")
    gdf.to_file(gpkg_file_path, driver="GPKG", layer="stream_heights")

if __name__ == "__main__":
    get_stations()  # Check and print the status of the local file
    station_info = load_stations()
    get_height()
    stream_height_data = load_height()
    merged_data = join_stations_with_height(stream_height_data, station_info)
    create_spatial_files(merged_data)