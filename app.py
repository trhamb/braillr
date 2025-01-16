from flask import Flask, render_template, request, send_file, jsonify
from tools.text_to_png import text_to_png
from tools.png_to_stl import png_to_stl
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if not os.path.exists('outputs'):
    os.makedirs('outputs')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        text = request.form.get('text')
        baseplate = request.form.get('baseplate') == 'true'
        
        if text:
            png_name = os.path.join('outputs', f"{text}.png")
            stl_name = os.path.join('outputs', f"{text}.stl")
            
            png_file = text_to_png(text, png_name)
            stl_file = png_to_stl(png_file, stl_name, height_scale=5.0, size_scale=0.5, baseplate=baseplate)
            return jsonify({'stl_path': os.path.basename(stl_file)})
        return jsonify({'error': 'No text provided'}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('outputs', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
