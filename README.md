# balto-api

## Before you do anything

1. Install python 3.8
2. Install pipenv: `pip install pipenv`
3. Run `pipenv install --dev` in the project folder

## Set up the database

1. Create a blank postgres database called `balto_movies` (will work on automating in the future)
2. Run `pipenv shell`
3. Run `python manage.py db upgrade`

## Run the project

1. Run `pipenv shell`
2. Export an environment variable named `SQLALCHEMY_CONNECTION` with your connection string (will make more secure in the future)
3. Run `python app.py`

## Run with docker

Coming soon

# What's left to be done

1. Add Elasticsearch so that we can actually have a fast and good search (along with accurate server side counts)
2. Add a full test suite
3. Rewrite the janky db layer
4. Add functionality to create new: Cast; Origin; Genre; Director
5. Consolidate Cast and Director and join them to the movie table with a role of sorts (they're the same object and can be the same person)
6. Big one: Clean up the data ingest layer for CSV. There is a lot of junky data in the system and the naive sanitization that I performed was not enough.
7. Set up in docker with WSGI
8. Create a pipeline to deploy everything
9. Better error handling everywhere