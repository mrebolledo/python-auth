import sqlalchemy
import ssl
from dotenv import load_dotenv
import os
import redis


load_dotenv()

class ApplicationConfig:

    SECRET_KEY = os.environ['SECRET_KEY']

    SESSION_TYPE="redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

    database_uri = sqlalchemy.engine.url.URL.create(
                            drivername="postgresql+pg8000",
                            username=os.environ["DB_USER"],
                            password=os.environ["DB_PASS"],
                            host=os.environ["DB_HOST"],
                            port=int(os.environ["DB_PORT"]),
                            database=os.environ["DB_NAME"],
    )

    if os.environ['ENVIRONMENT'] == 'local':
        ssl_args = None
    else:
        ssl_context = ssl.SSLContext()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_verify_locations(os.environ["SSL_CA_POSTG"])
        ssl_context.load_cert_chain(os.environ["SSL_CERT_POSTG"], os.environ["SSL_KEY_POSTG"])
        ssl_args = {"ssl_context": ssl_context}
    
    SQLALCHEMY_DATABASE_URI = database_uri

    if os.environ['ENVIRONMENT'] == 'production':
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args" : ssl_args
        }
        TESTING = False
        DEBUG = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = False
    else: 
        TESTING = True
        DEBUG = True
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = True   
