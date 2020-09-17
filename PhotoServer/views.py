from django.shortcuts import render


def frontend(request):
    return render(request, 'PhotoServer/client.html')
