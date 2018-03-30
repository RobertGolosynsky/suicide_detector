from config import *
from api_helpers import get_lyrics
from model_persistance_helper import best_model
from text_draw import TextDraw


def ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))


model = best_model()
song = "Nirvana-smells"
text = get_lyrics(*song.split("-"))
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
grams = [(g, model.predict_proba([" ".join(g)])[0][0]) for g in grams]

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
        td.add(word[0], color=[int(255*word[1]), int(255*(1-word[1])), 0])
    td.new_line()

td.save("{}/{}.png".format(diagrams_folder, song))
