from gensim.models import KeyedVectors
import sys

# with open("./twitter_sample2/others/twitter_sample2_doc.vec") as f:
#     print(f)
# sys.exit()

# word_vecs = KeyedVectors.load_word2vec_format('./twitter_sample2/others/twitter_sample2_doc_exclude_stopwards_rank_10.vec', binary=False)
word_vecs = KeyedVectors.load_word2vec_format('./test/result/_result.vec', binary=False)

# print(word_vecs.wv.most_similar(positive=["メイク"],topn=100))

for v in word_vecs.wv.most_similar(positive=["ヒロインメイク"],topn=100):
    print(v)