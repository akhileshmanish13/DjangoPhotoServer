from . import local_picture_loader
from . import local_cache_file_handler
from .models import CachedPhoto
import os
from background_task import background
from background_task.models import Task

cache_size = os.environ.get('cache_size', 20)
# print(f">>>>>>>>>>>>> {cache_size} <<<<<<<<<<<<<<<<")
background_task_verbose_name="Update Cache"

def cacheAlreadySetToUpdate():
    return Task.objects.filter(verbose_name=background_task_verbose_name).exists()


def cacheNeedsUpdate():
    if(cacheAlreadySetToUpdate()):
        print("----------- Cache AlreadySetToUpdate ----------------")
        return False;

    fresh_photo_count = CachedPhoto.objects.all().filter(number_of_times_read=0).count()

    cache_refresh_size = cache_size /2 #if cache_size is small then 5 will mean it always resets.
    print(f"Does cacheNeedsUpdate?: fresh-photos={fresh_photo_count} cache_size={cache_size} cache_refresh_size={cache_refresh_size}")

    if (fresh_photo_count <= cache_refresh_size):
        print(f"cacheNeedsUpdate: fresh-photos={fresh_photo_count} cache_size={cache_size}", )
        return True

    return False;


def delete_old_values():
    photos_to_delete = CachedPhoto.objects.all().filter(number_of_times_read__gte=1)

    for cached_photo in photos_to_delete:
        local_cache_file_handler.deleteImageIfInLocalDirectory(cached_photo.cache_file_url)

    photos_to_delete.delete();

@background()
def save_image_url_to_cache_if_unique(image_url):

    assumed_new_url = local_cache_file_handler.get_local_photo_cache_url_for(image_url)

    #Check if it already exists and abort.
    if( CachedPhoto.objects.all().filter(cache_file_url=assumed_new_url).exists() ):
        print(f'Already cached {image_url} at {assumed_new_url}.')
        return;

    # Doesn't exist so copy it and save.
    new_local_image_url = local_cache_file_handler.copyImageToLocalDirectory(image_url)
    if(new_local_image_url):
        CachedPhoto.objects.create(cache_file_url=new_local_image_url)
    
    print(f"Saved {image_url} to cache as {new_local_image_url}.");



def add_new_pictures_to_cache(number_to_add):

    for i in range(number_to_add):
        original_image_url = local_picture_loader.getRandomLocalPictureURL();

        save_image_url_to_cache_if_unique(original_image_url)

    # CachedPhoto.objects.bulk_create(new_cache_objects) #Don't use bulk insert in case something fails above.
    print('finished finding new pictures to cache')

@background()
def updateCache():
    add_new_pictures_to_cache(cache_size)
    delete_old_values()
    print('finished updating cache')


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
