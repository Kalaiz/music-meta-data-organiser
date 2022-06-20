"""Music meta data organiser - Organises the meta data of audio files.
Usage: 
    music_meta_data_organiser (-h | --help)
    music_meta_data_organiser <directory> 
    music_meta_data_organiser <directory> (-s format | --standardise=format)
    music_meta_data_organiser <directory> (rmca | --remove-cover-art)
    music_meta_data_organiser <directory> (ca | --set-cover-art)
    music_meta_data_organiser <directory> (fn | --set-album-name)
    music_meta_data_organiser <directory> (ab | --set-album-name)
    music_meta_data_organiser <directory> (at | --set-artist-name)
    music_meta_data_organiser <directory> [-s format] [fn] [ab] [at] [ca] [rmca]


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
from queue import Queue
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


def main(args:dict) -> int:
    """Example of args: 
        {'--standardise': None,
        '<directory>': '.',
        'ab': False,
        'at': False,
        'ca': False,
        'fn': False,
        'rmca': False}"""
    directory = args.get(util.ARG_DIRECTORY_KEY)
    try:
        queue = traverse(path=directory)
    except NoSuchPath as error:
        print("Invalid path: "+ error.args[0]+ "\nPlease input a valid one.")
        return -1

    logging.basicConfig(filename="meta-data-organiser.log")
    logging.root.setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    asyncio.run(process(queue,args))
    return 0


async def process(queue:Queue, args:dict):

    shazam = Shazam()
    logging.debug("Queue size "+ str(queue.qsize()))
    bar = Bar("Current progress", max=queue.qsize())
    while queue:

        try:
         current_music_file_path = queue.get_nowait()
        except:
          break

        logging.info("\nProcessing "+ current_music_file_path)

        try:
            result = await shazam.recognize_song(current_music_file_path)
        except CouldntDecodeError :
            logging.error("Could not decode " + current_music_file_path + " Skipping it.... ")
        except FileNotFoundError:
            logging.error("File name has been edited during the current operation... Skipping it...")

        logging.debug(json.dumps(result))

        standardisation_format = args.get(util.ARG_STANDARDISE_KEY,None) 
        is_album_needed = args.get(util.ARG_ALBUM_KEY,None)
        is_artist_needed = args.get(util.ARG_ARTIST_KEY,None)
        is_cover_art_needed = args.get(util.ARG_COVER_ART_KEY,None)
        is_file_name_needed = args.get(util.ARG_FILE_NAME_KEY,None)
        is_cover_art_to_be_removed = args.get(util.ARG_REMOVE_COVER_ART_KEY,None)
        current_file_format = util.get_extension(current_music_file_path)

        if standardisation_format and current_file_format != standardisation_format:
            logging.debug("Converting "+ current_music_file_path +" to the format "+ standardisation_format)
            current_music_file_path = convert_to_specific_format(current_music_file_path,format=standardisation_format)
                 

        audio_meta_data = AudioMetaData(current_music_file_path)

        title = fetch_title(result)
        audio_meta_data = audio_meta_data.set_title(title) 

        if is_album_needed:
            album = fetch_album(result)
            audio_meta_data = audio_meta_data.set_album(album)
        
        if is_artist_needed:
            artist = fetch_artist(result)
            audio_meta_data = audio_meta_data.set_artist(artist)

        if is_cover_art_to_be_removed:
            audio_meta_data = audio_meta_data.remove_cover_art()
        
        if is_cover_art_needed:
            cover_art_image_url = fetch_cover_art_url(result)
            logging.debug(cover_art_image_url)
            audio_meta_data = audio_meta_data.set_cover_art_url(cover_art_image_url)

        audio_meta_data.save()

        if is_file_name_needed:
            cleaned_title = util.clean_title(title)
            util.rename_file_name(current_music_file_path,cleaned_title,format=standardisation_format)

        sleep(random.uniform(0.1, 5))

        bar.next()
        logging.info("\n")
        
    
    logging.info("Done!")
    bar.finish()

if __name__ == '__main__':
    args = docopt(__doc__, help=True, version=None, options_first=False)
    standardised_arg = args.get("--standardise") 
    is_valid_format = standardised_arg in util.SUPPORTED_AUDIO_EXTENSIONS
    if (not standardised_arg ) and (not is_valid_format):
        supported_formats = ''.join(["\n-"+str(audio_format) for audio_format in util.SUPPORTED_AUDIO_EXTENSIONS])
        print("Audio format is not supported. Please try using any of these formats: " + supported_formats +'\n')
        sys.exit(-1)
    else:      
        sys.exit(main(args))
