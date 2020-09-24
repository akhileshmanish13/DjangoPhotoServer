from shutil import copy
import os.path
from os import remove


def get_local_photo_directory_and_check_it_exists():
    local_directory = os.environ.get('photo_cache_directory')
    if(not local_directory):
        print("no local photo_cache_directory specified ")
        return False;

    if(not os.path.isdir(local_directory)):
        os.makedirs(local_directory)

    return local_directory

def get_local_photo_cache_url_for(image_url):
    local_directory = get_local_photo_directory_and_check_it_exists();

    if(local_directory and image_url):
        new_file = os.path.basename(image_url)
        new_file = os.path.join(local_directory, new_file)
        return new_file
    
    

def copyImageToLocalDirectory(image_url):
    if(not os.path.isfile(image_url)):
        return False;
    
    local_directory = get_local_photo_directory_and_check_it_exists();
    if(not local_directory):
        return image_url; # Equivalent to not copying it, and just setting cahce to load from remote place.

    # print(f"Local directory {local_directory} and original file {image_url} exists" )
    
    new_local_image_url = copy(image_url,  local_directory);
    # print(f"copied {image_url} to local {new_local_image_url}");
    return new_local_image_url;

    
def deleteImageIfInLocalDirectory(image_url):
    if(not os.path.isfile(image_url)):
        print(f">> Not deleting {image_url}")
        return False;

    local_directory = get_local_photo_directory_and_check_it_exists();
    if(not local_directory):
        print(f">> Not deleting {image_url}")
        return False;

    file_name = os.path.basename(image_url)
    cache_destination = os.path.join(local_directory, file_name)

    if(os.path.isfile(cache_destination)):
        remove(cache_destination)
        print(f'deleted {cache_destination} from cache')
