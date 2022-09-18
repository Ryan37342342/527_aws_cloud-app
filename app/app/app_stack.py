from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
    aws_s3 as s3,
)
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_s3_notifications as s3_notifications


class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##################### stack is defined within here###################################################

        # create a layer for packages (installed at app/app/layers)
        layer = lambda_.LayerVersion(self, 'astro_layer',
                                     code=lambda_.Code.from_asset("app/layer/"),
                                     description='packages for mast lambda',
                                     compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
                                     removal_policy=cdk.RemovalPolicy.DESTROY
                                     )
        # lambda function to access s3 bucket where data is stored
        fn = lambda_.Function(self, "get_data_from_hubble",
                              runtime=lambda_.Runtime.PYTHON_3_9,
                              code=lambda_.Code.from_asset("app/lambdas"),
                              handler="get_data_s3_hubble.get_data",
                              layers=[layer],
                              )
        #bucket to store uploaded photos (lambda triggers on upload to this bucket)
        bucket_upload = s3.Bucket(self, "output-bucket",
                                  bucket_name="upload-picture-here",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,
                                  auto_delete_objects=True,
                                  block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                  )
        # add an event to the bucket that triggers an event when anything is uploaded to it
        bucket_upload.add_event_notification(s3.EventType.OBJECT_CREATED,
                                             s3_notifications.LambdaDestination(fn)
                                             )
        #bucket where the results are stored/returned
        bucket_results = s3.Bucket(self, "MAST-results-bucket575",
                                   bucket_name="mast-results-bucket575",
                                   removal_policy=cdk.RemovalPolicy.DESTROY,
                                   auto_delete_objects=True,
                                   block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                   )
