"""This module is responsible for holding all the function that will being used
at the main app.py file.
"""
import numpy as np
import librosa
import soundfile as sf
from number_to_text import number_to_text
from year_to_text import year_to_text
from name_pronouncer import name_pronouncer
from cache_sounds import voices, types, paths, static_dict, word_dict, character_dict, create_sound_lists, cache_sounds
import datetime
import os
import hashlib

# Defining constants.
END = '\n\n'
# SAMPLE_RATE = 384000
SAMPLE_RATE = 8000

word_crop_th = 0.02

# Creating the sound_lists.
# create_sound_lists() 

# Using the function to cache the sounds.
# cache_sounds(voices, types, paths)

# print(static_dict, end=END)
# print(word_dict, end=END)
# print(character_dict, end=END)

text = 'D M I Finance me apka swagat hai. Kya meri baat {Ankush} se\
 ho rahi hai? Apki deya rashi {1212 rupay} hae. Apki deya rashi ka antim deya\
 samay {12 April, 1212} {01:12 AM} hai.'
# print(text, end=END)

voice = 'voice_1'

def text_to_speech(text, voice):
	text_replaced = text.replace('{', '~')
	text_replaced = text_replaced.replace('}', '~')

	text_splits = text_replaced.split('~')
	# print(text_splits, end=END)

	# Now it's time to take the splits from the text_splits and build up the 
	# voice_clip.
	voice_clip_ar = np.array([])

	for i in range(len(text_splits)):
		text_split = text_splits[i]

		# 1. Check if the split is available in static_dict. 
		# Elif take all the words from the split. Convert 
		# 1. each word to lowercase. 
		# 2. Convert number to words. 
		# 3. Search the word in the word_dict. 
		# 4. If not available use name entity 
		# 5. Pronunciation method for it by using character_dict.

		# Before doing checking in statics, we need to use md5 hash value of the text_split.
		text_split_hash_value = hashlib.md5(text_split.encode()).hexdigest()

		if text_split_hash_value in static_dict[voice]:
			voice_clip_ar = np.concatenate([voice_clip_ar, static_dict[voice][text_split_hash_value]])

		else:
			# Removing comma from the text_split.
			text_split = text_split.replace(',', '')

			# Replacing ':' with space.
			text_split = text_split.replace(':', ' ')

			# Converting the text_split (variable) to lowercase. 
			text_split = text_split.lower()

			# Convert the text split to a list of words. 
			word_list = text_split.split(' ')

			for i in range(len(word_list)):
				word = word_list[i]

				# Detect if the word is a number.
				if word.isnumeric():
					# Detect if year.
					month_list = ['january', 'february', 'march', 'april']
					try:
						if word_list[1] in month_list:
							# Use year to text.
							number_text = year_to_text(word)
						else:
							# Using number to words.
							number_text = number_to_text(word)
					except:
						# Using number to words.
						number_text = number_to_text(word)
					number_words = number_text.split(' ')
					for j in range(len(number_words)):
						number_word = number_words[j]
						if number_word in word_dict[voice]:
							if number_word[-1] in ['a', 'i', 'u', 'e', 'o', 'y']:
								voice_clip_ar = np.concatenate([voice_clip_ar, word_dict[voice][number_word][0 : len(word_dict[voice][number_word]) - int(word_crop_th * SAMPLE_RATE)]])
							else:
								voice_clip_ar = np.concatenate([voice_clip_ar, word_dict[voice][number_word]])
				elif word in word_dict[voice]:
					if word[-1] in ['a', 'i', 'u', 'e', 'o', 'y']:
						voice_clip_ar = np.concatenate([voice_clip_ar, word_dict[voice][word][0 : len(word_dict[voice][word]) - int(word_crop_th * SAMPLE_RATE)]])
					else:
						voice_clip_ar = np.concatenate([voice_clip_ar, word_dict[voice][word]])
				else:
					# Use name pronouncer function to crate the array.
					try:
						name_ar = name_pronouncer(word, voice)
						voice_clip_ar = np.concatenate([voice_clip_ar, name_ar])
					except:
						pass

	# print(voice_clip_ar, end=END)
	date_time = str(datetime.datetime.now())
	date_time = date_time.replace(' ', '_')

	output_path = 'ram_disk_folder/static/outputs/sln_outputs/{}.wav'.format(date_time)
	# Writing the file.
	sf.write(output_path, voice_clip_ar, SAMPLE_RATE)

	# Finding the base path.
	# real_path = os.path.realpath(__file__)
	# real_path = real_path.split('/')[0 : -1]
	# base_path = '/'.join(real_path) + '/'

	# Using sox command to convert the file to .sln format.
	sln_path = 'ram_disk_folder/static/outputs/sln_outputs/{}.sln'.format(date_time)
	command = 'sox {} {}'.format(output_path, sln_path)

	os.system(command)

	
	# print('Output generated.')

	return (sln_path, output_path)

if __name__ == '__main__':
	sln_path = text_to_speech(text, voice)
	print(sln_path)