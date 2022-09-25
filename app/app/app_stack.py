from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
    aws_s3 as s3,
    aws_cognito as cognito,
    Duration
)
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_s3_notifications as s3_notifications


class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##################### stack is defined within here###################################################
        self.TempFunctionName()
        self.CreateUserPool()

    def TempFunctionName(self):
        # bucket to store uploaded photos (lambda triggers on upload to this bucket)
        bucket_upload = s3.Bucket(self, "output-bucket",
                                  bucket_name="upload-picture-here",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,
                                  auto_delete_objects=True,
                                  block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                  )

        # bucket where the results are stored/returned
        bucket_results = s3.Bucket(self, "MAST-results-bucket575",
                                   bucket_name="mast-results-bucket575",
                                   removal_policy=cdk.RemovalPolicy.DESTROY,
                                   auto_delete_objects=True,
                                   block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                   )

    def CreateUserPool(self):
        # specify the configuration of the user pool
        cognito_userPool = cognito.UserPool(
            self, "StarGuide-userPool",
            user_pool_name="starguide-userPool",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            self_sign_up_enabled=True,
            user_verification=cognito.UserVerificationConfig(
                email_subject="Verify your StarGuide account!",
                email_body="Thanks for signing up to StarGuide! \n click {##Verify Email##} to verify your email.",
                email_style=cognito.VerificationEmailStyle.LINK
            ),
            sign_in_aliases=cognito.SignInAliases(
                username=True,
                email=True
            ),
            auto_verify=cognito.AutoVerifiedAttrs(
                email=True
            ),
            sign_in_case_sensitive=False,
            standard_attributes=cognito.StandardAttributes(
                fullname=cognito.StandardAttribute(
                    required=False,
                    mutable=True
                ),
                address=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                )
            ),
            mfa=cognito.Mfa.REQUIRED,
            mfa_second_factor=cognito.MfaSecondFactor(
                sms=False,
                otp=True
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True,
                temp_password_validity=Duration.days(1)
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
        )
        # app clients https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html
        app_client = cognito_userPool.add_client(
            "StarGuide-appClient",
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True
            ),
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO],
            read_attributes=cognito.ClientAttributes().with_standard_attributes(
                given_name=True,
                family_name=True,
                email=True,
                email_verified=True,
                address=True,
                birthdate=True,
                gender=True,
                locale=True,
                middle_name=True,
                fullname=True,
                nickname=True,
                profile_picture=True,
                preferred_username=True,
                profile_page=True,
                timezone=True,
                last_update_time=True,
                website=True
            ),
        )

        domain = cognito_userPool.add_domain("StarGuide-userPoolDomain",
                                             cognito_domain=cognito.CognitoDomainOptions(
                                                 domain_prefix="star-guide"
                                             ))
