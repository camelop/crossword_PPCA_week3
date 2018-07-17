# read in
with open("GRE_raw.txt") as f:
	lines = f.readlines()
	words = [line.split()[0] for line in lines]
	meanings = [" ".join(line.split()[1:]) for line in lines]

# clean data
new_words = []
new_meanings = []
for i in range(len(words)):
	if words[i].isalpha():
		new_words.append(words[i])
		new_meanings.append(meanings[i])
words = new_words
meanings = new_meanings

# write out
with open("words.txt", "w") as f:
	f.write(str(len(words)))
	f.write('\n')
	for word in words:
		f.write(word.upper())
		f.write('\n')
with open("meanings.txt", "w") as f:
	f.write(str(len(meanings)))
	f.write('\n')
	for meaning in meanings:
		f.write(meaning)
		f.write('\n')
 