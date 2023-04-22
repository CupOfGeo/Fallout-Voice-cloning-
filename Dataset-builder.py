
import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment
import io
import zipfile
import os
import shutil

def MrNewVegas(output_path):
    # delete if the directory already exists
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

    response = requests.get("https://fallout.fandom.com/wiki/Radio_New_Vegas")

    soup = BeautifulSoup(response.text, 'html.parser')
    li_tags = soup.find_all('li')

    # Transcription file
    with open(f'{output_path}/MrNewVegas.txt', mode='w', newline='') as file:

        # Loop through the li tags and find the src attribute in the div element
        for li in li_tags:
            if li.find('i'):
                
                div_tag = li.find('audio')  # Find the first div element inside the li tag
                if div_tag:  # Check if a div element was found
                    src_attribute = div_tag['src']  # Access the src attribute using square bracket notation
                    print(src_attribute)
                    ogg_filename = None
                    for x in src_attribute.split('/'):
                        if '.ogg' in x:
                            ogg_filename = x
                            break
                    wav_filename = ogg_filename.replace('.ogg','.wav')

                    
                    response = requests.get(src_attribute)

                    # Convert the response content to an AudioSegment object
                    audio = AudioSegment.from_file(io.BytesIO(response.content))

                    # export as wav
                    audio.export(f'{output_path}/{wav_filename}', format='wav')

                    text = li.find('i').text
                    if text:
                        file.write(f'{text}|{wav_filename}\n')




def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

MrNewVegas('wiki-MNV')
zip_folder('wiki-MNV', 'wiki-MNV.zip')
