import nltk
from pprint import pprint

from time import time
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report

from data_helpers import get_documents, save_plots, default_tokenizer_and_pos_tagger
from model_persistance_helper import save_model
from config import *



# TODO: CROSS VALIDATION
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

pipeline = Pipeline(
    [
        ("tf_idf", TfidfVectorizer(ngram_range=(1, 1), lowercase=True, analyzer='word',
                                   tokenizer=default_tokenizer_and_pos_tagger,
                                   use_idf=True)),
        ("svm", SVC(kernel="linear", probability=True))
    ]
)


docs = []
for category in categories:
    docs.append(get_documents(category))

l = min(len(d) for d in docs)
documents = []
for d in docs:
    documents += d[:l]

X, y, _ = zip(*documents)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

parameters = {
    'tf_idf__max_df': (0.05, 0.1, 0.2),
    'tf_idf__max_features': (None, 5000, 10000, 50000),
    'tf_idf__ngram_range': ((1, 1), (1, 2), (1, 3)),  # unigrams or bigrams
    # 'tf_idf__norm': ('l1', 'l2'),
    'svm__kernel': ('linear', 'poly', 'rbf', 'sigmoid'),
    # 'svm__probability': [True],
}

if __name__ == "__main__":
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=10)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(X, y)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))






