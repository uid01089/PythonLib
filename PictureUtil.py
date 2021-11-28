from PIL import Image, ExifTags
from pathlib import Path

def getExif(path : Path)-> dict:
    
    exifData = {}

    image = Image.open(path)
    img_exif = image.getexif()
    if img_exif is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                exifData[ExifTags.TAGS[key]] = val
    
    return exifData

