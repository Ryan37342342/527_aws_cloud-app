import os

# ~~ Upload file content ~~
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
AWS_DEFAULT_REGION = 'eu-west-1'
AWS_COGNITO_DOMAIN = 'https://star-guide.auth.us-east-1.amazoncognito.com'
AWS_COGNITO_USER_POOL_ID = 'us-east-1_ehyW8ec2Y'
AWS_COGNITO_USER_POOL_CLIENT_ID = '7kj5hea8kt59k8tt8lqkrgnens'
AWS_COGNITO_USER_POOL_CLIENT_SECRET = '1ocdos5tajqvr5j14a81v6a97k8kmiis2l39kv4bra7irbeudi3r'
AWS_COGNITO_REDIRECT_URL = 'https://localhost:5000/aws_cognito_redirect'
