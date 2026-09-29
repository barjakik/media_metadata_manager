import os as os
import sys
from exif import Image
from datetime import datetime
from geopy.geocoders import Nominatim
import time
from pathlib import Path
import pandas as pd

i = 0

tot = 0

prefix = sys.argv[1]

data = {}

if prefix[-1] != '/' :
    prefix = prefix + '/'

path = Path(prefix)
j = sum(1 for x in path.rglob('*') if x.is_file())

def dms_to_dd(gps_coords, gps_coords_ref):
    d, m, s =  gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd

def treat_metadata(prefix, dir):
    global i
    global j
    global tot
    global data
    for file in os.listdir(prefix+dir):
        filename = os.fsdecode(file)
        if(os.path.isdir(prefix+dir+filename)) :
            treat_metadata(prefix + dir, filename + "/")
        else :
            tot += 1
            _, ext = os.path.splitext(prefix+dir+filename)
            if ext != ".mp4" :
                image = Image(prefix+dir+filename)
                if image.has_exif and hasattr(image, 'gps_latitude'):
                    dt = datetime.strptime(image.datetime, "%Y:%m:%d %H:%M:%S")
                    decimal_latitude = str(dms_to_dd(image.gps_latitude, image.gps_latitude_ref))
                    decimal_longitude = str(dms_to_dd(image.gps_longitude, image.gps_longitude_ref))
                    location = geolocator.reverse(str(dms_to_dd(image.gps_latitude, image.gps_latitude_ref))+","+str(dms_to_dd(image.gps_longitude, image.gps_longitude_ref)), language='en')
                    time.sleep(20) # To comply with Nominatim usage policy
                    if(location != None) :
                        i+= 1
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
                        if city in data:
                            if data[city]["firstvis"] > dt :
                                data[city]["firstvis"] = dt
                            if data[city]["lastvis"] < dt :
                                data[city]["lastvis"] = dt
                        else :
                            data[city] = {"country": country, "state": state, "firstvis": dt, "lastvis": dt}
                        
    print(f'{prefix + dir} done; {tot}/{j} files treated')

geolocator = Nominatim(user_agent="media_metadata_manager")

treat_metadata("", prefix)

df = pd.DataFrame.from_dict(data, orient='index', columns=["city", "country", "state", "firstvis", "lastvis"])

df.to_csv(f'{prefix}.csv')

print(f'{i} photos used!\n')