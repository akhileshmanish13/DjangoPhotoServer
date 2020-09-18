import os
import os
import sys
import random
import pathlib
import glob

from django.http import HttpResponse

def httpResponsePicturFromLocalUrl(file_url):
    with open(file_url, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


# https://stackoverflow.com/a/6412902
def recursive_files(extensions, dir):
    for path, _, fnames in os.walk(dir):
        for fname in fnames:
            file_extension = pathlib.Path(fname).suffix
            if(file_extension in extensions):
                yield os.path.join(path, fname)


def get_random_files_recurse(extensions, folder_url=os.getcwd()):
    
    # Check folder exists.
    if(not os.path.exists(folder_url)):
        error_message = "Sorry, path not found:" + folder_url
        print(error_message)
        raise Exception(error_message);

    folder_tree = recursive_files(extensions, folder_url)

    for n, x in enumerate(folder_tree, 1):
        if random.randrange(n) == 0:
            pick = x
    return pick



def getLocalPicture():

    extensions = [".jpeg", ".jpg", ".png"];
    extensions = extensions + list(map(lambda s: s.upper(), extensions))

    print("extensions", extensions)

    root_url = "/Volumes/4TB WD Passport/Photos Library.photoslibrary/originals/"
    try:
        image_url = get_random_files_recurse(extensions, root_url)
        print("image_url", image_url)

    except:
        root_url = "/Users/tawfiq/Pictures/"
        print("new root_url", root_url)
        image_url = get_random_files_recurse(extensions, root_url)
    
    print("\nFile found:", image_url)
    print("\n")
    return httpResponsePicturFromLocalUrl(image_url)
