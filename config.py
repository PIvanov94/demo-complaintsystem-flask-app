from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from db import db
from resources.routes import routes


class DevApplicationConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )

class TestApplicationConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('TEST_DB_NAME')}"
    )


def create_app(config="config.DevApplicationConfig"):
    app = Flask(__name__)
    app.config.from_object(DevApplicationConfig)
    migrate = Migrate(app, db)
    CORS(app)
    api = Api(app)
    [api.add_resource(*r) for r in routes]
    return app