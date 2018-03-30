from config import *
from api_helpers import get_lyrics
from data_helpers import tokenize_and_process, pos_tagger
from model_persistance_helper import best_model
from text_draw import TextDraw
from file_helpers import check_create_folder
from mathe import translate

def ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))


def create_text_diagram(model, lyrics, file_name):

    text = lyrics
    lines = text.splitlines()
    lines = [line for line in lines if len(line) > 0]
    td = TextDraw(font_file, 15)
    lines_splited = []

    for line in lines:
        line_splited = line.split(" ")

        lines_splited.append(list([w, 0] for w in line_splited))

    flat_list = [item[0] for sublist in lines_splited for item in sublist]
    ngram_length = 5
    grams = ngrams(flat_list, ngram_length)

    grams = [(g, model.predict_proba([tokenize_and_process(" ".join(g), pos_tagger)])[0][0]) for g in grams]

    k = 0
    for a in lines_splited:
        for b in a:
            l = k-(ngram_length-1)
            if l < 0:
                l = 0
            grs = grams[l:k+1]
            k += 1
            b[1] = sum([g[1] for g in grs])/len(grs)



    for line in lines_splited:
        for word in line:
            mark = word[1]
            red = translate(mark, 0, 0.5, 255, 0)
            green = translate(mark, 0.5, 1, 0, 255)

            td.add(word[0], color=[int(red), int(green), 0])
        td.new_line()
    fn = "{}.{}".format( file_name, diagram_file_extension)
    file_path = os.path.join(diagrams_folder, fn)
    check_create_folder(file_path)
    td.save(file_path)
    return fn
