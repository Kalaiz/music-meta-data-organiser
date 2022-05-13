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
from progress.bar import Bar
from pydub.exceptions import CouldntDecodeError


def main() -> int:
    # TODO : read args and act accordingly
    logging.basicConfig(filename="meta-data-organiser.log")
    logging.root.setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    queue = traverse()
    asyncio.run(process(queue))
    return 0


async def process(queue, args=None):

    shazam = Shazam()

    bar = Bar("Current progress", max=queue.qsize())
    while queue:
        current_music_file_path = queue.get()

        logging.info("\nProcessing "+ current_music_file_path)

        try:
            result = await shazam.recognize_song(current_music_file_path)
        except CouldntDecodeError :
            logging.error("Could not decode "+ current_music_file_path+" Skipping it.... ")
        logging.debug(json.dumps(result))

        # TODO: Standardise formats if requested
        # TODO: Parse args
        # format = "mp3"
        # convert_to_specific_format(current_music_file_path,format=format)



        audio_meta_data = AudioMetaData(current_music_file_path)

        cover_art_image_url = fetch_cover_art_url(result)
        title = fetch_title(result)
        artist = fetch_artist(result)
        album = fetch_album(result)

        audio_meta_data = audio_meta_data.set_title(title) \
                       .set_album(album)  \
                       .set_artist(artist) \
                       .remove_cover_art()
                    #    .set_cover_art_url(cover_art_image_url)
       
        audio_meta_data.save()

        cleaned_title = util.clean_title(title)
        util.rename_file_name(current_music_file_path,cleaned_title)
        sleep(random.uniform(0.1, 5))

        bar.next()
        logging.info("\n")
        


    bar.finish()
if __name__ == '__main__':
    sys.exit(main())
