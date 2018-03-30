from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from file_helpers import silent_remove

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
