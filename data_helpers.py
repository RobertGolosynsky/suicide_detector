import glob
import traceback

from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from config import *
from plots import plot_confusion_matrix


def save_text(file_name, text):
    try:
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except:  # Guard against race condition
                traceback.print_exc()
        file = open(file_name, "w", encoding="utf-8")
        file.write(text)
        file.close()
    except:
        traceback.print_exc()
        return


def get_documents(category):
    valid_categories = categories
    if category not in valid_categories:
        raise ValueError("Category must be one of: {}".format(valid_categories))

    documents = []
    porter_stemmer = PorterStemmer()
    folder_path = not_suicidal_folder_path if category == not_suicidal_category_name else suicidal_folder_path
    for file in glob.glob(os.path.join(folder_path, "*.txt".format(folder_path))):
        words = word_tokenize(open(file, "r", encoding="utf-8").read())
        #pos_tagged_words = nltk.pos_tag(words)
        #pos_tagged_words = [" ".join(w) for w in pos_tagged_words]

        stemmed_words = [porter_stemmer.stem(w) for w in words]
        documents.append((stemmed_words, category))
    return documents


def save_plots(y_test, predictions, categories, pipe_name, report):
    plot_confusion_matrix(y_test, predictions, categories, pipe_name, current_checkpoint_directory, normalize=True)
    save_text(os.path.join(current_checkpoint_directory, "{}.{}".format(pipe_name, report_file_extension)), report)
