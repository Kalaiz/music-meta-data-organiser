from pydub import AudioSegment
import os 

def convert_to_mp3(path:str):
    extension = path.split('.')[-1]
    music_file = AudioSegment.from_file(path,format=extension)
    music_file.export(path.split(".")[0]+".mp3",format="mp3")
    os.remove(path=path)
    print("Successfully converted mp3 " + path)
