from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import CORS, cross_origin
from api.services import retriever_service, generator_service, file_service, evaluation_service
from werkzeug.utils import secure_filename

bp = Blueprint('rag', __name__)
CORS(bp)

@bp.route('/upload', methods=['POST'])
# @jwt_required()
@cross_origin(origin='*')
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

@bp.route('/generate', methods=['POST'])
# @jwt_required()
@cross_origin(origin='*')
def generate():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"error": "Question not provided"}), 400

    retriever = retriever_service.create_retriever()
    response = generator_service.generate(question, retriever)
    return jsonify({"response": response}), 200


@bp.route('/evaluate', methods=['POST'])
# @jwt_required()
@cross_origin(origin='*')
def evaluate():
    data = request.get_json()
    # question = data.get('question')
    # if not question:
    #     return jsonify({"error": "Question not provided"}), 400

    response = evaluation_service.main()
    return jsonify({"response": response}), 200