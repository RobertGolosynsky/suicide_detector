from api_helpers import get_lyrics
from model_persistance_helper import best_model
model = best_model()
if not model:
    print("No prediction model checkpoint found. Aborting.")
    exit(0)

while True:
    print("Input an artist and his song ('-' separated) and figure out if the song has suicidal tendencies")
    raw = input()
    sliced = raw.split("-")
    if len(sliced) < 2:
        print("Separate artist and song with '-' ")
        continue

    lyrics = get_lyrics(sliced[0], sliced[1])
    if lyrics:
        print("Lyrics: ")
        print(lyrics)
        print()
        print(model.predict([lyrics]))
    else:
        print("Song not found")
