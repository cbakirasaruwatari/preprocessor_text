from gensim.models import KeyedVectors
word_vecs = KeyedVectors.load_word2vec_format('./twitter_sample2/skipgram/twitter_sample2.vec', binary=False)
print(word_vecs.wv.most_similar(positive=['下地']))

