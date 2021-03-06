from __future__ import annotations
import logging
from util import ID3_EASY_SUPPORTED_META_TAGS, ID3_SUPPORTED_AUDIO_EXTENSION, ID3_SUPPORTED_META_TAGS, M4A_SUPPORTED_META_TAGS, create_meta_tag, get_extension, get_meta_tag, guess_mime_type
from mutagen.id3 import APIC
from mutagen.mp4 import MP4Cover
from urllib.request import urlopen

class AudioMetaData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.extension = get_extension(file_path)
        try:
            self.meta_tag = get_meta_tag(file_path=file_path,extension=self.extension,easy=False)
        except:
            logging.info("No meta tag exists. Creating one now...")
            logging.debug(self)
            create_meta_tag(file_path=file_path,extension=self.extension)
            self.meta_tag = get_meta_tag(file_path=file_path,extension=self.extension,easy=False)

        self.is_id3_supported = self.extension in ID3_SUPPORTED_AUDIO_EXTENSION
        if self.is_id3_supported:
            self.simple_meta_tag = get_meta_tag(file_path=file_path,extension=self.extension,easy=True)
    
    def set_title(self,title)->AudioMetaData:
        if title:
            self.title = title
            self._set_attribute("title",self.extension,title)
        return self

    def set_artist(self,artist)->AudioMetaData:
        if artist:
            self.artist = artist
            self._set_attribute("artist",self.extension,artist)
        return self

    def set_album(self,album)->AudioMetaData:
        if album:
            self.album = album
            self._set_attribute("album",self.extension,album)
        return self

    def set_cover_art_url(self,cover_art_url)->AudioMetaData:
        if cover_art_url:
            self.cover_art_url = cover_art_url
            self._set_attribute("cover-art",self.extension,cover_art_url)
        return self


    def _get_meta_tag_attribute_name(self,attribute_name,extension):
        if extension in ID3_SUPPORTED_AUDIO_EXTENSION:
            id3_easy_supported_attributes = set(ID3_EASY_SUPPORTED_META_TAGS.keys())
            id3_supported_attributes = set(ID3_SUPPORTED_META_TAGS.keys())
            assert attribute_name in id3_supported_attributes.union(id3_easy_supported_attributes), "Attribute name not found"
            if attribute_name in id3_easy_supported_attributes:
                return self.simple_meta_tag,ID3_EASY_SUPPORTED_META_TAGS[attribute_name]
            elif attribute_name in id3_supported_attributes:
                return self.meta_tag,ID3_SUPPORTED_META_TAGS[attribute_name]
        elif extension == "m4a":
            if attribute_name in M4A_SUPPORTED_META_TAGS:
                return self.meta_tag,M4A_SUPPORTED_META_TAGS[attribute_name]
        
        assert False, "There is no implementation for file format " + extension


            
    def _set_attribute(self,attribute_name,extension,value):
        meta_tag,actual_attribute_name = self._get_meta_tag_attribute_name(attribute_name,extension)
        if attribute_name == "cover-art":
            self._set_cover_art(extension,actual_attribute_name,meta_tag,value)
        else:
            meta_tag[actual_attribute_name] = value
            

    def _set_cover_art(self,extension,actual_attribute_value,meta_tag,url):
        cover_art_mime_type = guess_mime_type(url)
        logging.debug("set_cover_art "+ cover_art_mime_type)
        image_type = get_extension(url)
        if cover_art_mime_type:
            cover_art = urlopen(url)
            if extension in ID3_SUPPORTED_AUDIO_EXTENSION:
                meta_tag.add(APIC(
                                encoding=3,
                                mime=cover_art_mime_type,
                                type=3,
                                desc=u"Cover",
                                data=cover_art.read()
                                ))
            elif extension == "m4a":
                image_format = None
                if image_type == "png":
                    image_format = MP4Cover.FORMAT_PNG
                elif image_type == "jpeg" or image_type == "jpg":
                    image_format = MP4Cover.FORMAT_JPEG
                else:
                    logging.error("Image format not suitable; Skipping it....")
                    return 
                meta_tag[actual_attribute_value] =  [MP4Cover(cover_art.read(), imageformat=image_format)]

    def remove_cover_art(self):
        if self.is_id3_supported:
            self.meta_tag.delall("APIC")
        elif self.extension == "m4a":
            _, cover_art_attribute = self._get_meta_tag_attribute_name("cover-art",self.extension)
            self.meta_tag[cover_art_attribute] = []
        return self

    def save(self):   
        self.meta_tag.save()
        if self.is_id3_supported:
            self.simple_meta_tag.save()
       
     
