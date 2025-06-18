import os
from flask import Flask, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_total_price(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    lines = text.split("\n")
    total_price = None
    for line in lines:
        if "receipt total" in line.lower():
            numbers = [float(s) for s in line.split() if s.replace('.', '', 1).isdigit()]
            if numbers:
                total_price = max(numbers)
    return total_price

@app.route('/', methods=['GET', 'POST'])
def index():
    total_price = None
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)
            total_price = extract_total_price(image_path)
    return render_template('index.html', total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
