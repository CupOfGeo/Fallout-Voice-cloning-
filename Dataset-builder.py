
import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment
import io
import zipfile
import os
import shutil
import re
from tqdm import tqdm


def make_new_dir(output_path):
    # delete if the directory already exists
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

def ogg2wav(audio, wav_output_path):
    # Set the sample rate to 22050
    audio = audio.set_frame_rate(22050)
    # Set the channels to 1 (mono)
    audio = audio.set_channels(1)
    # Set the sample width to 2 (16-bit)
    audio = audio.set_sample_width(2)
    # export as wav
    audio.export(wav_output_path, format='wav')


def MrNewVegas_wiki(output_path):
    make_new_dir(output_path)

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
                    # Download ogg file 
                    response = requests.get(src_attribute)
                    # Convert the response content to an AudioSegment object
                    audio = AudioSegment.from_file(io.BytesIO(response.content))
                    ogg2wav(audio, f'{output_path}/{wav_filename}')

                    text = li.find('i').text
                    
                    # These two audio clips have different speakers in them and so I will chose to omit 
                    # but they could be fixed rather easy
                    bad_data = ['FNV_RNV_begoodoriwillshootyoudead.wav', 'FNV_RNV_tokenotfound.wav']

                    if text or wav_filename in bad_data:
                        file.write(f'{wav_filename}|{text}\n')




def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))



def remove_curly_brackets(raw_str):
  return re.sub(r'\{.*?\}', '', raw_str)

def MrHouse_sound_resources(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    response = requests.get("https://www.sounds-resource.com/download/5645/")

    # download zip file
    with open(f'{folder_path}/MrHouse.zip', 'wb') as f:
        f.write(response.content)

    # unzip into folder
    with zipfile.ZipFile(f'{folder_path}/MrHouse.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{folder_path}/oggs')

    

    # Set the input and output directories
    input_dir = f"{folder_path}/oggs"
    output_dir = f"{folder_path}"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Converting oggs to wavs") 
    # Loop through all files in the input directory
    for file in tqdm(os.listdir(input_dir)):
        if file.endswith(".ogg"):
            # Load the input file
            input_file = os.path.join(input_dir, file)
            sound = AudioSegment.from_ogg(input_file)
            ogg2wav(sound, f'{output_dir}/{os.path.splitext(file)[0] + ".wav"}')
    print("Done cleaning up")
    shutil.rmtree(input_dir) # remove oggs folder
    os.remove(f'{folder_path}/MrHouse.zip') # delete zip file of oggs
    
    

def MrHouse_wiki(output_path):
    make_new_dir(output_path)

    MrHouse_sound_resources(output_path)
    
    url = "https://fallout-archive.fandom.com/wiki/Robert_House%27s_dialogue"

    # Make a request to the web page
    response = requests.get(url)

    raw_data = []

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    hosue_audio_ogg = os.listdir(output_path)

    # Find all the tr tags in the HTML
    table = soup.find('table', {'class': 'va-table'})
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 7:
            if cells[5].text.lower().strip()+".wav" in hosue_audio_ogg:
                # minor cleaning 
                response = cells[4].text.strip()  
                response = remove_curly_brackets(response) # removes {sound/emotion/tone}
                fname = cells[5].text.lower().strip()+".wav"
                raw_data.append(fname+"|"+response)

        with open(f'{output_path}/wiki-transcription.txt', 'w') as file:
            for line in raw_data:
                file.write(line + '\n')






# MrNewVegas_wiki('wiki-MNV')
# zip_folder('wiki-MNV', 'wiki-MNV.zip')
MrHouse_wiki('MrHouse')