import os
import os
import sys
import random
import pathlib
import glob

from django.http import HttpResponse

# Slow as it loads the whole tree.
def get_random_files_glob(extensions, root_directory=os.getcwd()):
    file_list = [];
    for ext in extensions:
        file_list = file_list +list(Path(root_directory).glob(f"**/*.{ext}"))

    if not len(file_list):
        return False;
    
    rand = random.randint(0, len(file_list) - 1)
    
    return file_list[rand]


def httpResponsePicturFromLocalUrl(file_url):
    with open(file_url, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


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



# Error if it traverses into a directory with no pictures...
# Might get into an infinite loop.
# C
def get_random_files_recurse_old(extensions, folder_url=os.getcwd()):
    
    # Check if any of the file extensions in this folder?
    # or if there are directories. 
    if(not os.path.exists(folder_url)):
        error_message = "Sorry, path not found:" + folder_url
        print(error_message)
        raise Exception(error_message);

    if(not glob.glob('*.jpeg') ):
        error_message = "Sorry no extensions found in:" + folder_url
        print(error_message)
        raise Exception(error_message);



    file_url = random.choice(os.listdir(folder_url) )

    new_url = os.path.join(folder_url, file_url)

    if os.path.isdir(new_url):
        recured_url = get_random_files_recurse(extensions, new_url)

    file_extension = pathlib.Path(new_url).suffix
    print('file_extension', file_extension)

    # Error if it traverses into a directory with no pictures...
    # Will just keep hitting the else statement. 
    if(file_extension in extensions):
        return new_url
    else:
        return get_random_files_recurse(extensions, folder_url)


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
