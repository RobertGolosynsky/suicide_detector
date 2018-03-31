from PIL import Image, ImageFont, ImageDraw
from file_helpers import silent_remove
from config import *
from data_helpers import ngrams
from file_helpers import check_create_folder
from mathe import translate


class TextDraw:

    def __init__(self, font_file, font_size):
        self.font_file = font_size

        self.font = ImageFont.truetype(font_file, font_size)
        self.draw_table = []
        self._new_line = True

    def add(self, text, color):
        entry = (text, color)
        if self._new_line:
            self._new_line = False
            self.draw_table.append([entry])
        else:
            self.draw_table[-1].append(entry)

    def new_line(self):
        self._new_line = True

    def save(self, file_name):
        silent_remove(file_name)
        img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        draw = ImageDraw.Draw(img)
        vertical_margin = 20
        horizontal_margin = 20
        w, h = 0, 0
        line_spacing = 0
        max_width = 0
        space_width, space_height = draw.textsize(text=" ", font=self.font)

        for line in self.draw_table:
            h += line_spacing
            w = 0
            for text, color in line:
                line_width, line_height = draw.textsize(text=text, font=self.font)
                w += line_width + space_width
            if w > max_width:
                max_width = w
            h += space_height

        max_width += 2*horizontal_margin
        h += 2*vertical_margin
        img = Image.new('RGB', (max_width, h), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        w, h = 0, vertical_margin

        for line in self.draw_table:
            h += line_spacing
            w = horizontal_margin
            for text, color in line:
                line_width, line_height = draw.textsize(text=text, font=self.font)
                draw.text((w, h), text, font=self.font, fill=tuple(color))
                w += line_width + space_width

            h += space_height

        img.save(file_name)


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

