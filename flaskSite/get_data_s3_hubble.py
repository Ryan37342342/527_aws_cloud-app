import subprocess
from astroquery.mast import Zcut
from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
from exif import Image


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,
                                     img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                                     img.gps_longitude_ref))
        except AttributeError:
            print('No Coordinates')
    else:
        print('The Image has no EXIF information')

    return (coords)


def get_data():
    # send image to s3 bucket
    # subprocess.run("aws s3 cp " + imagepath + " s3://upload-picture-here")
    # read image
    #data = image_coordinates(imagepath)
    data = [-70.50919, 107.18696]
    if data != "":
        print(data)
        lat = data[1]
        lon = data[0]
    else:
        print("no gps data found")
    # extract data from image
    # enable dataset
    Observations.enable_cloud_dataset()
    cutout_coord = SkyCoord(lat, lon, unit="deg")
    # get fits image
    manifest = Zcut.download_cutouts(coordinates=cutout_coord, size=[200, 300], units="px")
    # display fits image

if __name__ == "__main__":
    get_data()