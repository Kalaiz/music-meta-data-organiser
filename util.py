import mimetypes
import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.mp4 import MP4 

SUPPORTED_AUDIO_EXTENSIONS = ["mp3","m4a","wav"]
ID3_SUPPORTED_AUDIO_EXTENSION = ["mp3","wav"]
assert len(SUPPORTED_AUDIO_EXTENSIONS) == len(set(SUPPORTED_AUDIO_EXTENSIONS).union(set(ID3_SUPPORTED_AUDIO_EXTENSION)))

ID3_EASY_SUPPORTED_META_TAGS = {"title":"title","artist":"artist","album":"album"}
ID3_SUPPORTED_META_TAGS = {"cover-art":"APIC"}
M4A_SUPPORTED_META_TAGS = {"title":"\xa9nam","artist":"\xa9ART","album":"\xa9alb","cover-art":"covr"}

def guess_mime_type(url:str):
    mime_type = mimetypes.guess_type(url)
    if mime_type:
        return mime_type[0]
    else:
        return None

def get_extension(file_path:str):
    return file_path.split(".")[-1]
   
def get_meta_tag(file_path:str,extension:str,easy=True):
    if extension in ID3_SUPPORTED_AUDIO_EXTENSION:
        if easy:
            return EasyID3(file_path)
        else:
            return ID3(file_path)
    elif extension == "m4a":
        return MP4(file_path)
    else:
        return None

def create_meta_tag(file_path:str,extension:str):
    if extension in ID3_SUPPORTED_AUDIO_EXTENSION:
        id3_tag = ID3()
        id3_tag.save(file_path)


def get_new_file_path(old_file_path:str,new_file_name:str)->str:
    """ Given an absolute path of a file and a new file name, 
    returns an absolute path to the new file name replacing the new one."""
    base_path,file_name = os.path.split(old_file_path)
    file_extension = get_extension(file_name)
    new_file_name_with_extension = new_file_name + '.' + file_extension
    return os.path.join(base_path,new_file_name_with_extension)


def rename_file_name(old_file_path:str,new_file_name:str):
    new_file_path = get_new_file_path(old_file_path,new_file_name)
    os.rename(old_file_path,new_file_path)

        