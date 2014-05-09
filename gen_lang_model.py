import nltk
from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.model import NgramModel
import os

# Returns a list containing all tokens from the data set (any text file in /data/)
def get_tokens_from_data():
	all_words = []

	file_names = os.listdir(os.curdir + "/data")

	for name in file_names:
		f = file(os.curdir + "/data/" + name)
		for token in nltk.word_tokenize(f.read()):
			if token.isalpha():
				all_words.append(token.lower())

	return all_words

# 
def build_ngrams(tokens):

	unigrams = []
	bigrams = []
	trigrams = []
	fourgrams = []
	fivegrams = []

	for token in tokens:
		unigrams += nltk.util.ngrams(word,1)
		bigrams += nltk.util.ngrams(word,2)
		trigrams += nltk.util.ngrams(word,3)
		fourgrams += nltk.util.ngrams(word,4)
		fivegrams += nltk.util.ngrams(word,5)

	return unigrams, bigrams, trigrams, fourgrams, fivegrams

def get_ngram_counts(ngram):

	count_dict = {}

	for gram in ngram:
		if gram in count_dict.keys():
			count_dict[gram] += 1
		else:
			count_dict[gram] = 1

	return count_dict


def main():
	all_words = get_tokens_from_data()

	unigrams, bigrams, trigrams, fourgrams, fivegrams = build_ngrams(all_words)


	unigram_counts = get_ngram_counts(unigrams)
	print "done with unigrams"
	bigram_counts = get_ngram_counts(bigrams)
	print "done with bigrams"
	trigram_counts = get_ngram_counts(trigrams)
	print "done with trigrams"
	fourgram_counts = get_ngram_counts(fourgrams)
	print "done with fourgrams"
	fivegram_counts = get_ngram_counts(fivegrams)
	print "done with fivegrams"

	# for word in all_words[:10]:
	# 	print nltk.util.ngrams(word, 3)






if __name__ == "__main__":
	main()
