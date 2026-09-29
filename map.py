import os as os
import sys
from exif import Image
import numpy as np
import plotly
import plotly.express as px
from pathlib import Path

def dms_to_dd(gps_coords, gps_coords_ref):
    d, m, s =  gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd

it = 0
i = 0

prefix = sys.argv[1]

if prefix[-1] != '/' :
    prefix = prefix + '/'

path = Path(prefix)
j = sum(1 for x in path.rglob('*') if x.is_file())

def get_dir_coords(prefix, directory) :
    global it
    global j
    global i
    lats = np.ndarray([])
    longs = np.ndarray([])
    for file in os.listdir(prefix + directory):
        filename = os.fsdecode(file)
        if(os.path.isdir(prefix+directory+filename)) :
            lat2, long2 = get_dir_coords(prefix + directory, filename + "/")
            lats = np.append(lats, lat2)
            longs = np.append(longs, long2)
            continue
        else :
            _, ext = os.path.splitext(prefix+directory+filename)
            im = True
            try :
                image = Image(prefix+dir+filename)
            except KeyboardInterrupt :
                return
            except:
                im = False
            if im and image.has_exif and hasattr(image, 'gps_latitude') :
                decimal_latitude = str(dms_to_dd(image.gps_latitude, image.gps_latitude_ref))
                decimal_longitude = str(dms_to_dd(image.gps_longitude, image.gps_longitude_ref))
                lats= np.append(lats, decimal_latitude)
                longs = np.append(longs, decimal_longitude)
                i += 1
        it += 1
    print(f'{prefix + directory} done; {it}/{j} files treated')
    return (lats, longs)

lats, longs = get_dir_coords("", prefix)

fig = px.scatter_geo(lat=lats,lon=longs)
fig.update_geos(resolution=50)
plotly.offline.plot(fig, filename=f'{prefix[:-1]}.html')

print(f'{i} photo(s) with location metadata found!\n')