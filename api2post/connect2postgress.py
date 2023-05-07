import pg8000
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Time
import sqlalchemy
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import os
from google.cloud.sql.connector import Connector, IPTypes


# Set the path to your service account key JSON file
SERVICE_ACCOUNT_FILE = 'playground-geo-35c6afedf9ed.json'

# Create credentials object from service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# # Create an authorized session using the credentials
# session = AuthorizedSession(credentials)


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = 'playground-geo:us-central1:test-postgress'  # e.g. 'project:region:instance'
    db_user = 'quickstart-user'  # e.g. 'my-db-user'
    db_pass = os.environ['TEST_POSTGRES_PASSWORD']  # e.g. 'my-db-password'
    db_name = 'audio_transcription'  # e.g. 'my-database'


    # initialize Cloud SQL Python Connector object
    connector = Connector(credentials=credentials)

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=IPTypes.PUBLIC,
            
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool



    

def get_db():
    # Create a connection engine
    engine = connect_with_connector()
    # Define a session factory
    Session = sessionmaker(bind=engine)
    return Session()

# Define a declarative base
Base = declarative_base()

# Define the table structure as an ORM class
class Transcription(Base):
    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True)
    wav_filename = Column(String)
    original_transcription = Column(String)
    edited_transcription = Column(String)
    questionable = Column(Boolean)
    dont_use = Column(Boolean)
    character_id = Column(Integer)
    # locked_by = Column(Integer)
    # locked_time = Column(Time)

    def __str__(self):
        return (f"Transcription(id={self.id}, "
                f"wav_filename='{self.wav_filename}', "
                f"original_transcription='{self.original_transcription}', "
                f"edited_transcription='{self.edited_transcription}', "
                f"questionable={self.questionable}, "
                f"dont_use={self.dont_use}, "
                f"character_id={self.character_id})")