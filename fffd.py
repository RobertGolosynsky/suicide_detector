from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import movie_reviews
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import glob
from nltk import word_tokenize


def create_pipelines():
    bow_nb = Pipeline(
            [
                ("bow", CountVectorizer(ngram_range=(1, 1), lowercase=False, analyzer='word', tokenizer=lambda x:x)),
                ("nb", MultinomialNB())
            ]
        )
    tfidf_nb = Pipeline(
            [
                ("tf_idf", TfidfVectorizer(ngram_range=(1, 1), lowercase=False, analyzer='word', tokenizer=lambda x: x,
                                           use_idf=True)),
                ("nb", MultinomialNB())
            ]
        )
    tfidf_svm = Pipeline(
            [
                ("tf_idf", TfidfVectorizer(ngram_range=(1, 1), lowercase=False, analyzer='word', tokenizer=lambda x: x,
                                           use_idf=True)),
                ("svm", SVC(kernel="linear"))
            ]
        )
    tfidf_nn = Pipeline(
            [
                ("tf_idf", TfidfVectorizer(ngram_range=(1, 1), lowercase=False, analyzer='word', tokenizer=lambda x: x,
                                           use_idf=True)),
                ("mlp", MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=20, random_state=1))
            ]
        )
    return [
               ("BOW_NB", bow_nb),
               ("TFIDF_NB", tfidf_nb),
               ("TFIDF_SVM", tfidf_svm),
               ("TFIDF_MLP", tfidf_nn)
    ]


#nltk.download('movie_reviews')
# documents = [([w.lower() for w in movie_reviews.words(fileid)], category)
#               for category in movie_reviews.categories()
#               for fileid in movie_reviews.fileids(category)]


def get_documents(category):
    documents = []
    for file in glob.glob("{}/*.txt".format(category)):
        words = word_tokenize(open(file, "r").read())
        documents.append((words,category))
    return documents


documents = get_documents("suicide")
documents += get_documents("nosuicide")[:len(documents)]

X = [d[0] for d in documents]
y = [d[1] for d in documents]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



for pipe_name, pipe in create_pipelines():
    pipe.fit(X_train, y_train)
    predictions = pipe.predict(X_test)
    report = classification_report(y_test, predictions)
    print(pipe_name)
    print(report)




