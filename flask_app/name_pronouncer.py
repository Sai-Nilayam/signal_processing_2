# Shell-1
# ----------------------------------------------------------------
# Imports
# Required imports are at it's place where it is needed to be used. However here, there should be a list of all 
# imports so that it will be possible to use those just by runnig the 1st shell.
import librosa
import soundfile as sf
import numpy as np
import os
import shutil
from itertools import product
from cache_sounds import voices, types, paths, create_sound_lists, static_dict, word_dict, character_dict, cache_sounds, SAMPLE_RATE
import datetime

# Constants
END = '\n\n'
# SAMPLE_RATE = 384000
SAMPLE_RATE = 8000

# ----------------------------------------------------------------
# Enables the caching of different sound chunks.
# create_sound_lists()
# cache_sounds(voices, types, paths)

# print(static_dict)
# print(word_dict)
# print(character_dict)

# Shell-2
# ----------------------------------------------------------------
# Global variable

# All english alphabets
# a b c-> d e f g h i j k l m n o p q- r s t u v w- x- y- z

# Stands for Vyanjanavarna set.
vv_set = [
	'k', 'kh', 'g', 'gh', 'n2',
	'ch', 'chh', 'j', 'jh',
	't', 'th', 'd', 'dh',
	't2', 'th2', 'd2', 'dh2',
	'p', 'ph', 'b', 'bh',
	
	'f', 'v', 'z',
	
	'y', 'w', 'q', 'x',
	
	# A part of the vv is pvv too.
	'r', 'l', 'sh', 's', 'h',
	'n', 'm',
]

pvv_set = [
	'r', 'l', 'sh', 's',
	'n', 'm',
	'g', 'j', 'd', 'd2', 'b',
	'gh', 'jh', 'dh', 'dh2', 'bh',
]

# Stands for Swaravarna set.
sv_set = [
	'a', 'a2', 'i', 'u', 'e', 'o',
#     'ae', 'ao',
	# All these mixed sv are not required in this set. Insted we are going to collect these from real large text
	# corpuses.
#     'aa2', 'ai', 'au', 'ae', 'ao',
#     'a2a', 'a2i', 'a2u', 'a2e', 'a2o',
#     'ia', 'ia2', 'iu', 'ie', 'io',
#     'ua', 'ua2', 'ui', 'ue', 'uo',
#     'ea', 'ea2', 'ei', 'eu', 'eo',
#     'oa', 'oa2', 'oi', 'ou', 'oe',
	
	# Extra Mappings. 
	'aa'
]

# Stands for Punctuation set. 
p_set = [
	',', '.', '?', '!'
]

char_set = sv_set + vv_set + p_set

sv_set_large = [
	# Here we are going to append all the new sv those are collected from large text corpus. 
]


# Shell-3
# ----------------------------------------------------------------
## This shell is responsible for taking a word as input and converting it to it's character list.

# input: 'ankush'
# output: ['a', 'n', 'k', 'u', 'sh']

def word_to_chars(word, char_1, char_2, char_3, char_4):
	# We will be taking 4 different lists.
	word_to_char_list = []

	i = 0
	final_index = len(word)
	
	# Writing the word_to_char_list formatter script.
	while i < final_index:
		# Check if the character is in the char_4.
		try:
			inst_char = word[i : i+4]
			if inst_char in char_4:
				word_to_char_list.append(inst_char)
				i = i + 4
				continue
		except:
			pass

		# Check if the character is in the char_3.
		try:
			inst_char = word[i : i+3]
			if inst_char in char_3:
				word_to_char_list.append(inst_char)
				i = i + 3
				continue
		except:
			pass

		# Check if the character is in the char_2.
		try:
			inst_char = word[i : i+2]
			if inst_char in char_2:
				if inst_char == 'aa':
					word_to_char_list.append('a2')
				else:
					word_to_char_list.append(inst_char)
				i = i + 2
				continue
		except:
			pass

		# Check if the character is in the char_1.
		try:
			inst_char = word[i : i+1]
			if inst_char in char_1:
				word_to_char_list.append(inst_char)
				i = i + 1
				continue
			else:
				# If the character was not found anywhere append '_na_' for it.
				word_to_char_list.append('_na_')
				i = i + 1
		except:
			pass
		
	return word_to_char_list

