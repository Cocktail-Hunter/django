# Cocktail Hunter

Find cocktails you can make based on your inventory.

### Context

People sometimes don't have a wide variety of alcohol in their homes and might not want to go all the way to the store for that one mysterious ingredient.

### This is where this app comes in...

Users will be able to input a list of all the alcohol and ingredients they've got and the app will return all possible cocktails the user can make. By default, it will result with cocktails strictly with the ingredients the user has but it can be toggled off where the app can result with cocktails with 1-2 missing ingredients.

# Long term plans

Users are able to publish their own cocktail recipes that they've discovered or want to share with the community.

# Local setup

## Prerequisites

Your system should have Python 3.8.x installed before you continue with the local setup.

## Installation

Ignore step 5 for now even if Django tells you to do so as there is currently no database set-up.

1. Install pipenv: `pip install pipenv`.
2. Install python dependencies by running `pipenv install`, which also creates a virtual env.
3. Create the `.env` file and fill it in using the variables listed below.
4. Run `pipenv shell` to activate a sub shell for the virtual environment created.
5. Run `python manage.py migrate` if there are changes made to the database.

### Environment Variables

Keep the the `SETTING` variable as it is.

```
SECRET_KEY=
SETTING=backend.settings.dev
```

## Running Development server

You'd need to run two shell instances here, one for the Vue frontend and one for the Django backend which provides the API endpoints.

1. Run `pipenv shell` to activate the virtual environment.
2. Run `python manage.py runserver` to start the Django backend.


## Additional Notes

You can exit the virtual environment by simply typing `exit` as you normally would to exit a normal command line since
pipenv starts up a subshell for the environment. This also means that if you have made changes to the environment variables
in `.env`, you will need to restart the subshell.

If you do not need the subshell, you may simply run `pipenv run python manage.py runserver` to start the server instead and it will save you the hassle of needing to restart the subshell for environment variable changes.