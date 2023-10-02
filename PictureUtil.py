# This class provides utility functions for extracting Exif metadata from images.
from PIL import Image, ExifTags
from pathlib import Path


def getExif(path: Path) -> dict:
    """
    Get Exif metadata from an image file.

    Args:
        path (Path): The path to the image file.

    Returns:
        dict: A dictionary containing Exif metadata, where keys are metadata tags and values are their corresponding values.
    """
    exifData = {}

    image = Image.open(path)
    img_exif = image.getexif()
    if img_exif is None:
        print('Sorry, the image has no Exif data.')
    else:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                exifData[ExifTags.TAGS[key]] = val

    return exifData