# Using the function.
word = 'raekt2esh'

char_1 = []
char_2 = []
char_3 = []
char_4 = []

for char in char_set:
	if len(char) == 4:
		char_4.append(char)
	if len(char) == 3:
		char_3.append(char)
	if len(char) == 2:
		char_2.append(char)
	if len(char) == 1:
		char_1.append(char)


# Shell-4
# ----------------------------------------------------------------
# This shell is responsible for merging the swaravarnas given a word_to_char_list.

def word_to_connected_chars(word_to_char_list):
	word_to_connected_char_list = []

	inst_sv = ''

	for i in range(len(word_to_char_list)):
		inst_char = word_to_char_list[i]

		if inst_char in sv_set:
			inst_sv = inst_sv + inst_char

		if inst_char in vv_set:
			if inst_sv != '':
				word_to_connected_char_list.append(inst_sv)
				# Also append it in the sv_set_large.
				sv_set_large.append(inst_sv)
				inst_sv = ''

			word_to_connected_char_list.append(inst_char)

		if i == len(word_to_char_list) - 1:
			if inst_sv != '':
				word_to_connected_char_list.append(inst_sv)
				# Also append it in sv_set_large
				sv_set_large.append(inst_sv)
				
		# Append any punctuation if it's present.
		if inst_char in [',', '.', '?', '!']:
			word_to_connected_char_list.append(inst_char)
				
	return word_to_connected_char_list


# Shell-5
# ----------------------------------------------------------------
# This shell is responsible for creating the fluctuated character list out of the main character list.

def char_fluctuator(word_to_connected_char_list):
	chars = word_to_connected_char_list
	# print(chars, end=END)

	char_flct = []

	for i in range(len(chars)):
		char = chars[i]
		if char in vv_set:
			try:
				char_after = chars[i + 1]
				char_before = chars[i - 1]
				if char_after in sv_set_large:
					char_flct.append(char + '_s')
					
				elif (char_before in sv_set_large) and (i != 0):
					char_flct.append(char + '_e')
					char_flct.append('_g_')
				else:
					char_flct.append(char + '_s')
			except:
				pass
			if i == len(chars)-1:
				char_flct.append(char + '_e')
		elif char in sv_set_large:
			char_flct.append(char)

	# print(char_flct, end=END)

	# Now reversing the char_flct
	char_flct.reverse()
	# print(char_flct, end=END)

	char_flct_final = []

	j = 0
	for i in range(len(char_flct)):
		char = char_flct[i]

		if char in sv_set_large:
			# Check if ending SV.
			is_ending_sv = True
			for k in range(i+1, len(char_flct)):
				char_nexts = char_flct[k]
				if char_nexts in sv_set_large:
					is_ending_sv = False

			if j == 0:
				char_flct_final.append(char + '_e')
				j = j + 1

			elif j > 1 and is_ending_sv == True:
				char_flct_final.append(char + '_s')

			elif j > 0:
				char_flct_final.append(char + '_m')
				j = j + 1
		else:
			char_flct_final.append(char)

	char_flct_final.reverse()

	# print(char_flct_final, end=END)

	# Now it's time to handle the pvv.
	char_flct_list_altimate = []

	for i in range(len(char_flct_final)):
		char_flct = char_flct_final[i]
		char = char_flct.split('_')[0]
		char_suffix = char_flct.split('_')[1]
		if char in pvv_set and char_suffix == 'e':
			try:
				char_before = char_flct_final[i - 1]
				char_before_suffix = char_before.split('_')[1]
				char_before_pure = char_before.split('_')[0]
				if char_before_pure in sv_set_large:
					char_flct_list_altimate.append(char_flct + '_' + char_before_suffix)
				else:
					char_flct_list_altimate.append(char_flct + '_e')
			except:
				pass
		else:
			char_flct_list_altimate.append(char_flct)
			
	# print(char_flct_list_altimate, end=END)
	
	# Now it's time to handle the speacial 'h' sound when it comes.
	char_flct_list_altimate_2 = []
		
	for i in range(len(char_flct_list_altimate)):
		char_flct = char_flct_list_altimate[i]
		char = char_flct.split('_')[0]
		char_flct_suffix = char_flct.split('_')[1]
		
		if (char_flct_suffix == 's') and (char[-1] == 'h' or char[-2:] == 'h2') and (char != 'ch'):
			if char == 'h':
				char_split_1 = 'h'
			elif char[-2:] == 'h2':
				char_split_1 = char[0: len(char)-2] + '2'
			else:
				char_split_1 = char[0 : len(char)-1]
			
			char_next = char_flct_list_altimate[i + 1]
			char_next_pure = char_next.split('_')[0]
			
			if (char_next_pure in sv_set) or (char_next_pure in sv_set_large):
				first_letter = char_next_pure[0]
				needed_h = 'h_s_' + first_letter
				if char != 'h':
					char_flct_list_altimate_2.append(char_split_1 + '_s')
					char_flct_list_altimate_2.append(needed_h)
				else:
					char_flct_list_altimate_2.append(needed_h)
			else:
				char_flct_list_altimate_2.append(char_split_1)
				char_flct_list_altimate_2.append('h_s_a')
			
		elif char_flct == 'h_e':
			before_char = char_flct_list_altimate[i - 1]
			before_char_pure = before_char.split('_')[0]
			if (before_char_pure in sv_set) or (before_char_pure in sv_set_large):
				last_letter = before_char_pure[-1]
				needed_h = 'h_e_' + last_letter
				char_flct_list_altimate_2.append(needed_h)
			else:
				char_flct_list_altimate_2.append(char_flct)
		else:
			char_flct_list_altimate_2.append(char_flct)
	
	return char_flct_list_altimate_2

