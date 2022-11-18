def number_to_text(number):
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
		'3': 'tin',
		'4': 'char',
		'5': 'panch',
		'6': 'chhe',
		'7': 'saat',
		'8': 'aath',
		'9': 'nao',

		'00': 'sunya',
		'01': 'ek',
		'02': 'do',
		'03': 'tin',
		'04': 'char',
		'05': 'panch',
		'06': 'chhe',
		'07': 'saat',
		'08': 'aath',
		'09': 'nao',

		# Double digit nubers.
		'10': 'das',
		'11': 'igyara',
		'12': 'bara',
		'13': 'tera',
		'14': 'chaoda',
		'15': 'pandra',
		'16': 'sola',
		'17': 'satra',
		'18': 'athra',
		'19': 'unis',
		
		'20': 'bis',
		'21': 'ikis',
		'22': 'bais',
		'23': 'teis',
		'24': 'chaobis',
		'25': 'pachis',
		'26': 'chhabis',
		'27': 'satais',
		'28': 'athais',
		'29': 'unatis',
		'30': 'tis',

		'31': 'ikatis',
		'32': 'batis',
		'33': 'taetis',
		'34': 'chaotis',
		'35': 'paetis',
		'36': 'chhatis',
		'37': 'saetis',
		'38': 'athtis',
		'39': 'untalis',

		'40': 'chalis',
		'41': 'ikchalis',
		'42': 'bayalis',
		'43': 'tiyalis',
		'44': 'chaowalis',
		'45': 'paentanis',
		'46': 'chhialis',
		'47': 'saentanish',
		'48': 'athtalis',
		'49': 'unachas',

		'50': 'pachas',
		'51': 'ikyaban',
		'52': 'baban',
		'53': 'tirepan',
		'54': 'chaowan',
		'55': 'pachpan',
		'56': 'chhapan',
		'57': 'sataban',
		'58': 'athaban',
		'59': 'unsath',

		'60': 'sath',
		'61': 'iksath',
		'62': 'basath',
		'63': 'tesath',
		'64': 'chaosath',
		'65': 'paensath',
		'66': 'chhiesath',
		'67': 'satsath',
		'68': 'athsath',
		'69': 'unatar',

		'70': 'satar',
		'71': 'ikathar',
		'72': 'bahatar',
		'73': 'tihatar',
		'74': 'chaohatar',
		'75': 'pachatar',
		'76': 'chhihatar',
		'77': 'satatar',
		'78': 'atatar',
		'79': 'unyasi',

		'80': 'asi',
		'81': 'ikyasi',
		'82': 'bayasi',
		'83': 'tiyasi',
		'84': 'chowasi',
		'85': 'pichasi',
		'86': 'chhiasi',
		'87': 'satasi',
		'88': 'atasi',
		'89': 'inyanbe',

		'90': 'nabe',
		'91': 'ikyanbe',
		'92': 'biyanbe',
		'93': 'tiranbe',
		'94': 'chowanbe',
		'95': 'pachanbe',
		'96': 'chhianbe',
		'97': 'satanbe',
		'98': 'athanbe',
		'99': 'ninyanbe',
	}

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
	print(number_to_text('100'))