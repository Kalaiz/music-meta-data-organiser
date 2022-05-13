from pydub import AudioSegment
import os
import logging
import util



def convert_to_specific_format(path: str,format="mp3"):
    extension = util.get_extension(path)
    
    try:
     music_file = AudioSegment.from_file(path, format=extension)
    except Exception as e:
        logging.error("No such file as "+ path+ "; Skipping it.....")
        return

    file_name_path = path.split('.')[0]
    file_name_with_extension_path = file_name_path + '.' + format
    file_unique_identifier = 1

    while os.path.exists(file_name_with_extension_path):
        logging.info("File already exist; " + file_name_with_extension_path +
                     "; Appending numericals behind to make it unique.")
        file_name_with_extension_path = util.DUPLICATE_FILE_NAME_TEMPLATE.format(file_name=file_name_path,
                                                                               file_identifier=file_unique_identifier,format=format)

    music_file.export(file_name_with_extension_path, format=format)
    os.remove(path=path)
    logging.info("Successfully converted  " + path)