# Shell-6
# ----------------------------------------------------------------
# This shell is responsible for converting char_flct_list to it's speech form.

# input: ['a_s', 'n_e', '_g_', 'k_s', 'u_m', 'sh_e']
# output: 'word.wav'

def char_flct_to_speech(char_flct_list, voice, noise, vv_set_name, sv_set_name, pvv_set_name, vv_volume, sv_volume, yukt_gap):
	# Beofore putting any gaps we need to import the noise and crop the part as gap as per the gap time
	# specified. 
	# noise_ar, sr = librosa.load('data/noise_set/{}.wav'.format(noise), sr=SAMPLE_RATE)
	noise_ar = character_dict[voice]['noise']

	_g_ = noise_ar[: int(yukt_gap * SAMPLE_RATE)]

	speech_ar = np.array([])
	
	concatenation_case = []

	for i in range(len(char_flct_list)):
		inst_char = char_flct_list[i]
		inst_char_pure = inst_char.split('_')[0]
		inst_char_suffix = inst_char.split('_')[1]

		if (inst_char_pure in vv_set):
			if inst_char_pure in pvv_set and inst_char_suffix == 'e' :
				# inst_chunk_ar, inst_sr = librosa.load('data/sv_sets/{}/{}/{}'.format(sv_set_name, pvv_set_name, inst_char + '.wav'), sr = SAMPLE_RATE) 
				inst_chunk_ar = character_dict[voice][inst_char]
			else:
				# inst_chunk_ar, inst_sr = librosa.load('data/vv_sets/{}/{}'.format(vv_set_name, inst_char + '.wav'), sr=SAMPLE_RATE)
				inst_chunk_ar = character_dict[voice][inst_char]
				inst_chunk_ar = inst_chunk_ar * vv_volume
			speech_ar = np.concatenate([speech_ar, inst_chunk_ar])
			concatenation_case.append(inst_char)
		
		if inst_char == '_g_':
			inst_chunk_ar = _g_
			speech_ar = np.concatenate([speech_ar, inst_chunk_ar])
			concatenation_case.append(inst_char)
		
		if inst_char_pure in sv_set_large:
			# Handling the concatenation of the sv is a bit different.
			try:
				char_after = char_flct_list[i + 1]
				char_after_pure = char_after.split('_')[0]
				char_after_pure_suffix = char_after.split('_')[1]
				
				if char_after_pure in vv_set:
					if char_after_pure in pvv_set and char_after_pure_suffix == 'e':
						# char_after_ar, inst_sr = librosa.load('data/sv_sets/{}/{}/{}'.format(sv_set_name, pvv_set_name, char_after + '.wav'), sr = SAMPLE_RATE)
						char_after_ar = character_dict[voice][char_after]
					else:
						# char_after_ar, inst_sr = librosa.load('data/vv_sets/{}/{}'.format(vv_set_name, char_after + '.wav'), sr=SAMPLE_RATE)
						char_after_ar = character_dict[voice][char_after]
						
					# inst_chunk_ar, inst_sr = librosa.load('data/sv_sets/{}/{}'.format(sv_set_name, inst_char + '.wav'), sr=SAMPLE_RATE)
					inst_chunk_ar = character_dict[voice][inst_char]
					
					char_after_len = len(char_after_ar)
					inst_chunk_len = len(inst_chunk_ar)
					
					# To see if the it's taking unsusual concatenation.
					# print(inst_chunk_len, char_after_len)
					
					if inst_chunk_len >char_after_len:
						inst_chunk_ar_appendable = inst_chunk_ar[: inst_chunk_len - char_after_len]
						speech_ar = np.concatenate([speech_ar, inst_chunk_ar_appendable])
						concatenation_case.append(inst_char)
					else:
						concatenation_case.append('unsual_concatenation_susp')
				else:
					# inst_chunk_ar, inst_sr = librosa.load('data/sv_sets/{}/{}'.format(sv_set_name, inst_char + '.wav'), sr=SAMPLE_RATE)
					inst_chunk_ar = character_dict[voice][inst_char]
					inst_chunk_ar = inst_chunk_ar * sv_volume
					speech_ar = np.concatenate([speech_ar, inst_chunk_ar])
					concatenation_case.append(inst_char)
			except:
				# inst_chunk_ar, inst_sr = librosa.load('data/sv_sets/{}/{}'.format(sv_set_name, inst_char + '.wav'), sr=SAMPLE_RATE)
				inst_chunk_ar = character_dict[voice][inst_char]
				inst_chunk_ar = inst_chunk_ar * sv_volume
				speech_ar = np.concatenate([speech_ar, inst_chunk_ar])
				# concatenation_case.append(inst_char)
				
	# print('concatenation_case:', concatenation_case)
	return speech_ar


