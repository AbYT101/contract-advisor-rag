from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

from api import routes  # Import routes after creating the app
