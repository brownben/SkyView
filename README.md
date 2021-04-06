# SkyView

## Team Project for Glasgow University Web Application Development Course

Created by Ben Brown (@brownben), Chris Abraham (@chris114ab), Eva Kupcova (@kupcis), Kai Lascheit (@KaiLascheit000)

Our site SkyView is for people interested in the solar system, regardless of level of expertise, with information on the planets with a feed of posts on each, there is plenty to see. Users who choose not to login can still benefit by simply browsing the site content and reading, however making an account offers users the ability to interact with posts with likes, comments or even posts of their own. The site’s feed being created by the users allow a community to discuss all the new developments from space exploration to stars and galaxies.

## Instructions

```
# install dependancies
pip install -r requirements.txt

# setup database
py manage.py makemigrations website
py manage.py migrate
py populate_skyview.py

# run
py manage.py runserver

# run tests
py manage.py test
```
