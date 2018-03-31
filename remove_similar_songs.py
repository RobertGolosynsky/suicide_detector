from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from data_helpers import get_documents
from config import categories
from file_helpers import silent_remove


def _find_similar(tfidf_matrix, index, top_n=10):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index + 1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]


def remove_similar_songs():
    corpus = []
    for cat in categories:
        for doc in get_documents(cat, lambda x: x):
            corpus.append((doc[2], " ".join(doc[0])))

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform([content for file, content in corpus])
    l = len(list(tfidf_matrix))

    indexes = []
    for i in range(0, l):
        print("progress {}".format(i * 100 / l))
        for index, similarity in _find_similar(tfidf_matrix, i, top_n=10):
            if similarity > 0.95:
                indexes.append(index)
                silent_remove(corpus[index][0])
