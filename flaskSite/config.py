import os

# ~~ Upload file content ~~
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
AWS_DEFAULT_REGION = 'eu-west-1'
AWS_COGNITO_DOMAIN = 'https://star-guide.auth.us-east-1.amazoncognito.com'
AWS_COGNITO_USER_POOL_ID = 'us-east-1_ehyW8ec2Y'
AWS_COGNITO_USER_POOL_CLIENT_ID = '3mdr87hipfio4lohsb8hf1sk8f'
AWS_COGNITO_USER_POOL_CLIENT_SECRET = '16vdl4683qpfk41t9a7rnqq51a4bd1dvtv1t0uoi0kq8fno0lqsg'
AWS_COGNITO_REDIRECT_URL = 'https://localhost:5000/aws_cognito_redirect'
