import glob
import traceback

import nltk
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from config import *
from file_helpers import check_create_folder
from plots import plot_confusion_matrix


def save_text(file_name, text):
    try:
        check_create_folder(file_name)
        file = open(file_name, "w", encoding="utf-8")
        file.write(text)
        file.close()
    except:
        traceback.print_exc()
        return


def get_documents(category, words_processor):
    valid_categories = categories
    if category not in valid_categories:
        raise ValueError("Category must be one of: {}".format(valid_categories))

    documents = []
    folder_path = not_suicidal_folder_path if category == not_suicidal_category_name else suicidal_folder_path
    for file in glob.glob(os.path.join(folder_path, "*.txt".format(folder_path))):
        line = open(file, "r", encoding="utf-8").read()
        documents.append((tokenize_and_process(line, words_processor), category))
    return documents


def save_plots(y_test, predictions, categories, pipe_name, report):
    plot_confusion_matrix(y_test, predictions, categories, pipe_name, current_checkpoint_directory, normalize=True)
    save_text(os.path.join(current_checkpoint_directory, "{}.{}".format(pipe_name, report_file_extension)), report)


def pos_tagger(words):
    pos_tagged_words = nltk.pos_tag(words)
    pos_tagged_words = [" ".join(w) for w in pos_tagged_words]
    return pos_tagged_words


def tokenize_and_process(line, words_processor):
    line = line.lower()
    return words_processor(word_tokenize(line))
