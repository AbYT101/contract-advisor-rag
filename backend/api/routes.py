from flask import request, jsonify
from werkzeug.utils import secure_filename
from . import app
from .services import retriever_service, generator_service, file_service

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file_service.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = file_service.save_file(file, filename)
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/api/retrieve', methods=['POST'])
def retrieve():
    contract_text = file_service.get_file_content()
    if contract_text is None:
        return jsonify({"error": "No file content available"}), 400
    results = retriever_service.retrieve(contract_text)
    return jsonify(results)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    question = data.get('question')
    context = file_service.get_file_content()
    if context is None:
        return jsonify({"error": "No file content available"}), 400
    response = generator_service.generate(question, context)
    return jsonify(response)
