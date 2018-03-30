import glob
from config import *

# changes data structure so that it can be fed to the TextCNN

output_suicidal = "suicide_lyrics.txt"
output_not_suicidal = "not_suicidal_lyrics.txt"

with open(output_suicidal, "w", encoding="utf-8") as f:
    for file in glob.glob("{}/*.txt".format(suicidal_folder_path)):
        s = open(file, "r", encoding="utf-8").read()
        f.write(s.replace("\n", " ")+"\n")

with open(output_not_suicidal, "w", encoding="utf-8") as f:
    for file in glob.glob("{}/*.txt".format(not_suicidal_folder_path)):
        s = open(file, "r", encoding="utf-8").read()
        f.write(s.replace("\n", " ")+"\n")

