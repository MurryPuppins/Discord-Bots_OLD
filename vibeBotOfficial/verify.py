import os

directory = 'memes'

with open('vibe.txt', 'r+') as f:
    lines = f.readlines()
    for file in os.listdir(directory):
        if ('>' + str(file) + '\n') not in lines:
            if file != ".DS_Store":
                f.write('>' + str(file) + '\n')

print("Finished meme file check")
