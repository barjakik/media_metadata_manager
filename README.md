# media_metadata_manager
A set of small programs written in python that help rename files according to their EXIF or ffmpeg metadata, and map them out on a world map.

Currently only works with images; video files are to come soon. The files get renamed to the yyyy-mm-dd HH:MM:SS model, followed by the Country, Region and City the photo was taken in if possible. Creates directories for the photos in the form yyyymm to organise them more clearly. Ignores photos without exif data.

Required libraries :
- numpy
- exif
- plotly
- geopy
- ffmpeg-python (!NOT python-ffmpeg!)

Use :
python3 map.py [DIR] to create a html file of a map of the world with the locations found in the metadata of all photos in [DIR] and its subfolders using plotly.

python3 renamer.py [DIR] to change the names of all image and video files in [DIR] and all its subdirectories to the yyyy-mm-dd HH:MM:SS model, with the addition of Country, Region, City wherever applicable.

python3 renamer_no_loc.py [DIR] to change the names of all image and video files in [DIR] and all its subdirectories to the yyyy-mm-dd HH:MM:SS model without querying for the location
python3 metadata_treater.py [DIR] to get 

python3 metadata_treater.py [DIR] to get the cities of all photos with location metadata in [DIR] and all its subdirectories, and return them into a [DIR].csv file

# TO BE ADDED :

- figure out if ffmpeg can have location metadata
- find a way to deal with edited files and others that do not feature EXIF data
- potentially compile for ease of use?