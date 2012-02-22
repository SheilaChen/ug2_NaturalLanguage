from nltk import pos_tag
import nltk
import re
from nonVBG import *

#Section 3, Task 1: Use pos_tag to tag each word in every sentence in a list.
#Add script for tag_sentences here:

# tag_sentences :: [String] -> [[(String, String)]]
def tag_sentences(sent_list):
	return map(lambda sent: pos_tag(sent), sent_list)

#Section3, Task 1: Given a list of tagged sentences, build and return
#a dictionary whose keys are words ending in 'ing', where the value
#associated with a w is a *list* of all pos-tags assigned to w anywhere
#in the given sentences.
#Add script for build_ing_dict here:

# build_ing_dict :: [[(String, String)]] -> {String : [String]}
def build_ing_dict(tag_sent_list):
	dict = {}
	pattern = "(^|\b)[A-Z]?[a-z]*ing(\b|$)"
	
	for tag_sent in tag_sent_list:
		for (word, tag) in tag_sent:
			if re.match(pattern, word):
				if word in dict:
					dict[word].append(tag)
				else:
					dict[word] = [tag]
	
	return dict

#Section 3, Task 2: Re-tag 'ing' words that follow a preposition
#and aren't in nonVBG. Add script for retag_sentence here:

# retag_sentence :: [(String, String)] -> [(String, String)]
def retag_sentence(tag_sent):
	retag_sent = []
	prev_tag = None
	
	for (word, tag) in tag_sent:
		if word.endswith("ing") and word not in nonVBG and prev_tag == "IN":
			retag_sent.append((word, "VBG"))
		else:
			retag_sent.append((word, tag))
		prev_tag = tag
	
	return retag_sent

# retag_sentences :: [[(String, String)]] -> [[(String, String)]]
def retag_sentences(tag_sent_list):
	return map(lambda tag_sent: retag_sentence(tag_sent), tag_sent_list)

# Testing
if __name__ == "__main__":
	tag_sent_list_obama = tag_sentences(nltk.corpus.inaugural.sents("2009-Obama.txt"))
	tag_sent_list_wash1 = tag_sentences(nltk.corpus.inaugural.sents("1789-Washington.txt"))
	dict_obama = build_ing_dict(tag_sent_list_obama)
	dict_wash1 = build_ing_dict(tag_sent_list_wash1)
	dict_obama_retag = build_ing_dict(retag_sentences(tag_sent_list_obama))
	dict_wash1_retag = build_ing_dict(retag_sentences(tag_sent_list_wash1))
	
	print "dict_obama\t\t",
	print dict_obama
	print "dict_obama_retag\t",
	print dict_obama_retag
	
	print "\n"
	
	print "dict_wash1\t\t",
	print dict_wash1
	print "dict_wash1_retag\t",
	print dict_wash1_retag

#End of File
