import nltk
from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.model import NgramModel
import os
import numpy
import random
import pickle

# Returns a list containing all tokens from the data set (any text file in /data/)
def tokenize_data():
	all_words = []

	file_names = os.listdir(os.curdir + "/data")

	for name in file_names:
		f = file(os.curdir + "/data/" + name)
		for token in nltk.word_tokenize(f.read()):
			if token.isalpha():
				all_words.append(token.lower())

	return all_words

# Returns a tuple containing all of the unigrams, bigrams, trigrams, fourgrams, and givegrams from the input "tokens"
def build_ngrams(tokens, n):

	ngrams = []

	# Build standard ngram tokens
	for token in tokens:
		ngrams += nltk.util.ngrams(token,n)

	if n > 1:
		# Add the "start" and "end" character ngrams
		for token in tokens:
			ngrams.append(("^",token[:n])) # START
			ngrams.append((token[-1:-n:-1],"$")) # END
	return ngrams

# Returns a dictionary with <token> -> <counts> pairs for the specified ngram
def get_ngram_counts(ngrams):

	count_dict = {}

	for gram in ngrams:
		if gram in count_dict.keys():
			count_dict[gram] += 1
		else:
			count_dict[gram] = 1

	return count_dict

def counts_to_probs(ngrams):
	total = sum(ngrams.values())

	ngram_probs = {}

	for key in ngrams.keys():
		ngram_count = float(ngrams[key])/total
		ngram_probs[key] = ngram_count

	return ngram_probs

# 
def add_char(text):
	return text

def create_and_save_ngram_counts():
	debug = True

	# TOKENIZE
	all_words = tokenize_data()
	if debug: print "done tokenizing"

	# CREATE NGRAMS
	unigrams = build_ngrams(all_words, 1)
	bigrams = build_ngrams(all_words, 2)
	trigrams = build_ngrams(all_words, 3)
	fourgrams = build_ngrams(all_words, 4)
	fivegrams = build_ngrams(all_words, 5)
	if debug: print "done creating ngrams"

	# COUNT
	unigram_counts = get_ngram_counts(unigrams)
	if debug: print "done with unigrams"
	
	bigram_counts = get_ngram_counts(bigrams)
	if debug: print "done with bigrams"

	trigram_counts = get_ngram_counts(trigrams)
	if debug: print "done with trigrams"
	
	fourgram_counts = get_ngram_counts(fourgrams)
	if debug: print "done with fourgrams"
	
	fivegram_counts = get_ngram_counts(fivegrams)
	if debug: print "done with fivegrams"


	with open('ngrams/unigram_counts.pickle', 'wb') as handle:
  		pickle.dump(unigram_counts, handle)
	with open('ngrams/bigram_counts.pickle', 'wb') as handle:
  		pickle.dump(bigram_counts, handle)
	with open('ngrams/trigram_counts.pickle', 'wb') as handle:
  		pickle.dump(trigram_counts, handle)
	with open('ngrams/fourgram_counts.pickle', 'wb') as handle:
  		pickle.dump(fourgram_counts, handle)
	with open('ngrams/fivegram_counts.pickle', 'wb') as handle:
  		pickle.dump(fivegram_counts, handle)


def main():
	create_and_save_ngram_counts()
  	quit()

 	# Load
	with open('unigram_probs.pickle', 'rb') as handle:
  		unigram_probs = pickle.load(handle)

	print unigram_probs
	quit()

	rand_double = random.random()
	kill_threshold = 1.0

	length_bias = 0.05

	result = "^"

	while rand_double < kill_threshold:
		result = add_char(result)
		# Then get another random value, add a bias term so the longer result is, the more likely we are to terminate.
		rand_double = random.random() + (length_bias * len(result))

	result = result[0].upper() + result[1:]

	print result




if __name__ == "__main__":
	main()