# Now Using all the functions to generate a word.
# ----------------------------------------------------------------
# Pronounces a Name Entity.
def name_pronouncer(word, voice):
	word_to_char_list = word_to_chars(word, char_1, char_2, char_3, char_4)
	# print('character_list:', word_to_char_list, end=END)

	word_to_connected_char_list = word_to_connected_chars(word_to_char_list)
	# print('connected_character_list:', word_to_connected_char_list, end=END)

	char_flct_list = char_fluctuator(word_to_connected_char_list)
	# print('char_flct_list', char_flct_list, end=END)
	
	noise = 'noise_2'
	vv_set_name = 'vv_set_n2_t2'
	sv_set_name = 'sv_set_n2_t2_s2_revised'
	pvv_set_name = 'pvv_set_n2_t2_s2_revised'
	yukt_gap = 0.01
	vv_volume = 1
	sv_volume = 1

	speech_ar = char_flct_to_speech(char_flct_list, voice, noise, vv_set_name, sv_set_name, pvv_set_name, vv_volume, sv_volume, yukt_gap)

	# Now we need to save this to apply the ffmpeg command to make the word get in a given frame.
	date_time = str(datetime.datetime.now())
	date_time = date_time.replace(' ', '_')
	file_path = 'ram_disk_folder/static/outputs/inst_names/{}.wav'.format(date_time)
	sf.write(file_path, speech_ar, SAMPLE_RATE)

	expected_duration = 0.5
	original_duration = librosa.get_duration(speech_ar, sr=SAMPLE_RATE)
	speed_index = original_duration / expected_duration

	output_file_path = 'ram_disk_folder/static/outputs/inst_names/{}_fast.wav'.format(date_time)
	cmd = 'ffmpeg -i {} -filter:a "atempo={}" -vn {} -y'.format(file_path, speed_index, output_file_path)
	os.system(cmd)

	# Now gettting back the file array.
	speech_ar, sr = librosa.load(output_file_path, sr=SAMPLE_RATE)

	# Now we need to delete both the files.
	os.remove(file_path)
	os.remove(output_file_path)

	# sf.write('static/outputs/word.wav', speech_ar, SAMPLE_RATE)
	# print('Output generated.')

	return speech_ar

if __name__ == '__main__':
	word = 'ankush'
	voice = 'voice_4'
	name_ar = name_pronouncer(word, voice)
	print('Function executed with no errors.')


