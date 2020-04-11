import os


def configure(app):
    CONN_STRING = os.environ.get('SQLALCHEMY_CONNECTION')

    if CONN_STRING is None:
        raise Exception(
            """Please set the "SQLALCHEMY_CONNECTION" environment variable
            before starting the application""")

    UPLOAD_FOLDER = 'uploads'

    app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STRING
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
