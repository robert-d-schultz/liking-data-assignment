import nltk
import numpy
import re
import csv
import gensim
import operator
import collections

source_text = []
stemmed_text = []
tokenized_text = []
pos_text = []
count_text = []
no_stop_text = []
no_stop_text2 = []

def preprocess():
	# first stem and lowercase words, then remove rare
	# lowercase
	global source_text
	source_text = [text.lower() for text in source_text]

	global count_text
	count_text = [len(text.split()) for text in source_text]

	# tokenize
	global tokenized_text
	tokenized_text = [nltk.word_tokenize(text) for text in source_text]

	'''# stem
	porter = nltk.PorterStemmer()
	global stemmed_text
	stemmed_text = [[porter.stem(t) for t in tokens] for tokens in tokenized_text]

	# remove rare
	vocab = nltk.FreqDist(w for line in stemmed_text for w in line)
	rarewords_list = set(vocab.hapaxes())
	stemmed_text = [['<RARE>' if w in rarewords_list else w for w in line] for line in stemmed_text]

	# pos
	global pos_text
	pos_text = [[a[1] for a in nltk.pos_tag(text)] for text in tokenized_text]

	# stop words
	global no_stop_text
	no_stop_text = [[word for word in text if word not in nltk.corpus.stopwords.words('english')] for text in stemmed_text]

	global no_stop_text2
	no_stop_text2 = [[word for word in text if word not in nltk.corpus.stopwords.words('english')] for text in tokenized_text]'''


# avg word vec of responses
def avg_word_vec():
	model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin', binary=True)
	out = []
	for text in tokenized_text:
		avg = numpy.zeros(300)
		cnt = 0
		for word in text:
			if (word in model.vocab):
				avg = numpy.add(avg, model[word])
				cnt += 1
		if cnt == 0:
			avg_vec = avg
		else:
			avg_vec = avg / cnt
		out.append(avg_vec.tolist())
	return numpy.asarray(out).T.tolist()

def extract_features(text):
	global source_text
	source_text = text			# we'll use global variables to pass the data around

	preprocess()

	features = []		# features will be list of lists, each component list will have the same length as the list of input text

	features.extend(avg_word_vec())

	features = numpy.asarray(features).T.tolist()

	return features
