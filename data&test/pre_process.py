with open("GRE_raw.txt") as f:
	lines = f.readlines()
	words = [line.split()[0] for line in lines]
	meanings = [" ".join(line.split()[1:]) for line in lines]

with open("words.txt", "w") as f:
	f.write(len(words))
	f.write('\n')
	for word in words:
		f.write(word)
		f.write('\n')

with open("meanings.txt", "w") as f:
	f.write(len(meanings))
	f.write('\n')
	for meaning in meanings:
		f.write(meaning)
		f.write('\n')
