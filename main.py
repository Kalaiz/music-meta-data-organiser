# TODO: 
# Setup args for the cmd program
# DFS for all song files and their relative paths in a concurrent queue
# Divide the job and let them be processed by multiple concurrent entities.
# Progress bar for cm
# Provide GUI
# Testing


import random
import sys
import asyncio
from time import sleep
from shazamio import Shazam
from  traverse import traverse
from convert import convert_to_mp3
from mutagen.id3 import ID3,APIC
from urllib.request import urlopen
import logging

def main() -> int:
    # TODO : read args and act accordingly
    # TODO: custom file naming convention
    logging.basicConfig(filename="meta-data-organiser.log",  level=logging.DEBUG)
    queue = traverse()
    asyncio.run(process(queue))
    return 0

async def process(queue,args=None):
    shazam = Shazam()
    temp = 0
    logging.debug(queue)
    print(queue.qsize())
    while queue:
        current_music_file = queue.get()
        # if  ".mp3" not in current_music_file:
        #     convert_to_mp3(current_music_file)

        # TODO : Remove all tags 
        if ".m4a" in current_music_file:
            print(current_music_file)
            result = await shazam.recognize_song(current_music_file)
            print(result)

            temp+=1
            sleep(random.uniform(0.1,2))
            if temp ==5:
                break

        # 
       
        # current_music_file_meta_data = ID3(current_music_file)   
        # print(current_music_file_meta_data)
        # print("==============")
        # print(result)
        # print("==============")

        # cover_art_image_url = ""
        # title = ""
        # artist = ""
        # album = ""
        # current_music_file_meta_data["title"]= title
        # current_music_file_meta_data["artist"]= artist
        # current_music_file_meta_data["album"]= album
        # cover_art = urlopen(cover_art_image_url)

        # current_music_file_meta_data['APIC'] = APIC(
        #                 encoding=3,
        #                 mime='image/jpeg',
        #                 type=3,
        #                 desc=u'Cover',
        #                 data=cover_art.read()
        #                 )

        # cover_art.close()
        # current_music_file_meta_data.save()



if __name__ == '__main__':
    sys.exit(main())
