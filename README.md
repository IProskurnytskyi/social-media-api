# Social Media API 

Social Media API system for creating profiles, posts, hashtags and following users written on DRF.


## Installing using GitHub

Python3 must be already installed

```shell
git clone https://github.com/IProskurnytskyi/social-media-api
cd social_media_api
git checkout -b develop
python -m venv venv
if macOS: source venv/bin/activate
if Windows: venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
if you want to run periodic tasks run these commands in separate terminals
and login into admin panel to crete periodic task:
brew services start redis
celery -A social_media_api worker -l INFO
celery -A social_media_api beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Getting access
* create user via /api/users/register
* get access token via /api/users/token
* look for documentation via /api/doc/swagger
* admin panel via /admin
* logout via /api/users/logout
* view users that you are following via /api/users/me/followings
* view users that following you via /api/users/me/followers

## Following
You can follow users using this format: {"users": [2,3,4,5]}

## Features
* Managing profiles and posts
* Logout and invalidate your token
* Pages for viewing followers and followings
* Filtering names and ids
* JWT Authentication
* New permission classes
* Using email instead of username
* Throttling
* API documentation

# Contributing

If you'd like to contribute, please fork the repository and use a develop branch. 
Pull requests are warmly welcome.
