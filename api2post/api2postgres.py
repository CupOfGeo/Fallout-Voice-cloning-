from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from connect2postgress import Transcription, get_db
from datetime import datetime, timezone, time
import logging
from sqlalchemy.sql import func 

logging.basicConfig(level=logging.DEBUG)

# I could put these models in there own python file but like nah
class GetTranscriptModel(BaseModel):
    client_id: int

class TranscriptionModel(BaseModel):
      id: int
      wav_filename: str
      original_transcription: str
      edited_transcription: str
      questionable: bool
      dont_use: bool
      character_id: int
      locked_by: int
      locked_time: datetime

class GetTranscriptionResponse(BaseModel):
    results: list[TranscriptionModel]

class UpdateTranscriptModel(BaseModel):
    id: int
    client_id: int 
    edited_transcription: str
    questionable: bool 
    dont_use: bool


class DBSession:
    def __init__(self):
        # Session = sessionmaker(bind=engine)
        self.session = get_db()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


app = FastAPI()


@app.post("/get-transcriptions/")
def create_transcription(data: GetTranscriptModel):
    """user request to get transcriptions to edit"""
    with DBSession() as session:
        rows = session.query(Transcription).filter(Transcription.edited_transcription == None, Transcription.locked_by == None).limit(5).all()
        
        # rows = session.query(Transcription).filter(Transcription.edited_transcription == None and Transcription.locked_by == None).limit(5).all()
        for row in rows:
            row.locked_by = data.client_id
            row.locked_time = func.now()
        session.commit()
        logging.info(f"client_id:{data.client_id} locking ids:{[row.id for row in rows]}")
        return {"results":rows}
    
@app.post("/update-transcriptions/")
def update_transcriptions(data: UpdateTranscriptModel):

    with DBSession() as session:
        transcription = session.query(Transcription).filter_by(id=data.id).first()
        transcription.edited_transcription = data.edited_transcription
        transcription.questionable = data.questionable
        transcription.dont_use = data.dont_use
        if transcription.locked_by != data.client_id:
            raise ValueError('Transcription is not locked by this client.')
        transcription.locked_by = None
        session.commit()
    return "Thanks"
