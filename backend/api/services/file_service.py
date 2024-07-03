import os
from docx import Document
from utils.singleton_file import SingletonFile

UPLOAD_FOLDER = 'data/contracts/'
ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, filename):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Load file content into the singleton
    document = Document(file_path)
    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)
    content = '\n'.join(full_text)
    
    singleton_file = SingletonFile()
    singleton_file.set_file_content(content)

    return file_path

def get_file_content():
    singleton_file = SingletonFile()
    return singleton_file.get_file_content()
