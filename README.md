# Cocktail Hunter

Find cocktails you can make based on your inventory.
This is the backend for the web application handling data, etc.

# Local setup

## Prerequisites

Your system should have Python 3.8.x installed before you continue with the local setup.

## Installation

1. Install pipenv: `pip install pipenv`.
2. Install python dependencies by running `pipenv install`, which also creates a virtual env.
3. Create the `.env` file and fill it in using the variables listed below.
4. Run `pipenv shell` to activate a sub shell for the virtual environment created.
5. Run `python manage.py migrate` if there are changes made to the database.

### Environment Variables

Keep the the `SETTING` variable as it is.
Generate a 50 characters long hexademical string to use a secret key.

```
SECRET_KEY=
SETTING=backend.settings.dev
```

## Creating an Admin user

This should be done after running `pipenv shell`.
This will allow you to access the admin page at `https://localhost:8000/admin` to view and edit data.

1. Run `python manage.py createsuperuser`
2. Fill in the info it asks you to (e.g. username, email)

## Running Development server

You'd need to run two shell instances here, one for the Vue frontend and one for the Django backend which provides the API endpoints.

1. Run `pipenv shell` to activate the virtual environment.
2. Run `python manage.py runserver` to start the Django backend.


## Additional Notes

You can exit the virtual environment by simply typing `exit` as you normally would to exit a normal command line since
pipenv starts up a subshell for the environment. This also means that if you have made changes to the environment variables
in `.env`, you will need to restart the subshell.

If you do not need the subshell, you may simply run `pipenv run python manage.py runserver` to start the server instead and it will save you the hassle of needing to restart the subshell for environment variable changes.