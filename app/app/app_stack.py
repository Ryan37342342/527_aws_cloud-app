from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    aws_s3 as s3,
    aws_cognito as cognito

)
import aws_cdk as cdk
from constructs import Construct


class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##################### stack is defined within here###################################################
        self.TempFileName()
        self.CreateUserPool()
        self.createEC2()

    def createEC2(self):
        vpc = ec2.Vpc(self, "Vpc",
                      cidr="10.0.0.0/16"
                      )
        vpc.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        security_group = ec2.SecurityGroup.from_security_group_id(self, "SG", "sg-066cfd8df5995eb98",
                                                                  mutable=False,
                                                                  )

            # create autoscaling group
        astro_auto_scaler = autoscaling.AutoScalingGroup(self, "Astro-auto-scaler",
                                                         instance_type=ec2.InstanceType("t2.micro"),
                                                         machine_image=ec2.MachineImage.generic_linux(
                                                             {"us-east-1": "ami-08fa7fd7b65f37ecb"}),
                                                         security_group=security_group,
                                                         vpc=vpc,
                                                         )
        astro_auto_scaler.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        # create application load balancer
        lb = elbv2.ApplicationLoadBalancer(self, "LB",
                                           vpc=vpc,
                                           internet_facing=True
                                           )
        lb.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        # Add a listener
        listener = lb.add_listener("Listener",
                                   port=80,
                                   open=True,
                                   )

        # Create an AutoScaling group and add it as a load balancing
        # target to the listener.
        listener.add_targets("ApplicationFleet",
                             port=8080,
                             targets=[astro_auto_scaler]
                             )
        listener.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
    def TempFileName(self):
        # bucket to store uploaded photos (lambda triggers on upload to this bucket)
        bucket_upload = s3.Bucket(self, "output-bucket",
                                  bucket_name="upload-picture-here",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,
                                  auto_delete_objects=True,
                                  block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                  )

        # bucket where the results are stored/returned
        bucket_results = s3.Bucket(self, "MAST-results-bucket57587787687",
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
                temp_password_validity=cdk.Duration.days(1)
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
        app_client.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        domain = cognito_userPool.add_domain("StarGuide-userPoolDomain",
                                             cognito_domain=cognito.CognitoDomainOptions(
                                                 domain_prefix="star-guide"
                                             ))
        domain.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
