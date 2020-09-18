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

# Works but is very slow. 
def get_random_files_recurse_slow(extensions, folder_url=os.getcwd()):
    
    # Check folder exists.
    if(not os.path.exists(folder_url)):
        error_message = "Sorry, path not found:" + folder_url
        print(error_message)
        raise NameError(error_message);

    folder_tree = recursive_files(extensions, folder_url)

    chosen_image = False
    for n, x in enumerate(folder_tree, 1):
        if random.randrange(n) == 0:
            chosen_image = x
            print("chosen n", n)
    print("n", n)
    
    if(not chosen_image):
        error_message = "No pictures found:" + folder_url
        print(error_message)
        raise NameError(error_message);

    return chosen_image


# Error if it traverses into a directory with no pictures...
# Then it throws an error.
def get_random_files_recurse_quick(extensions, folder_url=os.getcwd()):
    
    # Check if any of the file extensions in this folder?
    # or if there are directories. 
    if(not os.path.exists(folder_url)):
        error_message = "Sorry, path not found:" + folder_url
        print(error_message)
        raise NameError(error_message);

    if( not os.listdir(folder_url)):
        error_message = "Sorry, path empty:" + folder_url
        print(error_message)
        raise NameError(error_message);

    # Can't use this as sub-directories might have files.
    # if(not glob.glob('*.jpeg') ): #Need to extend for all extensions
    #     error_message = "Sorry no extensions found in:" + folder_url
    #     print(error_message)
    #     raise NameError(error_message);



    chosen_file = random.choice(os.listdir(folder_url) )

    new_url = os.path.join(folder_url, chosen_file)

    if os.path.isdir(new_url):
        return get_random_files_recurse_quick(extensions, new_url)

    file_extension = pathlib.Path(new_url).suffix
    print('file_extension', file_extension)

    # Error if it traverses into a directory with no pictures...
    # Will just keep hitting the else statement. 
    if(file_extension in extensions):
        return new_url
    else:
        return get_random_files_recurse_quick(extensions, folder_url)


def get_random_files_recurse(extensions, folder_url=os.getcwd()):
    max_attempts = 10
    for attempt_number in range(max_attempts):
        try:
            image_url = get_random_files_recurse_quick(extensions, folder_url)
            if(image_url):
                return image_url
        except NameError as e:
            if(str(e)[0:22] == "Sorry, path not found:"):
                raise e #If the path isn't found, just quit.

            pass #try again
    
    error_message = f"No image found after {max_attempts} attempts in: {folder_url}"
    print(error_message)
    raise NameError(error_message);



def getLocalPicture():
    random.seed();
    extensions = [".jpeg", ".jpg", ".png"];
    extensions = extensions + list(map(lambda s: s.upper(), extensions))

    print("extensions", extensions)

    root_url = "/Volumes/4TB WD Passport/Photos Library.photoslibrary/originals_/"
    try:
        image_url = get_random_files_recurse(extensions, root_url)
        print("image_url", image_url)

    except NameError:
        root_url = "/Users/tawfiq/Pictures/Empty Folder/"
        print("new root_url", root_url)
        image_url = get_random_files_recurse(extensions, root_url)
    
    print("\nFile found:", image_url)
    print("\n")
    return httpResponsePicturFromLocalUrl(image_url)
