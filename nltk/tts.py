from nltk.corpus import inaugural, stopwords
from nltk import FreqDist, ConditionalFreqDist
import re

# pretty_name :: Address, Corpus? -> String
def pretty_name(address, corpus=inaugural):
	return "\t" + "    ".join([text_name[:-4] for text_name in address]) + "\t"

# excludes :: [String]? -> [String]
def excludes(excludeStrings=[]):
	return excludeStrings + excludePuncts([".\""]) + excludeWords()

# excludePuncts :: [String]? -> [String]
def excludePuncts(excludePunct=[]):
	return excludePunct + ["!", "?", "-", "--", ".", ",", ":", ";", "(", ")", "'", "\""]

# excludeWords :: [String]? -> [String]
def excludeWords(stopWords=[]):
	return stopWords + map(lambda unicode_str: unicode_str.encode(), stopwords.words("english"))

#Section 2, Task 1: Produce a list of overlapping lists of inaugural addresses
#Add script for inaug20 here:

# inaug20 :: Int?, Corpus? -> [[Address]]
def inaug20(num=5, corpus=inaugural):
	addresses = corpus.fileids()
	li = []
	
	while len(addresses) >= 5:
		li.append(addresses[:num])
		addresses = addresses[1:]
	
	return li

#Section 2, Task 2: Frequency distribution of words, excluding fn words and punct
#Add script for word_fdist here:

# word_fdist_single :: Address, [String]?, Corpus? -> FreqDist
def word_fdist_single(address, exclude=excludes(), corpus=inaugural):
	fd = FreqDist()
	
	for word in corpus.words(address):
		if not word.lower() in exclude:
			fd.inc(word.lower())
	
	return fd

# word_fdist :: [Address], [String]?, Corpus? -> FreqDist
def word_fdist(address_list, exclude=excludes(), corpus=inaugural):
	total_fd = FreqDist()
	
	for address in address_list:
		fd = word_fdist_single(address, exclude, corpus)
		for word in fd.keys():
			total_fd.inc(word, fd[word])
	
	return total_fd

#Section 2, Task 2: Also compute and print the 20 most common words in each
#of the overlapping 20-year periods. Add script for print_most_common here:

# print_most_common :: Int?, [Address]?, [String]?, Corpus? :: -> IO
def print_most_common(top=20, address_list=inaug20(), exclude=excludes(), corpus=inaugural):
	for address in address_list:
		print "******************* %s *******************" % pretty_name(address, corpus)
		print "Top %d most common words:" % top
		fd = word_fdist_single(address, exclude, corpus)
		for i in range(top):
			word = fd.keys()[i]
			print "\t%d\toccurences of\t%s " % (fd[word], word)
		print "\n\n\n"

#Section 2, Task 3: Frequency distribution of sentence lengths,
#excluding stopwords and punctuation. Add script for set_length_fdist here:

# sent_length_fdist_single :: Address, [String]?, Corpus? -> FreqDist
def sent_length_fdist_single(address, exclude=excludePuncts(), corpus=inaugural):
	fd = FreqDist()
	
	for sent in corpus.sents(address):
		nopunct_sent = [word for word in sent if not word in exclude]
		fd.inc(len(nopunct_sent))
	
	return fd

# sent_length_fdist :: [Address], [String]?, Corpus? -> FreqDist
def sent_length_fdist(address_list, exclude=excludePuncts(), corpus=inaugural):
	total_fd = FreqDist()
	
	for address in address_list:
		fd = sent_length_fdist_single(address, exclude, corpus)
		for len in fd.keys():
			total_fd.inc(len, fd[len])
	
	return total_fd

#Section 2, Task 3: Also compute and print the average sentence lengths in each of
#the overlapping 20-year periods. Add script for print_average_lengths here:

# print_average_lengths :: [Address]?, [String]?, Corpus? -> IO
def print_average_lengths(address_list=inaug20(), exclude=excludePuncts(), corpus=inaugural):
	for address in address_list:
		print "^^^^^^^^^^^^^^^^^^^^^^^ %s ^^^^^^^^^^^^^^^^^^^^^^^" % pretty_name(address, corpus)
		fd = sent_length_fdist_single(address, exclude, corpus)
		total_len = 0
		amount = 0
		for len in fd.keys():
			total_len += len*fd[len]
			amount += fd[len]
		avg_len = total_len/amount
		print "Average sentence length: %d\n\n\n" % avg_len

#Section 2, Task 4: Conditional freq distribution of words following 'I'/'my' or
#preceding 'me', plus printing samples that occur >1 for each pro-period pair.
#Add your script for build_cond_fdist here:

# build_cond_fdist :: [String]?, Corpus? -> ConditionalFreqDist
def build_cond_fdist(exclude=excludes(), corpus=inaugural):
	cfd = ConditionalFreqDist()
	prev = None
	
	for fileid in corpus.fileids():
		year = int(fileid[:4])
		for word in corpus.words(fileid):
			if prev in ["I", "my"] and word.lower() not in exclude:
				cfd[(year, prev)].inc(word)
			if word in ["me"] and prev.lower() not in exclude:
				cfd[(year, word)].inc(prev)
			prev = word
	
	return cfd
	
#Section 2, Task 4: Also compute and print, for each pronoun and each 20-year
#period, the list of words accompanying the pronoun more than once in the
#addresses within the period. Add your script for print_Imyme_words here:

# print_Imyme_words :: ConditionalFreqDist -> IO
def print_Imyme_words(cfd):
	years = range(1789, 2009+1, 4)
	pronouns = ["I", "my", "me"]
	
	for pronoun in pronouns:
		print "\n\n\n~~~ Words occuring more than once %s \"%s\" ~~~\n" % ("before" if pronoun == "me" else "after", pronoun)
		
		conditions = zip(years, [pronoun]*len(years))
		
		for (freq, word) in build_sorted_list(cfd, conditions):
			print "\t%d\toccurences of\t%s " % (freq, word)
	
	periods = [[int(address[:4]) for address in period] for period in inaug20() ]
	
	for period in periods:
		print "\n\n\n~~~~~~~~~~~~~~~~~ Words occuring more than once before \"me\" or after \"I\" or \"my\" from %s to %s ~~~~~~~~~~~~~~~~~\n" % (period[0], period[-1])
		
		conditions = [(year, pronoun) for pronoun in pronouns for year in period]
		
		for (freq, word) in build_sorted_list(cfd, conditions):
			print "\t%d\toccurences of\t%s " % (freq, word)

# build_sorted_list :: ConditionalFreqDist, [(Int, String)] -> [(Int, String)]
def build_sorted_list(cfd, conditions):
	dict = {}
	for condition in conditions:
		for word in cfd[condition].keys():
			if word in dict:
				dict[word] += 1
			else:
				dict[word] = 1
	
	li = [(dict[word], word) for word in dict if dict[word] > 1]
	
	return sorted(li, reverse=True)

# Testing
if __name__ == "__main__":
	print inaug20()
	print_most_common()
	print_average_lengths()
	print_Imyme_words(build_cond_fdist())
	
#End of file
