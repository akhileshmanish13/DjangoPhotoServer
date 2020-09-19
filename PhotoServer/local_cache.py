from . import local_picture_loader
from .models import CachedPhoto

cache_size =  20
minimum_cache_size = cache_size/2

# minimum_cache_size = 5
# minimum_cache_size = min(cache_size/2, minimum_cache_size)

def cacheNeedsUpdate():
    # Select count() from DB where number_of_times_read = 0
    fresh_photos = CachedPhoto.objects.all().filter(number_of_times_read=0)
    
    fresh_photo_count = len(fresh_photos)
    if (fresh_photo_count <= minimum_cache_size):
        print(f"cacheNeedsUpdate: fresh-photos={fresh_photo_count} minimum_cache_size={minimum_cache_size} cache_size={cache_size}", )
        return True
    
    return False;


def delete_old_values():
    photos_to_delete = CachedPhoto.objects.all().filter(to_delete=True)
    photos_to_delete_count = len(photos_to_delete);
    print(f"{photos_to_delete_count} photos to delete.")
    photos_to_delete.delete()


def mark_read_pictures_for_deletion():
    photos_to_mark_for_deletion = CachedPhoto.objects.all().filter(number_of_times_read__gte=1)
    print(f"{len(photos_to_mark_for_deletion)} photos marked for deletion.")
    photos_to_mark_for_deletion.update(to_delete=True)


def add_new_pictures_to_cache(number_to_add):
    new_cache_objects = []
    for i in range(number_to_add):
        image_url = local_picture_loader.getRandomLocalPictureURL();
        print(image_url)

        new_image = CachedPhoto(cache_file_url=image_url)
        new_cache_objects.append(new_image)


    CachedPhoto.objects.bulk_create(new_cache_objects)

    return True




def updateCache():
    delete_old_values()
    mark_read_pictures_for_deletion()
    add_new_pictures_to_cache(cache_size)

    

# https://django-background-tasks.readthedocs.io/en/latest/
# maybe can extend this with background task. 
def updateIfNeeded():
    if(cacheNeedsUpdate()):
        updateCache()
    else:
        print("Cache doesn't need update")


def getNewValue():
    updateIfNeeded()
    
    # toDelete asc -- ideally ones that are fresh.
    # number_of_times_read
    # date_added asc

    #Should put ones that aren't marked for deletion first (but if they're all marked for delete it still returns something).
    cache_val = CachedPhoto.objects.order_by('to_delete','number_of_times_read', 'date_added')[0]
    print("---------   Cache Object   ------------")
    print(cache_val.cached_image)
    print(cache_val.cache_file_url)
    print(cache_val.number_of_times_read)
    print(cache_val.date_added)
    print(cache_val.to_delete)
    
    
    response = local_picture_loader.httpResponsePicturFromLocalUrl(cache_val.cache_file_url)
    
    cache_val.number_of_times_read +=1
    cache_val.save()

    return response
    
    


def bypassCacheAndGetLocalPicture():
    return local_picture_loader.getRandomLocalPicture()