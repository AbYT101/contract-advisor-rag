class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:123456@DESKTOP-AFEFNC1/RAG?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'secret_key'
