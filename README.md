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
- Audio comes from https://www.sounds-resource.com/download/5645/ and is matched up to the wikis transcriptions https://fallout-archive.fandom.com/wiki/Robert_House%27s_dialogue with the removal of any extra sounds in curly brackets.

I recommend just zipping them and putting them in your google drive or storeage bucket.