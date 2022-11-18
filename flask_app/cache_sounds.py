# Writing a script that will create the voices, paths and types list.
import os
import librosa

# Statics.
END = '\n\n'
SAMPLE_RATE = 8000

static_dict = {}
word_dict = {}
character_dict = {}

voices = []
types = []
paths = []

def create_sound_lists():
	# Retriving all the voices.
	all_voices = os.listdir('data/')

	for j in range(len(all_voices)):
		voice = all_voices[j]

		# Retriving statics
		list_ = os.listdir('data/{}/statics/'.format(voice))
		for i in range(len(list_)):
			element = list_[i]
			voices.append(voice)
			types.append('static')
			paths.append('data/{}/statics/{}'.format(voice, element))

		# Retriving words
		list_ = os.listdir('data/{}/words/'.format(voice))
		for i in range(len(list_)):
			element = list_[i]
			voices.append(voice)
			types.append('word')
			paths.append('data/{}/words/{}'.format(voice, element))

		# Retriving characters
		list_ = os.listdir('data/{}/characters/'.format(voice))
		for i in range(len(list_)):
			element = list_[i]
			voices.append(voice)
			types.append('character')
			paths.append('data/{}/characters/{}'.format(voice, element))

	# print(voices, end=END)
	# print(types, end=END)
	# print(paths, end=END)

	# print(len(voices), len(types), len(paths))

# Using the function to fill the sound lists. 
# create_sound_lists()

# Now defining the function that inserts the variables in to the chaching dicts.
def cache_sounds(voices, types, paths):
    for i in range(len(paths)):
        voice = voices[i]
        type_ = types[i]
        path = paths[i]

        # Add the voice dict inside all the dicts if not present.
        if voice not in list(static_dict.keys()):
            static_dict[voice] = {}
        if voice not in list(word_dict.keys()):
            word_dict[voice] = {}
        if voice not in list(character_dict.keys()):
            character_dict[voice] = {}
        
        # Importing the sound.
        file_name = path.split('/')[-1][: -4]
        
        if type_ == 'static':
            # Add the file to the dict if not present previously.
            if file_name not in list(static_dict[voice].keys()):
                sound_ar, sr = librosa.load(path, sr=SAMPLE_RATE)
                static_dict[voice][file_name] = sound_ar

        if type_ == 'word':
            # Add the file to the dict if not present previously.
            if file_name not in list(word_dict[voice].keys()):
                sound_ar, sr = librosa.load(path, sr=SAMPLE_RATE)
                word_dict[voice][file_name] = sound_ar

        if type_ == 'character':
            # Add the file to the dict if not present previously.
            if file_name not in list(character_dict[voice].keys()):
                sound_ar, sr = librosa.load(path, sr=SAMPLE_RATE)
                character_dict[voice][file_name] = sound_ar

# cache_sounds()