from flask import Flask, request, send_from_directory, jsonify, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Mimic some processing (for simplicity, renaming the file)
        new_filename = os.path.splitext(filename)[0] + "_processed" + os.path.splitext(filename)[1]
        os.rename(filename, new_filename)
        
        return jsonify({"message": "Processing completed", "filename": new_filename}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
