# Fallout-Voice-cloning-
Going to play around with TalkNet and HiFi-Gan to clone some voice from Fallout NV .\

Dataset structure\
```
CharacterName/
    ├── audio_file_0.wav
    ├── ...
    ├── audio_file_n.wav
    └── character_transcription.txt
```

where the transcription is in rows like. `audio_file_0.wav|Text they said in clip`

So far we just make Datasets for  
### Mr.New Vegas 
- This dataset is built stright from the wiki https://fallout.fandom.com/wiki/Radio_New_Vegas

### Mr.House 
- Audio comes from https://www.sounds-resource.com/download/5645/ and is matched up to the wikis transcriptions https://fallout-archive.fandom.com/wiki/Robert_House%27s_dialogue with the removal of any extra sounds in brackets. There is also a list of audio files which 
    
    these are sound files from when hes dying in the pod that i removed 
    bad_data = ["00159463_1", "00159466_1", "0015945F_1", "00159465_1", "00159460_1", "00159461_1", "00159462_1", "0015946A_1", "0015946E_1", "0015946F_1"]

I recommend just zipping them and putting them in your google drive or storeage bucket.


just made a db in gcp username test-postgress. thinking this would be a good scema. (no terraform just ui)
```SQL
CREATE DATABASE audio_transcription;

\c audio_transcription;

CREATE TABLE transcriptions (
    id SERIAL PRIMARY KEY,
    wav_filename TEXT,
    original_transcription TEXT,
    edited_transcription TEXT,
    questionable BOOLEAN,
    dont_use BOOLEAN,
    character_id INTEGER NOT NULL
);
```


Starting building a transcription reviewer interface. The plan would be it just reads from the postgress db and give un verifed transcriptions then a user can edit transcription and then save it and get another one. there are additional flags such as dont_use and questionnable. 

My current thoguth is it will send any row that has an empty edited_transcription text