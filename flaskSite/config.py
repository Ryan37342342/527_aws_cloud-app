import json
import requests
import os
# ~~ Upload file content ~~
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# ~~ Cognito content ~~
AWS_DEFAULT_REGION = 'us-east-1'
AWS_COGNITO_DOMAIN = 'https://star-guide.auth.us-east-1.amazoncognito.com'
AWS_COGNITO_USER_POOL_ID = 'us-east-1_E26zHv04u'
AWS_COGNITO_USER_POOL_CLIENT_ID = '7kj5hea8kt59k8tt8lqkrgnens'
AWS_COGNITO_USER_POOL_CLIENT_SECRET = '1ocdos5tajqvr5j14a81v6a97k8kmiis2l39kv4bra7irbeudi3r'
AWS_COGNITO_REDIRECT_URL = 'http://localhost:5000/aws_cognito_redirect'
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_CSRF_PROTECT = False
JWT_COOKIE_SECURE = True
JWT_SECRET_KEY = os.urandom(16)
JWT_ALGORITHM = "RS256"

def get_cognito_public_keys():
    url = f"https://cognito-idp.{AWS_DEFAULT_REGION}.amazonaws.com/{AWS_COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    resp = requests.get(url)
    return json.dumps(json.loads(resp.text)["keys"][1])