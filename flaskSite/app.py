import os
from flask import Flask, jsonify, render_template, url_for, redirect, make_response, send_from_directory, request
from flask_awscognito import AWSCognitoAuthentication
from werkzeug.utils import secure_filename
from get_data_s3_hubble import get_data
from flask_cors import CORS
from jwt.algorithms import RSAAlgorithm
import config
from flask_jwt_extended import (
    JWTManager,
    set_access_cookies,
    verify_jwt_in_request,
    get_jwt_identity
)

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


@app.route('/uploadUserImage', methods=['POST', 'GET'])
def uploadUserImage():
    # check if user is signed in
    verify_jwt_in_request(optional=True)
    if not get_jwt_identity(): 
        return redirect(aws_auth.get_sign_in_url())
    # otherwise continue
    if request.method == 'POST':
        if 'uploadUserImage' not in request.files: 
            return redirect(request.url)
        userImage = request.files['uploadUserImage']        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if userImage.filename == '': 
            return redirect(request.url)
        if userImage and allowed_file(userImage.filename):
            userUploadfilename = secure_filename(userImage.filename)
            userImagePath = os.path.join(app.config['UPLOAD_FOLDER'], userUploadfilename)
            userImage.save(userImagePath)
            #get_data(userImagePath)
            return redirect(url_for('userIndex', filename=userUploadfilename))
    return render_template("userIndex.html")


@app.route('/uploads/<filename>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/userIndex/<filename>')
def userIndex(filename):
    print(filename)
    if filename == "e": 
        return render_template("userIndexEMPTY.html")
    else :
        return render_template("userIndex.html", userUploadedImage = filename)

# ~~ Cognito authentication content ~~ WIP
app.config.from_object(config)
app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(config.get_cognito_public_keys())

CORS(app)
aws_auth = AWSCognitoAuthentication(app)
jwt = JWTManager(app)

@app.route('/signInPage')
def signInPage():
    return redirect(aws_auth.get_sign_in_url())

@app.route('/aws_cognito_redirect', methods=['GET'])
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    resp = make_response(redirect(url_for("protected")))
    set_access_cookies(resp, access_token, max_age=30 * 60)
    print("Cookies set!")
    return resp


@app.route("/userIndex")
def protected():
    verify_jwt_in_request()
    if get_jwt_identity():
        return redirect(url_for("userIndex", filename="e"))
    else:
        print("not signed in")
        return redirect(aws_auth.get_sign_in_url())
