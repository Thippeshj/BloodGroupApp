import os
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session handling

# Dummy credentials
USERNAME = "123"
PASSWORD = "123"

# Load trained model
MODEL_PATH = "blood_group_model.h5"
model = load_model(MODEL_PATH)

IMG_HEIGHT = 64
IMG_WIDTH = 64
class_labels = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

def predict_blood_group(img_path):
    img = image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return class_labels[predicted_class]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join("static/uploads", file.filename)
            os.makedirs("static/uploads", exist_ok=True)
            file.save(filepath)
            result = predict_blood_group(filepath)
            return render_template("index1.html", prediction=result, image_path=filepath)
    return render_template("index1.html", prediction=None, image_path=None)

if __name__ == "__main__":
    app.run(debug=True)