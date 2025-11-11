import os
import shutil

from flask import Flask, request, render_template, redirect, url_for

from prediction import predict_and_get_class_images
from settings import UPLOAD_FOLDER, MODEL, CLASS_NAMES, SAVE_CORRECT_PATH, SAVE_INCORRECT_PATH

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = UPLOAD_FOLDER / filename
            file.save(filepath)
            return redirect(url_for("result_page", filename=filename))
        else:
            return "Invalid file type. Only PNG and JPG are allowed.", 400
    return render_template("upload.html")


@app.route("/result/<filename>")
def result_page(filename):
    filepath = UPLOAD_FOLDER / filename
    pred_class, confidence = predict_and_get_class_images(filepath, MODEL, CLASS_NAMES)
    return render_template("result.html",
                           filename=filename,
                           pred_class=pred_class,
                           confidence=round(confidence * 100, 2))

@app.route("/save/<filename>", methods=["POST"])
def save_page(filename):
    filepath = UPLOAD_FOLDER / filename
    status = request.args.get("status")
    name = request.args.get("name")
    if status == "1":
        path = SAVE_CORRECT_PATH / name / filename
    else:
        path = SAVE_INCORRECT_PATH / name / filename
    os.makedirs(os.path.dirname(path), exist_ok=True)

    shutil.move(str(filepath), str(path))

    return redirect(url_for("upload_page"))

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True, port=5050)