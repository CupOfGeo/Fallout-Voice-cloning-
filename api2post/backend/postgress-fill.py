from tqdm import tqdm
import os
from sqlalchemy.orm import sessionmaker
from connect2postgress import Transcription, get_db

"""
This helps me fill the database given a transcription 
Plans for this would be to turn it into a cloud function thats triggered when a transcription is uploaded to a bucket
"""


# Define a function to read the text file and insert the data into the database
def insert_data_from_file(filename):
    # Open the file for reading
    with open(filename, 'r') as file:
        # Create a session
        session = get_db()

        # Iterate over each line in the file
        for line in tqdm(file):
            # Split the line into columns
            columns = line.strip().split('|')

            # Create a new Transcription object and set its properties
            transcription = Transcription(
                wav_filename=columns[0],
                original_transcription=columns[1],
                edited_transcription=None,
                questionable=None,
                dont_use=None,
                character_id=0,
                locked_by=None,
                locked_time=None,
                client_id=None
            )
            # print(transcription)
            # Add the object to the session
            session.add(transcription)
            

        # Commit the session
        session.commit()

        # Close the session
        session.close()

# Call the function to insert the data
# insert_data_from_file('/Users/mazzeogeorge/Desktop/Fallout/Zombies/plr0/moon-plr0-whisper.txt')
