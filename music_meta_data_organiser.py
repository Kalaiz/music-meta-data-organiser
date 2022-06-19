"""Music meta data organiser - Organises the meta data of audio files.
Usage: music_meta_data_organiser <directory> [-s format] [rmca] [ca] [fn] [ab] [at] 

Options:
    -s format --standardise=format  Standardises the format of the audio files. # Note: Do not append '.' in front of the format.      
    -rmca     --remove-cover-art    Removes cover art.
    -ca       --set-cover-art       Applies relevant cover art to the file.
    -fn       --set-file-name       Applies relevant file name to the file.
    -ab       --set-album-name      Applies relevent album name to the file.
    -at       --set-artist-name     Applies relevent artist name to the file.
    -h        --help                Shows this guide.
"""

import json
import random
import sys
import asyncio
from time import sleep
from shazamio import Shazam
from parser import fetch_album, fetch_artist, fetch_cover_art_url, fetch_title
from audio_meta_data import AudioMetaData
from custom_exception import NoSuchPath
from traverse import traverse
from convert import convert_to_specific_format
import logging
import util
from progress.bar import Bar
from pydub.exceptions import CouldntDecodeError
from docopt import docopt


def main(directory,standardisation_format) -> int:
    try:
        queue = traverse(path=directory)
    except NoSuchPath as error:
        print("Invalid path: "+ error.args[0]+ "\nPlease input a valid one.")
        return
    logging.basicConfig(filename="meta-data-organiser.log")
    logging.root.setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    asyncio.run(process(queue,standardisation_format))
    return 0


async def process(queue, standardisation_format):

    shazam = Shazam()

    bar = Bar("Current progress", max=queue.qsize())
    while queue:
        current_music_file_path = queue.get()

        logging.info("\nProcessing "+ current_music_file_path)

        try:
            result = await shazam.recognize_song(current_music_file_path)
        except CouldntDecodeError :
            logging.error("Could not decode " + current_music_file_path + " Skipping it.... ")
        except FileNotFoundError:
            logging.error("File name has been edited during the current operation... Skipping it...")

        logging.debug(json.dumps(result))

        if standardisation_format:
                convert_to_specific_format(current_music_file_path,format=standardisation_format)

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
    args = docopt(__doc__, help=True, version=None, options_first=False)
    directory_arg = args.get("<directory>")
    standardised_arg = args.get("--standardise") 
    is_valid_format = standardised_arg in util.SUPPORTED_AUDIO_EXTENSIONS
    if (standardised_arg != None) and (not is_valid_format):
        supported_formats = ''.join(["\n-"+str(audio_format) for audio_format in util.SUPPORTED_AUDIO_EXTENSIONS])
        print("Audio format is not supported. Please try using any of these formats: " + supported_formats +'\n')
        sys.exit()
    else:      
        print(args)
        # sys.exit(main(directory_arg,standardised_arg))
