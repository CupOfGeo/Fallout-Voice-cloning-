from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from connect2postgress import Transcription, get_db
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

class GetTranscriptModel(BaseModel):
    client_id: int



class UpdateTranscriptModel(BaseModel):
    id: int
    clinet_id: int 
    edited_transcription: str


class DBSession:
    def __init__(self):
        # Session = sessionmaker(bind=engine)
        self.session = get_db()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Code to run during startup
    DBSession()
    print("Application started!")

@app.post("/get-transcriptions/")
def create_transcription(data: GetTranscriptModel):
    """user request to get transcriptions to edit"""
    with DBSession() as session:
        rows = session.query(Transcription).filter(Transcription.edited_transcription == None).limit(5).all()
        # rows = session.query(Transcription).filter(Transcription.edited_transcription == None and Transcription.locked_by == None).limit(5).all()
        # for row in rows:
        #     row.locked_by = GetTranscriptModel.client_id
        #     row.locked_time = datetime.utcnow()
        
        # session.commit()

        
        logging.info(f"client_id:{data.client_id} locking ids:{[row.id for row in rows]}")
        return {"result":rows}
    
@app.post("/updated-transcriptions/")
def update_transcriptions(UpdateTranscriptModel):

    with DBSession() as session:
        transcription = session.query(Transcription).filter_by(id=UpdateTranscriptModel['id']).first()
        transcription.edited_transcription = UpdateTranscriptModel.edited_transcription
        if transcription.locked_by != UpdateTranscriptModel['client_id']:
            raise ValueError('Transcription is not locked by this client.')
        transcription.locked_by = None
        session.commit()

        