
from queue import Queue
import os
from util import SUPPORTED_AUDIO_EXTENSIONS 


def traverse(path=None) -> Queue:
    if not path:
        path  = os.getcwd()

    if  not os.path.isdir(path):
        # TODO: Error handling
        pass
 

    queue = Queue()
    for root, _, files in os.walk(path):
        for file in files:
            if file.split(".")[-1] in SUPPORTED_AUDIO_EXTENSIONS:
                queue.put(root+'/'+file)
        
    return queue