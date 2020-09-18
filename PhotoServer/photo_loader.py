from . import local_picture_loader

from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, JsonResponse


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



def getPicture(request):
    return local_picture_loader.getLocalPicture()
    
    try:
        return local_picture_loader.getLocalPicture()
    except:
        print("Failed to getLocalPicture")
        raise 

    try:
        print("trying unsplash")
        return get_unsplash_image();
    except:
        print("Failed to get_unsplash_image")
        pass


    
    return empty_dummy_image()

