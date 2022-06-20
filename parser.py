import logging

def fetch_title(response:dict):
    result = ""
    try:
        result = response["track"]["title"]
    except (KeyError, TypeError) as e:
        logging.error("No title found")
    return result

def fetch_artist(response:dict):
     result = ""
     try:
        result = response["track"]["subtitle"]
     except (KeyError, TypeError) as e:
         logging.error("No artist found")
     return result

def fetch_cover_art_url(response:dict):
    result = ""
    try:
        result = response["track"]["images"]["coverart"]
    except (KeyError, TypeError) as e:
        logging.error("No cover art url found")
    return result

def fetch_album(response:dict):
    result = ""
    try:
        result = response["track"]["sections"][0]["metadata"][0]["text"]
    except (KeyError, TypeError,IndexError) as e:
         logging.error("No album name found")
    return result

