import os
from dash import Dash, dcc, html, Input, Output, State, callback_context
# import base64
import requests
import random
from pydantic import BaseModel
from app import app, server

class UpdateTranscriptModel(BaseModel):
    id: int
    client_id: int 
    edited_transcription: str
    questionable: bool 
    dont_use: bool

'''
Tack
Richtofen
'''


app.layout = html.Div([
    html.H1("Audio Preview and Transcription Editor", id='header'),
    html.Div([
        html.Label("Select File", id='title'),
        html.Audio(id="audio-preview", controls=True,autoPlay=True),
        dcc.Textarea(
            id="transcription-textarea",
            placeholder="Enter transcription here",
            rows=10,
            style={"width": "100%"}
        ),
        # html.Button("Save Transcription", id="save-button"),
        html.Button("Next Transcription", id="next-button"),
        html.Button("Questionable Transcription", id="questionable-button"),
        html.Button("Don't Use Transcription", id="bad-button"),
    ], style={"max-width": "500px", "margin": "auto"}),
    dcc.Store(id='local-storage', storage_type="local"),
    dcc.Store(id='client-id', storage_type="local")
])


@app.callback(Output('client-id', 'data'),Input("title","n_clicks"), State('client-id', 'data'))
def set_client_id(dummy,client_id):
    # this is not unique to the database but i dont want to worry about that right now 
    # Still pretty high bc of birthday paradox if more than 100 users were to use it.
    if client_id:
        return client_id
    else:
        return random.randint(0, 10000000)



def get_rows(client_id):
    # query for the first row with NULL edited_transcription
    url = f"{os.environ['BACKEND_URL']}/get-transcriptions/"
    payload = {'client_id': client_id}
    response = requests.post(url, json=payload)
    rows = response.json()
    if rows.get('results'):
        return rows['results']    
    else:
        return None


def save_row(row, new_transcription, questionable, bad, client_id):
    url = f"{os.environ['BACKEND_URL']}/update-transcriptions/"
    if new_transcription:
        payload = UpdateTranscriptModel(
            id=int(row['id']),
            client_id=client_id,
            edited_transcription=new_transcription,
            questionable=questionable, 
            dont_use=bad)
        
        response = requests.post(url, json=dict(payload))
    else:
        raise ValueError("Empty transcription") 



@app.callback(
    Output("audio-preview", "src"),
    Output("transcription-textarea", "value"), 
    # I think I can seperate theseout to another call back that gets triggered on an update to local-strage datas value
    # woud just make it a little cleaner
    Output("title", "children"),
    Output("local-storage", "data"),
    Input("next-button", 'n_clicks'),
    Input("questionable-button", 'n_clicks'),
    Input("bad-button", 'n_clicks'),
    State("title","children"),
    State("transcription-textarea", "value"),
    State("local-storage", "data"),
    State("client-id", "data")
)
def update_audio_preview(n_clicks_next,n_clicks_questionable,n_clicks_bad,prev_wav,edited_transcript, prev_rows, client_id):  
    client_id = client_id or set_client_id(5,client_id)
    

    prev_rows = prev_rows or get_rows(client_id) # first time goign to the page 
    if prev_rows:
        if len(prev_rows) == 0:
            # if theres nothing in the local-storage get a new rows
            prev_rows = get_rows(client_id)
    else:
        # if theres nothing in the local-storage get a new rows
        prev_rows = get_rows(client_id)
        
    if prev_rows is None:
        raise ValueError("Empty prev_rows") 
    
    row = prev_rows.pop()
    if prev_rows is None:
        raise ValueError("Empty prev_rows") 


    # logic for which buttton was pressed
    ctx = callback_context
    if not ctx.triggered:
        print('No button clicked')
        # return 'No button clicked'
    else:
        # only save if the button was clicked sure we might miss an unlock but thats ok.
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'next-button':
            save_row(row, edited_transcript, False, False, client_id=client_id)
        elif button_id == 'questionable-button':
            save_row(row, edited_transcript, questionable=True, bad=False, client_id=client_id)
        elif button_id == 'bad-button':
            save_row(row, edited_transcript, questionable=False, bad=True, client_id=client_id)
        else:
            print('Unknown button clicked')


    
    

    # local audio preview not fun 
    # audio_file_path = f"/Users/mazzeogeorge/Desktop/Fallout/Zombies/testfolder{row['wav_filename']}"
    # print(audio_file_path)
    # with open(audio_file_path, "rb") as f:
    #     audio_data = f.read()
    # audio_base64 = base64.b64encode(audio_data).decode("utf-8")
    # audio_preview = f"data:audio/wav;base64,{audio_base64}"

    audio_src_url = f"https://storage.googleapis.com/geo-audio-data/{row['wav_filename']}"


    return audio_src_url, row['original_transcription'], row['wav_filename'], prev_rows

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)