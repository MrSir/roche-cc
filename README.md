# Roche Code Challenge

## Installation & Setup
Run the following commands in order to configure the project:

`pip install -r requirements.txt` - to install the dependencies for the project

`uvicorn main:app --reload` - to start the FastAPI server so that you can view the documentation. Note that starting the server will also run create all the tables for the models inside the `roche_cc.db` SQLite file.

The API documentation can be access at `http://127.0.0.1:8000/docs#/`

## Technologies
- [FastAPI](https://fastapi.tiangolo.com) - used as the backbone for the application. It was chosen because it provided enough flexibility to build the API as one desires, but with enough utility in place to actually make things go a lot faster than writing from scratch. It came with automatic Swagger documentation based on typing, which is a huge plus.
- [Pydantic](https://docs.pydantic.dev/latest/) - was added to quickly define schema classes for the request and response payloads. It already plays nicely with FastAPI, so using it was a no brainer.
- [SQLAlchemy](https://www.sqlalchemy.org) - In this day and age writing raw SQL is simply not a good idea. Since we want the api to have a database with also want the code to have an ORM to make DB interactions a little safer and more pleasant to write.
- [SQLite](https://www.sqlite.org/index.html) - Since this coding challenge is more of a proof of concept than anything else, using a simple database to save time was key. Should this actually be built for product something like [MySQL](https://www.mysql.com) or [PostreSQL](https://www.postgresql.org) would have been used.
- [Arrow](https://arrow.readthedocs.io/en/latest/) - there were some date time operations I added as part of the code, and in order to make them much easier to do I ended up pulling in arrow as well.

## Code Structure
The code is organized into modules that clearly describe what is contained within them. For a little more context these can be interpreted as:
- `api/controllers` - this is  where all the controllers registering the API routes and the overall endpoint orchestration resides
- `api/database` - this is where you will find the configurations for the database connectivity, as well as the model definitions
- `api/jobs` - Job classes are defined as encapsulations of code that are meant to be placed on a queue and picked up by a worker servers, to be processed asynchronously. (Hint: think worker tasks in Djang/Celery)
- `api/services` - this where service classes that encapsulate actions related to a specific context reside. Services allow code to be more re-usable but also far more single responsibility. Service classes aid in moving logic away from places it does not belong. (e.g. controllers shouldn't really be concerned with what happens behind the scenes)
- `api/validation` - this is where the Rule and Validator mechanisms reside. These mechanisms are used for implementing more robust request validation. The idea being that before the controllers decide to do anything with the data, it must be validated first.
- `tests` - as the name implies this is where the test suite for the api is.

## Architecture
```mermaid
graph ERD;
    User-->ShoppingCart
    ShoppingCart-->Item
    Item-->Product
```

## Mechanisms NOT Implemented
- Authentication layer for the API is something I didn't bother spending time on. It wasn't mentioned in the requirements, and I figured it is assumed that ANY API would have an authentication layer built for it. So while this component is missing, it should absolutely exist in a production setup
- Authorization layer for the API was also something that was skipped. I did lay some of the contract work (e.g. `authorized_to(...)`) to imply that such a piece must also be implemented. In my opinion each API endpoint must perform proper authorization checks for the authenticated user. Just because you are authenticated doesn't mean you can perform a certain action.
- The queueing and worker background processing mechanisms are not implemented. While the Job classes are in place and partially tested, there is nothing in place to actually schedule these and then process them. In a production environment one would likely have something like Celery with a Redis queue up and running for crunching through these.
- While I did add support for an SQLite database, and have provided some testing for the db operations code, it is mostly mocked. The db operations are not the most stylish or performant, and are there just to illustrate what needs to be done.

## Bon