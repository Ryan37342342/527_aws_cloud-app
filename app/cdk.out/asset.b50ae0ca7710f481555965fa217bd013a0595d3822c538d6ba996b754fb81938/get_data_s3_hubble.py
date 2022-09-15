import json
from astroquery.mast import Observations
import boto3
import os


def get_data():
    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-1",

    )


# Query MAST for some WFC3 data
obsTable = Observations.query_criteria(project='HST',
                                       filters='F160W',
                                       instrument_name='WFC3/IR')

# Grab 100 products:
# http://astroquery.readthedocs.io/en/latest/mast/mast.html#getting-product-lists
products = Observations.get_product_list(obsTable[:100])

# Filter out just the drizzled FITS files
filtered_products = Observations.filter_products(products,
                                                 mrp_only=False,
                                                 productSubGroupDescription='DRZ')

# Use AWS S3 URLs for the MAST records (rather than the ones at http://mast.stsci.edu)
Observations.enable_s3_hst_dataset()

# We want URLs like this: s3://stpubdata/hst/public/ibg7/ibg705080/ibg705081_drz.fits
s3_urls = Observations.get_hst_s3_uris(filtered_products)

# Auth to create a Lambda function
session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secert_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)
client = session.client('lambda', region_name='us-east-1')

# Loop through the URLs for the data on S3
# 'your-output-bucket' is where you want to the Lambda outputs to be written
# FunctionName is the name of the Lambda function you made earlier.
for url in s3_urls:
    fits_s3_key = url.replace("s3://stpubdata/", "")
    event = {
        'fits_s3_key': fits_s3_key,
        'fits_s3_bucket': 'stpubdata',
        's3_output_bucket': ''  # <- change this to your output bucket
    }

    # Invoke Lambda function
    response = client.invoke(
        FunctionName='SEPFunction',
        InvocationType='Event',
        LogType='Tail',
        Payload=json.dumps(event)
    )
