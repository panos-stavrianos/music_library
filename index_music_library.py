import logging
import os
from os.path import basename, splitext

import eyed3
import pandas as pd


def index_music_library():
    library_path = os.getenv('MUSIC_LIBRARY_PATHS', "")
    if library_path == "":
        exit(0)
    logging.basicConfig(filename='index_music_library.log', filemode='w', level="INFO",
                        format='%(message)s')

    songs = pd.DataFrame()

    logging.info("Start Indexing")
    eyed3.log.setLevel("ERROR")
    log_file = os.path.abspath("index_music_library.log")
    os.system('gnome-terminal -- tail -F "{}"'.format(log_file))

    for root, dirs, files in os.walk(library_path):
        print(root)
        logging.info("Indexing->" + root)

        for file in files:
            try:
                if file.find(".mp3") < 0:
                    continue
                file_path = os.path.abspath(os.path.join(root, file))
                t = eyed3.load(file_path)
                if not t.tag.title or not t.tag.artist:
                    continue
                tag = {'artist': t.tag.artist,
                       'album': t.tag.album,
                       'title': t.tag.title,
                       'release_date': t.tag.release_date,
                       'filename': splitext(basename(file_path))[0],
                       'path': file_path,
                       'full_text': '{} {} {}'.format(t.tag.artist, t.tag.album, t.tag.title)
                       }
                print(tag)
                songs = songs.append(tag, ignore_index=True)

            except Exception as e:
                logging.error(e)
                continue

    songs.to_csv("songs.csv", index=False)

    logging.info("\nThat's it! Done!\n Now restart the application and you are ready to go!")
