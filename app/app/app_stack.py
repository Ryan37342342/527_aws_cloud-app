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

        # lambda function to access s3 bucket where data is stored
        fn = lambda_.Function(self, "get_data_from_hubble",
                              runtime=lambda_.Runtime.PYTHON_3_9,
                              code=lambda_.Code.from_asset("app/lambdas"),
                              handler="get_data_s3_hubble.get_data"
                              )
        bucket_upload = s3.Bucket(self, "output-bucket",
                                  bucket_name="upload-picture-here",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,
                                  auto_delete_objects=True,
                                  block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                  )
        # add an event to the bucket that triggers an event when a .mov file is uploaded
        bucket_upload.add_event_notification(s3.EventType.OBJECT_CREATED,
                                             s3_notifications.LambdaDestination(fn)
                                             )

        bucket_results = s3.Bucket(self, "MAST-results-bucket575",
                                   bucket_name="mast-results-bucket575",
                                   removal_policy=cdk.RemovalPolicy.DESTROY,
                                   auto_delete_objects=True,
                                   block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                   )
