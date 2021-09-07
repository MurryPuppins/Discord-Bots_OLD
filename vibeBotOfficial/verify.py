import os

# VERY handy script that will automatically add new files in the gifs/images to the vibelist
# But does so in a fashion that it maintains the vibelist format
directory = 'memes'

with open('vibe.txt', 'r+') as f:
    lines = f.readlines()
    for file in os.listdir(directory):
        if ('>' + str(file) + '\n') not in lines:
            if file != ".DS_Store":
                f.write('>' + str(file) + '\n')

print("Finished meme file check")
