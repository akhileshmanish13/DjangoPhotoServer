## Running it once it is setup
-------------------------------
```console
pipenv run ./start.sh
```

Which runs:
```console
pipenv shell python manage.py runserver 0.0.0.0:8000
pipenv shell python manage.py process_tasks
```


## Setting up pipenv
---------------------
```console
$ export PIPENV_VENV_IN_PROJECT="enabled"
```

```console
$ python3 -m pipenv install --python 3.8; #If you need to install python3.8
$ python3 -m pipenv shell;
% pipenv install; 
% python manage.py runserver
```


or 

```console
$ python3 -m pip install pipenv
$ python3 -m pipenv shell
$ pipenv install django
```

or  

Oneline: 
```console
$ export PIPENV_VENV_IN_PROJECT="enabled"; python3 -m pip install pipenv; python3 -m pipenv install --python 3.8;python3 -m pipenv shell; pipenv install; python manage.py runserver

$ export PIPENV_VENV_IN_PROJECT="enabled"; python3 -m pip install pipenv; python3 -m pipenv shell; pipenv install; python manage.py runserver

```


## Initial setup
----------------
Run db migrations

```console
% python manage.py makemigrations PhotoServer
% python manage.py showmigrations
% python manage.py migrate

```

And copy the env file. (adjust contentsas needed)

```console
$ cp .env_example .env
```
* * * 


## Initally setting up django .venv:
-------------------------------------

Run this so the venv in the same folder as the code
```console
$ export PIPENV_VENV_IN_PROJECT="enabled"
```

<https://stackoverflow.com/questions/52540121/make-pipenv-create-the-virtualenv-in-the-same-folder> 

```console
$ python3 -m pip install pipenv
$ python3 -m pipenv shell
$ pipenv install django
```

From <https://hackersandslackers.com/getting-started-django/> 

Then can run:
 
 ```console
 % python -m django --version
 % django-admin startproject PhotoServer
 % cd PhotoServer
 % python manage.py runserver
 ```

Will also need to run migrations:

## Running migrations for the DB:
---------------------------------
```console

% python manage.py makemigrations PhotoServer
% python manage.py showmigrations
% python manage.py migrate

```

For background-taks info see:
https://django-background-tasks.readthedocs.io/en/latest/


## Helpful SQL 
---------------------------------
```sql
sqlite3 db.sqlite3 'select priority,run_at,repeat,repeat_until,queue,attempts,failed_at,locked_at from background_task;'
```
```sql
sqlite3 db.sqlite3 'select id,number_of_times_read,date_added from PhotoServer_cachedphoto;'
sqlite3 db.sqlite3 'select * from PhotoServer_cachedphoto;'
```
```sql
delete from PhotoServer_cachedphoto where 1;
```


## Raspberry PI
----------------

To acess the hard-drive it sometimes requires that you be logged in as root otherwise you will get permission errors while the server is running.

Most of the pictures are accessible by root though so you can log into the pi and run:
```console
- sudo su root
```

From there just start the server and it should run fine without permission errors. Hacky workaround found here: https://askubuntu.com/a/489761

To get it to just boot on launch, can setup ```/etc/rc.local```
Follow the instructions in ```sample_rc.local``` in this repo.
