# Imports
from flask import Flask, request
import json
from text_to_speech import text_to_speech
from cache_sounds import voices, types, paths, create_sound_lists, static_dict, word_dict, character_dict, cache_sounds, SAMPLE_RATE
import time
import os
import shutil

# Defining the App.
app = Flask(__name__)

# ----------------------------------------------------------------
# Enables the caching of different sound chunks.
create_sound_lists()
cache_sounds(voices, types, paths)

# To track if all the workers of Gunicorn executed the codes or not. 
print('Codes executed by Worker X')
# ----------------------------------------------------------------

# For testing.
@app.route("/", methods=['POST', 'GET'])
def test_root():
	return 'test_root'

# For testing.
@app.route("/test", methods=['POST', 'GET'])
def test():
	return 'test'

# Updating the cache is not working properly. For now we will skip it.
# Updating the cache.
# @app.route("/update_cache", methods=['POST'])
# def update_cache():
# 	zip_file = request.files['zip_file']
# 	print(zip_file.name)

# 	tik = time.time()

# 	# Saving the zip_file to the required destination and 
# 	zip_file.save('data/' + zip_file.name + '.zip')
# 	# Unzipping the file.
# 	command = 'unzip -o data/' + zip_file.name + '.zip' + ' -d data/'
# 	os.system(command)
# 	# Removing the zip file.
# 	os.remove('data/' + zip_file.name + '.zip')

# 	# Now start converting all text to speech.
# 	create_sound_lists()
# 	cache_sounds(voices, types, paths)

# 	# Making the cache ready True so to exectue the tts function.
# 	global is_cache_ready
# 	is_cache_ready = True

# 	tok = time.time()

# 	time_taken = tok - tik

# 	# Building up the json to be returned from this function.
# 	response_dict = {
# 		'time_taken': time_taken,
# 		'message': 'TTS Cache updated.'
# 	}

# 	response_json = json.dumps(response_dict)

# 	return response_json

# For TTS.
@app.route("/tts", methods=['POST'])
def tts():
	api_key = request.form.get('api_key')
	text = request.form.get('text')
	voice = request.form.get('voice')

	tik = time.time()

	# Now start converting all text to speech.
	sln_path, wav_path = text_to_speech(text, voice)

	# Getting the bytes from the sln file.
	f = open(sln_path, 'rb')
	file_bytes_sln = str(f.read())
	f.close()

	# Getting the bytes from the wav file.
	f = open(wav_path, 'rb')
	file_bytes_wav = str(f.read())
	f.close()

	# Now deleting the files.
	os.remove(wav_path)
	os.remove(sln_path)

	tok = time.time()

	time_taken = tok - tik

	# Building up the json to be returned from this function.
	response_dict = {
		'path_to_sln': sln_path,
		'path_to_wav': wav_path,
		'file_bytes_sln': file_bytes_sln,
		'file_bytes_wav': file_bytes_wav,
		'time_taken': time_taken,
		'message': '.wav and .sln file generated. Bytes sent as string.'
	}

	response_json = json.dumps(response_dict)

	return response_json


if __name__ == '__main__':
	# Making the App run with a host url.
	app.run(debug=True, host='0.0.0.0')

	# For production.
	# app.run(debug=False, host='0.0.0.0')