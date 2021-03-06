import nltk
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from data_helpers import get_documents, save_plots, default_tokenizer_and_pos_tagger
from model_persistance_helper import save_model
from config import *



# TODO: CROSS VALIDATION
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')



def create_pipelines():
    pipes = []
    for ngram in range(1, 3):
        bow_nb = Pipeline(
                [
                    ("bow", CountVectorizer(ngram_range=(1, ngram), lowercase=True, analyzer='word', tokenizer=default_tokenizer_and_pos_tagger)),
                    ("nb", MultinomialNB())
                ]
            )

        tfidf_nb = Pipeline(
                [
                    ("tf_idf", TfidfVectorizer(ngram_range=(1, ngram), lowercase=True, analyzer='word', tokenizer=default_tokenizer_and_pos_tagger,
                                               use_idf=True)),
                    ("nb", MultinomialNB())
                ]
            )
        tfidf_svm = Pipeline(
                [
                    ("tf_idf", TfidfVectorizer(ngram_range=(1, ngram), lowercase=True, analyzer='word', tokenizer=default_tokenizer_and_pos_tagger,
                                               use_idf=True)),
                    ("svm", SVC(kernel="linear", probability=True))
                ]
            )

        tfidf_nn = Pipeline(
                [
                    ("tf_idf", TfidfVectorizer(ngram_range=(1, ngram), lowercase=True, analyzer='word', tokenizer=default_tokenizer_and_pos_tagger,
                                               use_idf=True)),
                    ("mlp", MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(20), random_state=1))
                ]
            )

        pipes.append(tfidf_nb)
        pipes.append(tfidf_svm)
        pipes.append(tfidf_nn)
        pipes.append(bow_nb)
    return pipes


should_save_plots = True

docs = []
for category in categories:
    docs.append(get_documents(category))

l = min(len(d) for d in docs)
documents = []
for d in docs:
    documents += d[:l]

X, y, _ = zip(*documents)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


for pipe in create_pipelines():
    pipe_name = " ".join([name for name, _ in pipe.steps] + ["ngramrange{}".format(pipe.steps[0][1].ngram_range)])
    pipe.fit(X_train, y_train)
    save_model(pipe, pipe_name)

    predictions = pipe.predict(X_test)
    report = classification_report(y_test, predictions)

    print(pipe_name)
    print(report)

    if should_save_plots:
        save_plots(y_test, predictions, categories, pipe_name, report)







