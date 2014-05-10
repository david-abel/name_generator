import nltk
import os
import numpy
import random
import pickle
from collections import defaultdict

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
			# Only add count if there are enough chars
			if len(token[:n]) == n:
				ngrams.append(("^",token[0])) # START
				ngrams.append((token[-1],"$")) # END
	return ngrams

# Returns a dictionary with <token> -> <counts> pairs for the specified ngram
def get_ngram_counts(ngrams):

	count_dict = defaultdict(int)

	for gram in ngrams:
		count_dict[gram] += 1

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

def sample(ngram_counts):
  	unigram_probs = counts_to_probs(ngram_counts)
  	sampleMult = numpy.random.dirichlet(ngram_counts.values(),1)
  	sampleList = numpy.random.multinomial(1, sampleMult[0])
	resultIndex = sampleList.argmax()
	result = unigram_probs.keys()[resultIndex]

	return result[0]

def combine_counts_for_string(text_so_far, unigrams, weights=[1,1,1,1,1], *ngrams):
	
	all_count_dict = unigrams # Probabilities we give to the multinomial after sampling dirichlets for all ngrams

	for ngram in ngrams:
		n = len(ngram.keys()[0])
		# Fancy shmancy dictionary so we don't have to check existence first
		count_dict = defaultdict(int)
		prevChars = text_so_far[-1:-n:-1] # Gets previous n-1 chars from the text_so_far
			
		for key in ngram.keys():
			# If the previous chars are the same, and there are enough chars for the ngram, incremement the counts
			if len(key[:n-1]) == n-1 and key[:n-1] == prevChars:
				count_dict[key[-1]] += 1 * weights[n-1]

		for key in count_dict.keys():
			all_count_dict[key] += count_dict[key]

	return all_count_dict

def get_terminate_prob(text_so_far, weight=1, *ngrams):
	return 0.3

	for ngram in ngrams:
		n = len(ngram.keys()[0])
		prevChars = text_so_far[-1:-n - 1:-1] # Gets previous n-1 chars from the text_so_far
		for key in ngram.keys():
			prevChars = text_so_far[-1:-n:-1] # Gets previous n-1 chars from the text_so_far
			
			# If the previous chars are the same, and there are enough chars for the ngram, incremement the counts
			if len(key[:n-1]) == n-1 and key[:n-1] == prevChars:
				count_dict[key[-1]] += 1 * weights[n-1]



def main():
	# create_and_save_ngram_counts()
	# quit()
	
	weights = [1,2,3,4,5]

 	# Load
	with open('ngrams/unigram_counts.pickle', 'rb') as handle:
  		unigram_counts = pickle.load(handle)
  	with open('ngrams/bigram_counts.pickle', 'rb') as handle:
  		bigram_counts = pickle.load(handle)	
	with open('ngrams/trigram_counts.pickle', 'rb') as handle:
  		trigram_counts = pickle.load(handle)
  	with open('ngrams/fourgram_counts.pickle', 'rb') as handle:
  		fourgram_counts = pickle.load(handle)	
  	with open('ngrams/fivegram_counts.pickle', 'rb') as handle:
  		fivegram_counts = pickle.load(handle)	

  	print bigram_counts
  	quit()

  	candidate_name = "^"

  	for i in xrange(10):
  		# Combine counts for all n-grams and sample a letter
	  	all_count_dict = combine_counts_for_string(candidate_name, unigram_counts, weights, bigram_counts, trigram_counts, fourgram_counts, fivegram_counts)
	  	candidate_name += sample(all_count_dict)
  		
  		# Decide when to end the word, allow minimum of 3 letters and maximum of 10 letters, for now
  		if i > 3:
	  		terminate_prob = get_terminate_prob(candidate_name, unigram_counts, bigram_counts, trigram_counts, fourgram_counts, fivegram_counts)
			if terminate_prob > random.random():
				break


	print candidate_name.replace("^","").replace("$","")

if __name__ == "__main__":
	main()
