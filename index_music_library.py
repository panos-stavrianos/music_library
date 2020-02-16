import logging
import os
from os.path import splitext, basename

import eyed3
import pandas as pd


def index_music_library():
    library_path = os.getenv('MUSIC_LIBRARY_PATHS', "")
    if library_path == "":
        exit(0)
    logging.basicConfig(filename='index_music_library.log', filemode='w', level="INFO",
                        format='%(message)s')

    songs = pd.DataFrame(columns=["artist", "album", "title", "release_date", "filename", "path", "full_text"])

    logging.info("Start Indexing")
    eyed3.log.setLevel("ERROR")
    log_file = os.path.abspath("index_music_library.log")
    file_paths = []
    os.system('gnome-terminal -- tail -F "{}"'.format(log_file))
    if not os.path.exists("file_paths.txt"):

        file_paths = []
        for root, dirs, files in os.walk(library_path):
            print(root)
            logging.info("Indexing->" + root)

            for file in files:
                try:
                    if file.find(".mp3") < 0:
                        continue
                    file_path = os.path.abspath(os.path.join(root, file))
                    file_paths.append(file_path)

                except Exception as e:
                    logging.error(e)
                    continue

        with open("file_paths.txt", "w") as f:
            f.writelines("%s\n" % f_p for f_p in file_paths)

    with open("file_paths.txt") as f:
        file_paths = [current_path.rstrip() for current_path in f.readlines()]

    print(file_paths)
    count = 0

    while len(file_paths) != 0:
        file_path = file_paths.pop()

        t = eyed3.load(file_path)
        print(file_path)
        if t is None or t.tag is None or not t.tag.title or not t.tag.artist:
            tag = {'artist': '',
                   'album': '',
                   'title': splitext(basename(file_path))[0],
                   'release_date': '',
                   'filename': splitext(basename(file_path))[0],
                   'path': file_path,
                   'full_text': '{}'.format(splitext(basename(file_path))[0])
                   }
        else:
            tag = {'artist': t.tag.artist,
                   'album': t.tag.album,
                   'title': t.tag.title,
                   'release_date': t.tag.release_date,
                   'filename': splitext(basename(file_path))[0],
                   'path': file_path,
                   'full_text': '{} {} {}'.format(t.tag.artist, t.tag.album, t.tag.title)
                   }
        songs = songs.append(tag, ignore_index=True)
        count += 1
        if count % 10 == 0:
            songs.to_csv('songs.csv', mode='a', header=False, index=False)
            songs = pd.DataFrame(columns=["artist", "album", "title", "release_date", "filename", "path", "full_text"])
            with open("file_paths.txt", "w") as f:
                f.writelines("%s\n" % f_p for f_p in file_paths)
            logging.info("Remaining {}".format(len(file_paths)))

    songs.to_csv('songs.csv', mode='a', header=False, index=False)

    songs = pd.read_csv("songs.csv",
                        names=["artist", "album", "title", "release_date", "filename", "path", "full_text"])

    songs.to_csv('songs_final.csv', index=False)
    os.remove("songs.csv")
    os.remove("file_paths.txt")
    logging.info("\nThat's it! Done!\n Now restart the application and you are ready to go!")
