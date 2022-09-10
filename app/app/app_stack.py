from aws_cdk import (
aws_lambda as lambda_,
    Stack,

)
from astroquery.mast import Observations
from constructs import Construct
import json
import boto3
class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # lambda function to access s3 bucket where data is stored
        fn = lambda_.Function(self, "get_data_from_hubble",
                              runtime=lambda_.Runtime.PYTHON_3_9,
                              code=lambda_.Code.from_asset("app/lambdas"),
                              handler="get_data_s3_hubble.get_data"
                              )
