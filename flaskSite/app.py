import os
from flask import Flask, jsonify, render_template, url_for, redirect, make_response, request
from flask_awscognito import AWSCognitoAuthentication
from werkzeug.utils import secure_filename
from get_data_s3_hubble import get_data
import config

app = Flask(__name__)


if __name__ == "__main__":
    app.debug=True
    app.run()

# ~~ main website content ~~
@app.route('/')
def index():
    return render_template('index.html')

# ~~ Upload file content ~~
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/uploadUserImage', methods=['POST'])
def uploadUserImage():
    if request.method == 'POST':
        if 'uploadUserImage' not in request.files: return redirect(request.url)
        userImage = request.files['uploadUserImage']        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if userImage.filename == '': return redirect(request.url)
        if userImage and allowed_file(userImage.filename):
            filename = secure_filename(userImage.filename)
            userImagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            userImage.save(userImagePath)
            get_data(userImagePath)
            return redirect(url_for('userIndex', name=filename))
    return render_template("userIndex.html")

# ~~ Cognito authentication content ~~ WIP

app.config['AWS_DEFAULT_REGION'] = config.AWS_DEFAULT_REGION
app.config['AWS_COGNITO_DOMAIN'] = config.AWS_COGNITO_DOMAIN
app.config['AWS_COGNITO_USER_POOL_ID'] = config.AWS_COGNITO_USER_POOL_ID
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = config.AWS_COGNITO_USER_POOL_CLIENT_ID
app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = config.AWS_COGNITO_USER_POOL_CLIENT_SECRET
app.config['AWS_COGNITO_REDIRECT_URL'] = config.AWS_COGNITO_REDIRECT_URL

aws_auth = AWSCognitoAuthentication(app)

@app.route('/signInPage')
def signInPage():
    return redirect(aws_auth.get_sign_in_url())

@app.route('/aws_cognito_redirect')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    return jsonify({'access_token': access_token})

@app.route('/')
@aws_auth.authentication_required
def userIndex():
    claims = aws_auth.claims
    return jsonify({'claims': claims})
