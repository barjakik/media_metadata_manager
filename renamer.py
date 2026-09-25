import os as os
import sys
from exif import Image
from datetime import datetime
from geopy.geocoders import Nominatim
import time
from pathlib import Path

prefix = sys.argv[1]

path = Path(prefix)
j = sum(1 for x in path.rglob('*') if x.is_file())  # Only files, recursive
i = 0

def dms_to_dd(gps_coords, gps_coords_ref):
    d, m, s =  gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd

def rename_directory_contents(prefix, dir):
    global i
    global j
    for file in os.listdir(prefix+dir):
        filename = os.fsdecode(file)
        if(os.path.isdir(prefix+dir+filename)) :
            rename_directory_contents(prefix + dir, filename + "/")
        else :
            _, ext = os.path.splitext(prefix+dir+filename)
            if ext != ".mp4" :
                i+= 1
                image = Image(prefix+dir+filename)
                if image.has_exif :
                    dt = datetime.strptime(image.datetime, "%Y:%m:%d %H:%M:%S")
                    foldername = str(dt.year) + f'{dt.month:02d}'
                    if dir == foldername + "/" :
                        path = prefix+dir
                    else:
                        if not os.path.isdir(prefix+dir+foldername) :
                            os.mkdir(prefix+dir+foldername)
                        path = prefix+dir+foldername+"/"
                    dt = datetime.strptime(image.datetime, "%Y:%m:%d %H:%M:%S")
                    if hasattr(image, 'gps_latitude') :
                        decimal_latitude = str(dms_to_dd(image.gps_latitude, image.gps_latitude_ref))
                        decimal_longitude = str(dms_to_dd(image.gps_longitude, image.gps_longitude_ref))
                        location = geolocator.reverse(str(dms_to_dd(image.gps_latitude, image.gps_latitude_ref))+","+str(dms_to_dd(image.gps_longitude, image.gps_longitude_ref)), language='en')
                        time.sleep(20) # To comply with Nominatim usage policy
                        if(location != None) :
                            if 'country' in location.raw['address'] :
                                country = location.raw['address'].get('country', '')
                            else :
                                country = 'N/A'
                            if 'hamlet' in location.raw['address'] :
                                city = location.raw['address'].get('hamlet', '')
                            else :
                                if 'village' in location.raw['address'] :
                                    city = location.raw['address'].get('village', '')
                                else :
                                    if 'town' in location.raw['address'] :
                                        city = location.raw['address'].get('town')
                                    else :
                                        if 'city' in location.raw['address'] :
                                            city = location.raw['address'].get('city', '')
                                        else :
                                            if 'municipality' in location.raw['address'] :
                                                city = location.raw['address'].get('municipality', '')
                                            else :
                                                city = 'N/A'
                            if 'state' in location.raw['address'] :
                                state = location.raw['address'].get('state', '')
                            else :
                                if 'county' in location.raw['address'] :
                                    state = location.raw['address'].get('county', '')
                                else :
                                    if 'region' in location.raw['address'] :
                                        state = location.raw['address'].get('country', '')
                                    else :
                                        state = 'N/A'
                            os.rename(prefix+dir+filename, path+dt.strftime("%Y-%m-%d %H:%M:%S") + " - " + country + ", " + state + ", " + city + ext)
                        else :
                            os.rename(prefix+dir+filename, path+dt.strftime("%Y-%m-%d %H:%M:%S") + ext)
                    else :
                        os.rename(prefix+dir+filename, path+dt.strftime("%Y-%m-%d %H:%M:%S") + ext)
    print(f'{prefix + dir} done; {i}/{j} files treated')

geolocator = Nominatim(user_agent="media_metadata_manager")

rename_directory_contents("", prefix+"/")

print(f'{i} photo names changed!\n')