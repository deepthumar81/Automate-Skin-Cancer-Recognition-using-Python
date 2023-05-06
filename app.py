# Importing required libs
from flask import Flask, render_template, request
# from model import preprocess_img, predict_result
# from Mo import predict_image_class
# import sys
from PIL import Image
import io
import os

from module import Mo

# sys.path.insert(1, '/module')

# Instantiating flask app
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Home route


@app.route("/")
def main():
    return render_template("index.html")


# Prediction route
@app.route('/prediction', methods=['POST'])
def predict_image_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return render_template("result.html", err="Only .jpg .jpeg .png files are allowed")

            pred = Mo.predict_image_class(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            return render_template("result.html", predictions=str(pred))

    except Exception as e:
        error = "File cannot be processed."
        return render_template("result.html", err=error)


if __name__ == "__main__":
    app.run(port=9000, debug=True)
