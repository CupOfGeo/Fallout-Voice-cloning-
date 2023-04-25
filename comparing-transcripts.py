from difflib import SequenceMatcher

def compare_strings(string1, string2):
    # Create a SequenceMatcher object to compare the strings
    s = SequenceMatcher(None, string1, string2)

    # Get the differences between the strings
    differences = []
    for op, start1, end1, start2, end2 in s.get_opcodes():
        if op == 'replace':
            # For replace operations, add the replaced text to the differences list
            differences.append(f"{string1[start1:end1]} -> {string2[start2:end2]}")
        elif op == 'delete':
            # For delete operations, add the deleted text to the differences list
            differences.append(f"- {string1[start1:end1]}")
        elif op == 'insert':
            # For insert operations, add the inserted text to the differences list
            differences.append(f"+ {string2[start2:end2]}")

    # Return the differences list
    return differences


with open("wiki-transcription.txt", 'r') as wiki:
    wiki_lines = wiki.readlines()

with open("ai-transcription-md.txt", 'r') as whisper:
    whisper_lines = whisper.readlines() 

whisper_dict = {'_'.join(x.split('|')[0].split('_')[2:])[:-4]: x.split('|')[1].strip() for x in whisper_lines}

for line in wiki_lines:
    wav_filename, text = line.split('|')
    wiki_text = text.strip()
    wav_id = '_'.join(wav_filename.split('_')[2:])[:-4]
    whisper_text = whisper_dict[wav_id]

    print(wav_filename)
    print(compare_strings(wiki_text, whisper_text))




