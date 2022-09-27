import subprocess
from astroquery.mast import Zcut, Tesscut
from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
from exif import Image
from astroquery.vo_conesearch import ConeSearch, conesearch


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


def get_data(imagepath):
    # send image to s3 bucket
    subprocess.run("aws s3 cp " + imagepath + " s3://upload-picture-here")
    # read image
    data = image_coordinates(imagepath)

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
    image_count = Observations.query_criteria_count(dataproduct_type=["image"], coordinates=cutout_coord)
    if image_count != 0:
        table_images = Observations.query_criteria(dataproduct_type=["image"], coordinates=cutout_coord,  calib_level=["2","3"])
        product_list = Observations.get_product_list(table_images)
        products = Observations.filter_products(product_list,
                                                productType=["PREVIEW"],
                                                obs_collection=["HLA","JWST","GALEX"]
                                                )

        manifest = Observations.download_products(products[:10],cloud_only=True)
        #print(products)

    else:
        print("no images found at this location")


if __name__ == "__main__":
    get_data()
