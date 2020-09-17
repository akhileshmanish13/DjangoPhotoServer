from django.shortcuts import render
from os import path, listdir
import os, random
import pathlib 


from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, JsonResponse
from django.utils.dateformat import format

from django.core import serializers
from PIL import Image
import requests


def empty_dummy_image():
    red = Image.new('RGB', (1, 1), (255,0,0))
    response = HttpResponse(content_type="image/jpeg")
    red.save(response, "JPEG")
    return response


def get_unsplash_image():
    unsplash_url = 'https://source.unsplash.com/random/800x600'
    r = requests.get(unsplash_url, allow_redirects=True)
    return HttpResponse(r, content_type="image/jpeg")


# Slow as it loads the whole tree.
def get_random_files_glob(extensions, root_directory=os.getcwd()):
    file_list = [];
    for ext in extensions:
        file_list = file_list +list(Path(root_directory).glob(f"**/*.{ext}"))

    if not len(file_list):
        return False;
    
    rand = random.randint(0, len(file_list) - 1)
    
    return file_list[rand]


def returnPicturFromLocalUrl(file_url):
    with open(file_url, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


def get_random_files_recurse(extensions, folder_url=os.getcwd()):
    file_url = random.choice(os.listdir(folder_url) )

    new_url = os.path.join(folder_url, file_url)

    if os.path.isdir(new_url):
        return get_random_files_recurse(extensions, new_url)
    
    file_extension = pathlib.Path(new_url).suffix
    print('file_extension', file_extension)

    if(file_extension in extensions):
        return new_url
    else:
        return get_random_files_recurse(extensions, folder_url)


def getLocalPicture():

    extensions = [".jpeg", ".jpg", ".png"];
    root_url = "/Volumes/4TB WD Passport/Photos Library.photoslibrary/originals/"
    try:
        image_url = get_random_files_recurse(extensions, root_url)
        
    except e:
        root_url = "/Users/tawfiq/Pictures/"
        image_url = get_random_files_recurse(extensions, root_url)
    
    
    # return HttpResponse(image_url)
    return returnPicturFromLocalUrl(image_url)


def getPicture(request):

    try:
        return getLocalPicture()
    except:
        print("Failed to getLocalPicture")
        pass

    try:
        return get_unsplash_image();
    except:
        print("Failed to get_unsplash_image")
        pass


    
    return empty_dummy_image()

