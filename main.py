from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap5
import os
import numpy as np
from PIL import Image

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = "cnfkkc"

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # Add your allowed file extensions here
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

colors = {}

@app.route("/")
def home():
    return render_template('web.html', color= colors)

def palette():
    global color, colors
    numbers = {}
    image = Image.open('static/color.png')
    image_array = np.array(image)
    x, y, channels = image_array.shape
    for i in range(x):
        for j in range(y):
            red_value = image_array[i, j, 0]
            green_value = image_array[i, j, 1]
            blue_value = image_array[i, j, 2]
            rgb_values = (red_value, green_value, blue_value)
            if rgb_values in numbers:
                numbers[rgb_values]["count"] += 1
            else:
                numbers[rgb_values] = {"count": 1}

    sorted_numbers = sorted(numbers.items(), key=lambda item: item[1]["count"], reverse=True)
    colors = sorted_numbers[:6]
    print(colors)


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file part'

    file = request.files['image']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        new_filename = 'color.png'  # Set your own custom filename here
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        palette()
        return redirect('/')

    else:
        return 'Invalid file'


if __name__ == "__main__":
    app.run(debug=True)