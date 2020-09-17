from django.shortcuts import render
from os import path

from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, JsonResponse
from django.utils.dateformat import format

from django.core import serializers
from PIL import Image
import requests


def get_unsplash_image():
    unsplash_url = 'https://source.unsplash.com/random/800x600'
    r = requests.get(unsplash_url, allow_redirects=True)
    return HttpResponse(r, content_type="image/jpeg")


def getPicture(request):
    return get_unsplash_image()

    # try:
    #     with open("file_url, "rb") as f:
    #         return HttpResponse(f.read(), content_type="image/jpeg")
    # except IOError:
    #     red = Image.new('RGB', (1, 1), (255,0,0))
    #     response = HttpResponse(content_type="image/jpeg")
    #     red.save(response, "JPEG")
    #     return response
