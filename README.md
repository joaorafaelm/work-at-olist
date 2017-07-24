# Work at Olist
[![Build Status](https://travis-ci.org/joaorafaelm/work-at-olist.svg?branch=master)](https://travis-ci.org/joaorafaelm/work-at-olist) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/358e51e3ce08402eb9e906ab74dab7d7)](https://www.codacy.com/app/joaorafaelm/work-at-olist?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joaorafaelm/work-at-olist&amp;utm_campaign=Badge_Grade) [![Requirements Status](https://requires.io/github/joaorafaelm/work-at-olist/requirements.svg?branch=master)](https://requires.io/github/joaorafaelm/work-at-olist/requirements/?branch=master) [![Code Health](https://landscape.io/github/joaorafaelm/work-at-olist/master/landscape.svg?style=flat)](https://landscape.io/github/joaorafaelm/work-at-olist/master)


Hi :smile:

This is my solution for the test proposed [here](https://github.com/olist/work-at-olist).

#### Requirements
* Python 3.6+
* PostgreSQL
* Virtualenv
-------------
#### Environment
This project was developed using Pycharm, Vim and Atom Editor, running on macOS Sierra 10.12.

-------------
#### Getting Set Up
Clone this project and create the virtual environment:
~~~~
$ git clone https://github.com/joaorafaelm/work-at-olist && cd work-at-olist
$ virtualenv -p python3.6 .olistvenv
$ source .olistvenv/bin/activate
~~~~
Set your environment variables in the .env file:
~~~~
$ cp local.env .env
~~~~
Install all dependencies and setup database:
~~~~
$ make update && make migrate
~~~~
Testing. *(Default argument APP=channels)*:
~~~~
$ make test
~~~~
Running the app:
~~~~
$ make run
~~~~
You can now go to [http://localhost:8000](http://localhost:8000).

*Run `make help` to show all commands.*

-------------
#### Deploying
Setup [heroku](https://devcenter.heroku.com/articles/heroku-cli) and run:
~~~~
$ make deploy
~~~~
-------------
#### Importing categories
To import the csv into the system, run:
~~~~
$ python work-at-olist/manage.py importcategories <marketplace_name> <csv_file>
~~~~
-------------
#### API documentation
##### Listing all channels
This endpoint will list all channels registered.
~~~~
GET /api/v1/channel/
~~~~
###### Example response
~~~~
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Amazon",
            "reference": "amazon"
        }
    ]
}
~~~~

##### Detail of a channel
This endpoint will show the details for a specific channel (categories and subcategories).
~~~~
GET /api/v1/channel/{channel_reference}/
~~~~
***Channel_reference** is the identifier for the channel.*
###### Example response
~~~~
{
    "name": "Amazon",
    "reference": "amazon",
    "categories": [
        {
            "reference": "amazon-books",
            "name": "Books",
            "channel": "amazon",
            "parent_reference": null
        },
        {
            "reference": "amazon-books-national-literature",
            "name": "National Literature",
            "channel": "amazon",
            "parent_reference": "amazon-books"
        },
        ...
    ]
}
~~~~

##### Listing all categories
This endpoint will list all categories registered.
~~~~
GET /api/v1/category/
~~~~
###### Example response
~~~~
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "reference": "amazon-books",
            "name": "Books",
            "channel": "amazon",
            "parent_reference": null
        },
        {
            "reference": "amazon-books-national-literature",
            "name": "National Literature",
            "channel": "amazon",
            "parent_reference": "amazon-books"
        },
        ...
    ]
}
~~~~
##### Detail of a category
This endpoint will show the details for a specific category (parent and subcategories).
~~~~
GET /api/v1/category/{category_reference}/
~~~~
***Category_reference** is the identifier for the category.*
###### Example response
~~~~
{
    "reference": "amazon-books-national-literature",
    "name": "National Literature",
    "channel": "amazon",
    "parent": {
        "name": "Books",
        "reference": "amazon-books",
        "parent": null
    },
    "children": [
        {
            "name": "Science Fiction",
            "reference": "amazon-books-national-literature-science-fiction",
            "children": []
        },
        {
            "name": "Fiction Fantastic",
            "reference": "amazon-books-national-literature-fiction-fantastic",
            "children": []
        }
    ]
}
~~~~
