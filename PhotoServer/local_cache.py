from . import local_picture_loader
from .models import CachedPhoto
import os
from background_task import background
from background_task.models import Task

cache_size =  20
background_task_verbose_name="Update Cache"

def cacheAlreadySetToUpdate():
    return Task.objects.filter(verbose_name=background_task_verbose_name).exists()


def cacheNeedsUpdate():
    if(cacheAlreadySetToUpdate()):
        print("----------- Cache AlreadySetToUpdate ----------------")
        return False;

    fresh_photo_count = CachedPhoto.objects.all().filter(number_of_times_read=0).count()

    cache_refresh_size = cache_size /2 #if cache_size is small then 5 will mean it always resets.
    print(f"cacheNeedsUpdate?: fresh-photos={fresh_photo_count} cache_size={cache_size} cache_refresh_size={cache_refresh_size}")

    if (fresh_photo_count <= cache_refresh_size):
        print(f"cacheNeedsUpdate: fresh-photos={fresh_photo_count} cache_size={cache_size}", )
        return True
    
    return False;


def delete_old_values():
    CachedPhoto.objects.all().filter(number_of_times_read__gte=1).delete();
    

def add_new_pictures_to_cache(number_to_add):
    new_cache_objects = []
    for i in range(number_to_add):
        image_url = local_picture_loader.getRandomLocalPictureURL();
        print(image_url)

        new_image = CachedPhoto(cache_file_url=image_url)
        new_image.save() # This way if it fails on another attempt, some of the images still save
        # new_cache_objects.append(new_image)

    # CachedPhoto.objects.bulk_create(new_cache_objects)
    print('finished adding new pictures to cache')

@background()
def updateCache():
    add_new_pictures_to_cache(cache_size)
    delete_old_values()
    print('finished updating cache')
    

# https://django-background-tasks.readthedocs.io/en/latest/
# maybe can extend this with background task. 
def updateIfNeeded():
    if(cacheNeedsUpdate()):
        updateCache(verbose_name=background_task_verbose_name)

def urlExists(file_url):
    if(not os.path.exists(file_url)):
        error_message = "Sorry, path not found:" + file_url
        print(error_message)
        return False
    return True


def getNewCacheValue():
    updateIfNeeded()
    

    #Should put ones that aren't marked for deletion first (but if they're all marked for delete it still returns something).
    cache_val = CachedPhoto.objects.order_by('number_of_times_read', 'date_added').first()
    # print("---------   Cache Object   ------------")
    # print(cache_val.cached_image)
    # print(cache_val.cache_file_url)
    # print(cache_val.number_of_times_read)
    # print(cache_val.date_added)
    
    # Nothing in the DB
    if(not cache_val):
        error_message = "Sorry, no cached objects in db."
        print(error_message)
        raise Exception(error_message);

    return cache_val
    
    
    
def getNewPicture():
    
    # toDelete asc -- ideally ones that are fresh.
    # number_of_times_read
    # date_added asc
    file_url = False

    while(not file_url):
        cache_val = getNewCacheValue();

        if(cache_val and cache_val.cache_file_url and urlExists(cache_val.cache_file_url)):
            file_url = cache_val.cache_file_url; #and ends the while loop
        else:
            error_message = f"File URL not found deleting record.";

            if(cache_val and cache_val.cache_file_url):
                error_message += cache_val.cache_file_url
            cache_val.delete()

            print(error_message)
            


    print(f"Responding with: {file_url}")
    cache_val.number_of_times_read +=1
    cache_val.save()

    response = local_picture_loader.httpResponsePicturFromLocalUrl(file_url)    
    return response


def bypassCacheAndGetLocalPicture():
    return local_picture_loader.getRandomLocalPicture()