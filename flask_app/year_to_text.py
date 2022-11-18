def year_to_text(number):
	"""This fucntion takes input a number in it's text form and returns it's 
	speaking words as a single string.
	"""

	# Defining a few variables needed for the function.
	END = '\n\n'

	number_word_dict = {
		# Single digit numbers
		'0': 'sunya',
		'1': 'ek',
		'2': 'do',

		'00': 'sunya',
		'01': 'ek',
		'02': 'do',
		'10': 'das',

		# Double digit nubers.
		'11': 'igyara',
		'12': 'bara',
		'22': 'bais',
		'21': 'ikis'
	}

	try:
		if number[-3] != '0' and len(number) == 4:
			number_split_pattern = [2, 2, 2, 2, 2]
		else:
			# The way we will split the numbers 
			number_split_pattern = [2, 1, 2, 2, 2]
	except:
		# The way we will split the numbers 
		number_split_pattern = [2, 1, 2, 2, 2]

	# Will contain all the number splits in reverse order as we split in from the 
	# left to right the way we read numbers. 
	number_splits_reversed = [] 

	# Reversing the number
	number_reversed = number[::-1]
	# print(number_reversed, end=END)

	i = 0
	j = 0

	while i < len(number_reversed):
		number_split_value = number_split_pattern[j]
		j = j + 1
		
		number_splits_reversed.append(number_reversed[i : i + number_split_value])
		i = i + number_split_value

	# print(number_splits_reversed, end=END)

	# Each value in number_splits_reverse is also reversed. So reversing it back to 
	# set all those it's normal way.
	number_splits_reversed_proper = []

	for i in range(len(number_splits_reversed)):
		split = number_splits_reversed[i]
		split = split[::-1]
		number_splits_reversed_proper.append(split)

	# print(number_splits_reversed_proper, end=END)

	# Now creating the number to word program.
	number_words = []

	positional_words = ['', 'sao', 'hazar', 'lakh', 'karod']

	for i in range(len(number_splits_reversed_proper)):
		split = number_splits_reversed_proper[i]

		# Now skipping the words if the split is '0' or '00'
		if split == '0' or split == '00':
			continue

		split_word = number_word_dict[split]
		positional_word = positional_words[i]

		# The couple of the number text and it's positonal value text.
		number_positional_couple = [split_word, positional_word]

		number_words.append(number_positional_couple)

	# Reversing the number words so that we can get the original way of text, the 
	# way it shoudl be read.
	number_words.reverse()

	number_text = ''

	for i in range(len(number_words)):
		number_positional_couple = number_words[i]
		number_text = number_text +  number_positional_couple[0] + ' ' + number_positional_couple[1] + ' '

	# Stripping out the number text in order to get rid of the extra spaces if 
	# present.
	number_text = number_text.strip()

	# print(number_words, end=END)

	# print(number_text)

	return number_text

if __name__ == '__main__':
	print(year_to_text('1010'))