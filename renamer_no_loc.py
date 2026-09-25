import os as os
import sys
from exif import Image
from datetime import datetime
from pathlib import Path

i = 0

prefix = sys.argv[1]

path = Path(prefix)
j = sum(1 for x in path.rglob('*') if x.is_file())

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
            i+= 1
            if ext != ".mp4" :
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
                    os.rename(prefix+dir+filename, path+dt.strftime("%Y-%m-%d %H:%M:%S") + ext)
    print(f'{prefix + dir} done; {i}/{j} files treated')


rename_directory_contents("", prefix+"/")

print(f'{i} photo names changed!\n')