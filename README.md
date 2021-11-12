# FastAPI & ConfZ Demo

This repository shows how to use FastAPI & ConfZ together. It is the code-base for a corresponding blog article, see
TODO.

## Installation

Poetry is used for dependency management. To setup the repo, just run

```
poetry install
```

in this directory.

## Run API

To run the API, first set the environment variable `DB_ENV` to `db_dev.yml`. Then navigate to the folder _
fastapi_confz_demo_ and run

```
uvicorn app:app --reload
```

You should now be able to experiment with the endpoints by opening http://localhost:8000/docs.

## Run Tests

To run the tests, just execute

```
pytest
```

in this directory.
