# TODO:
# Setup args for the cmd program
# DFS for all song files and their relative paths in a concurrent queue
# Divide the job and let them be processed by multiple concurrent entities.
# Testing


import json
import random
import sys
import asyncio
from time import sleep
from shazamio import Shazam
from parser import fetch_album, fetch_artist, fetch_cover_art_url, fetch_title
from audio_meta_data import AudioMetaData
from traverse import traverse
from convert import convert_to_specific_format
import logging
import util


def main() -> int:
    # TODO : read args and act accordingly
    logging.basicConfig(filename="meta-data-organiser.log")
    logging.root.setLevel(logging.NOTSET)
    logging.getLogger().addHandler(logging.StreamHandler())

    queue = traverse()
    asyncio.run(process(queue))
    return 0


async def process(queue, args=None):

    shazam = Shazam()
    logging.debug(queue)

    while queue:
        current_music_file_path = queue.get()
        result = await shazam.recognize_song(current_music_file_path)
        logging.debug(json.dumps(result))

        # TODO: Standardise formats if requested
        # TODO: Parse args
        # format = "mp3"
        # convert_to_specific_format(current_music_file_path,format=format)

        sleep(random.uniform(0.1, 2))


        audio_meta_data = AudioMetaData(current_music_file_path)

        cover_art_image_url = fetch_cover_art_url(result)
        title = fetch_title(result)
        artist = fetch_artist(result)
        album = fetch_album(result)

        audio_meta_data.set_title(title) \
                       .set_album(album)  \
                       .set_artist(artist) \
                       .set_cover_art_url(cover_art_image_url)
       
        audio_meta_data.save()

        util.rename_file_name(current_music_file_path,title)


if __name__ == '__main__':
    sys.exit(main())
