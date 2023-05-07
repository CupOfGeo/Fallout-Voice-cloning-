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

GRANT SELECT, INSERT, UPDATE, DELETE ON transcriptions TO "quickstart-user";
GRANT ALL PRIVILEGES ON TABLE transcriptions TO "quickstart-user";
GRANT USAGE, SELECT ON SEQUENCE transcriptions_id_seq TO "quickstart-user";
```


Starting building a transcription reviewer interface. The plan would be it just reads from the postgress db and give un verifed transcriptions then a user can edit transcription and then save it and get another one. there are additional flags such as dont_use and questionnable. 

My current thoguth is it will send any row that has an empty edited_transcription text

TODO: i should probably add a user_id and updated time, locked_by, locked_time

With the current above implmentation i have a problem where 2 users can be doing the same work and then updating the same row. So to fix that i will add a locked_by and locked_time

then when a user queries for a subset of 5 records it will update the locked_by and locked_time of the 5 rows so that other users dont get the rows. then as they save them back with updated transcriptions the locked_by is removed. 

query to use would be `select * from transcription where edited_transcription is NONE and locked_by is NONE limit 5;`
then from those rows something like rows.locked_by = user & rows.locked_time = now() and update

then as they send them back just clear the locked_by = None. (can they also check if the locked_by user is there user?)

For cases where users disconnect or stop we have to run a query that cehcks if there are any rows with locked_times over Y mins and with locked_by not None and release them back.
This is a lot of quries and connections 

? Do i have to removed the locked_time well i would have to check every so often if there are quries with locked_by users and locked_time over Y mins from now so as long as there is no user i can still keep the locked time. 

Fuck I need an api between them.

```sql
ALTER TABLE transcriptions ADD COLUMN locked_by integer;
ALTER TABLE transcriptions ADD COLUMN locked_time timestamp;
SET TIME ZONE 'UTC'
ALTER TABLE transcriptions ALTER COLUMN locked_time TYPE timestamp without time zone;
```

