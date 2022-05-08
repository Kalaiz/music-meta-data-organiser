# TODO: 
# Setup args for the cmd program
# DFS for all song files and their relative paths in a concurrent queue
# Divide the job and let them be processed by multiple concurrent entities.
# Progress bar for cm
# Provide GUI
# Testing


import json
import random
import os
import sys
import asyncio
from time import sleep
from shazamio import Shazam
from parser import fetch_album, fetch_artist, fetch_cover_art_url, fetch_title
from  traverse import traverse
from convert import  convert_to_specific_format
from mutagen.id3 import ID3,APIC,ID3NoHeaderError
from urllib.request import urlopen
import logging
from mutagen import File
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3
import util



def main() -> int:
    # TODO : read args and act accordingly
    logging.basicConfig(filename="meta-data-organiser.log")
    logging.root.setLevel(logging.NOTSET)
    logging.getLogger().addHandler(logging.StreamHandler())

    queue = traverse()
    asyncio.run(process(queue))
    return 0

async def process(queue,args=None):

    shazam = Shazam()
    temp = 0
    logging.debug(queue)

    while queue:
        current_music_file_path = queue.get()

        result = await shazam.recognize_song(current_music_file_path)
        logging.debug(json.dumps(result))

        # TODO: Standardise formats if requested
        # TODO: Parse args
        # format = "mp3"
        # convert_to_specific_format(current_music_file_path,format=format)


        # TODO: Remove this later
        temp+=1
        sleep(random.uniform(0.1,2))
        if temp == 5:
            break

        try:
         if current_music_file_path.endswith(".m4a"):
            current_music_file_meta_data = MP4(current_music_file_path,easy=True).tags
         else:
            current_music_file_meta_data = EasyID3(current_music_file_path)   
        except ID3NoHeaderError:
            id3_tag = ID3()
            id3_tag.save(current_music_file_path)
            current_music_file_meta_data = EasyID3(current_music_file_path)   
           
        logging.debug(current_music_file_meta_data)
        logging.debug("==============")
        logging.debug(result)
        logging.debug("==============")

        cover_art_image_url = fetch_cover_art_url(result)
        title = fetch_title(result)
        artist = fetch_artist(result)
        album = fetch_album(result)

        current_music_file_meta_data["title"]= title
        current_music_file_meta_data["artist"]= artist
        current_music_file_meta_data["album"]= album
        


        current_music_file_album_meta_data = ID3(current_music_file_path)
        logging.debug(current_music_file_album_meta_data.getall("APIC"))

        cover_art_mime_type = util.guess_mime_type(cover_art_image_url)
        if cover_art_mime_type:
            cover_art = urlopen(cover_art_image_url)
            logging.debug(cover_art_image_url)
            current_music_file_album_meta_data.add(APIC(
                            encoding=3,
                            mime=u'image/jpg',
                            type=3,
                            desc=u'Cover',
                            data=cover_art.read()
                            ))
            current_music_file_album_meta_data.save()
            cover_art.close()

        
        current_music_file_meta_data.save()

        base_path,file_name = os.path.split(current_music_file_path)
        file_extension = file_name.split('.')[-1]
        new_file_name = title + '.' + file_extension
        new_file_path = os.path.join(base_path,new_file_name)
        os.rename(current_music_file_path,new_file_path)
        



if __name__ == '__main__':
    sys.exit(main())
