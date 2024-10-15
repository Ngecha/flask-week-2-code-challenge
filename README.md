# flask-week-2-code-challenge

# Late Show

For this assignment we were working on an RESTful API for tracking guests and their appearances on episodes.

## Usage

To use this API

1. Fork and clone this repository.
2. Run

```
$ pinenv install && pipenv shell
```

This installs the dependencies and launches the virtual environment.

3. Run

```
$ cd app
$ python3 app.py
```

This launches the local host server. You can use POSTMAN or any other platform to view, edit and view the superheroes

## Models

The Flask application has 3 models which inherit from:

```
(db.model , SerializerMixin)
```

1. Episodes.
   It creates the Episodes Table
   It has the id, the episode date and the number.

This model has a relationship with the appearance model.

2. Guests.

It creates the Guests table.
It has the id, name and the occupation of the guest
It has a relationship with the appearance model.

3.Appearance

It creates the appearance table. It has the id, rating, episode_id and the guest_id.

- An `Episode` has many `Guest`s through `Appearance`
- A `Guest` has many `Episode`s through `Appearance`
- An `Appearance` belongs to a `Guest` and belongs to a `Episode`

## Routes

The application has the following routes:

- GET/episodes;- returns all the episodes
- GET/episodes/:id ;- returns the episode of the specified id
- GET/guests ;- returns all the guests
- POST/appearances ;- creates a new `Appearance` that is associated with an existing `Episode` and `guest`. Accepts an object in JSON request body.
