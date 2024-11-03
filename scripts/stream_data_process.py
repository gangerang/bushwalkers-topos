import pandas as pd
import geopandas as gpd
import os
import requests
from ftplib import FTP
import re

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
    # Attempt to download and read the station file directly into a DataFrame
    response = requests.get(station_url)
    if response.status_code == 200:
        # Load data into a DataFrame directly without saving to disk
        station_info = pd.read_csv(pd.compat.StringIO(response.text))
        print("Station data loaded in memory.")
        return station_info
    else:
        print("Failed to download station file. Status code:", response.status_code)
        return None  # Return None if the download fails


def get_height():
    with FTP(ftp_host) as ftp:
        ftp.login()
        ftp.cwd(ftp_directory)
        files = ftp.nlst()
        matching_files = [file_name for file_name in files if re.match(height_file_pattern, file_name)]
        latest_file = sorted(matching_files)[-1] if matching_files else None

        if latest_file:
            csv_file_path = os.path.join(local_directory, latest_file.replace('.hcs', '.csv'))
            with open(latest_file, "wb") as temp_file:
                ftp.retrbinary(f"RETR {latest_file}", temp_file.write)

            df = pd.read_csv(latest_file, skiprows=8, header=None)
            df.columns = height_file_header
            df.to_csv(csv_file_path, index=False)
            df.to_csv(height_file_path, index=False)
            os.remove(latest_file)
        else:
            print("No matching files found on FTP server.")

def load_height():
    return pd.read_csv(height_file_path)

def load_stations():
    station_info = get_stations()  # Call get_stations and get the data directly
    if station_info is not None:
        # Ensure the DataFrame has the expected columns before filtering
        if 'SensorType' in station_info.columns:
            return station_info[station_info['SensorType'] == 'water level gauge']
        else:
            print("Error: 'SensorType' column not found.")
            return station_info  # Adjust as needed based on actual structure
    else:
        print("No station data available.")
        return None


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
    # Get station data
    station_info = load_stations()
    if station_info is None:
        print("Station data could not be loaded. Exiting script.")
    else:
        # Proceed with remaining operations only if station data is available
        get_height()
        stream_height_data = load_height()
        merged_data = join_stations_with_height(stream_height_data, station_info)
        create_spatial_files(merged_data)