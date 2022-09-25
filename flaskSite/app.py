import os
from flask import Flask, render_template, url_for, redirect, make_response, request
from flask_jwt_extended import JWTManager, set_access_cookies, verify_jwt_in_request, get_jwt_identity
from flask_awscognito import AWSCognitoAuthentication
from flask_cors import CORS
from jwt.algorithms import RSAAlgorithm
from werkzeug.utils import secure_filename
from get_data_s3_hubble import get_data
import config
import keys

app = Flask(__name__)


if __name__ == "__main__":
    app.debug=True
    app.run()

# ~~ main website content ~~
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signInPage')
def signInPage():
    return render_template('signInPage.html')


# ~~ Upload file content ~~
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/uploadUserImage', methods=['POST'])
def uploadUserImage():
    print("passed function entry check")
    if request.method == 'POST':
        print("passed POST check")
        if 'uploadUserImage' not in request.files: return redirect(request.url + "failed not in request.files check")
        print("passed not in request.files check")
        userImage = request.files['uploadUserImage']        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if userImage.filename == '': return redirect(request.url + "failed filename empty check")
        print("passed filename empty check")
        if userImage and allowed_file(userImage.filename):
            print("passed filename type allowed check")
            filename = secure_filename(userImage.filename)
            userImagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            userImage.save(userImagePath)
            get_data(userImagePath)
            return redirect(url_for('userIndex', name=filename))
    print("failed request check")        
    return render_template("userIndex.html")

# ~~ Cognito authentication content ~~ WIP

app.config.from_object("config")
app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(keys.get_cognito_public_keys())

CORS(app)
aws_auth = AWSCognitoAuthentication(app)
jwt = JWTManager(app)


@app.route("/signUserIn", methods=["GET", "POST"])
def signUserIn():
    return redirect(aws_auth.get_sign_in_url())


@app.route("/signedIn", methods=["GET"])
def logged_in():
    access_token = aws_auth.get_access_token(request.args)
    resp = make_response(redirect(url_for("protected")))
    set_access_cookies(resp, access_token, max_age=30 * 60)
    return resp


@app.route("/userIndex")
def protected():
    verify_jwt_in_request()
    if get_jwt_identity():
        return render_template("userIndex.html")
    else:
        return redirect(aws_auth.get_sign_in_url())