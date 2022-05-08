import mimetypes

def guess_mime_type(url:str):
    mime_type = mimetypes.guess_type(url)
    if mime_type:
        return mime_type[0]
    else:
        return None
