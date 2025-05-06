# wildlife-tracker-api
API backend for recording wildlife observations.

## Models
### Herd
A herd is a group of families that travel together.
## Family
A family is a genetically related group of animals.
## Observation
An Observation records the time, location, size, and health of
a family along with any notable family events, such as a birth
or a death.

## Local Installation
### Requirements ###
**Postgres**
You must have a postgres database installed on your local computer.
See config/settings/local for database settings.

**Poetry**
Install the poetry dependency management tool with:

`curl -sSL https://install.python-poetry.org | python3 -`

Add the poetry shell command with:

`poetry self add poetry-plugin-shell`

Start a poetry virtual environment with:

`poetry shell`

**Geospatial Libraries**
 Install geospatial libraries with:

`brew install gdal`

`brew install geos`

## Load Test Data
You can create test data comprised of herds with:

`python manage.py create_herds --species <species> --num_herds <number_of_herds> --state <two_letter_state>`

Allowable species are: antelope, elk, deer, and moose.

## Start the Local Server
From the wildlife-tracker-api directory:
`python manage.py runserver`

## Query Examples
*POST*, *Retrieve*, and *List* endpoints are implemented for the
herd, family, and observation models.

To query for a particular observation by identifier:
`http://127.0.0.1:8000/observations/00258a5f-a7cb-4bad-8105-c43de7e1f78b`

To query for time-ordered observations of a particular family:
`http://127.0.0.1:8000/observations/?family=00e77391-f6b4-442c-8c25-7a3aef684f7a&ordering=-timestamp`

To create a new family, send a POST requests to:
`http://127.0.0.1:8000/families/

{
    "name": "My loving Elk family",
    "herd": "009491c9-a134-44b5-9892-240cebd12972"
}
