# Movie Review Management API

This is a movie review management API written in Python with Django.

[The Movie Database](https://www.themoviedb.org/) API is used to fetch and store movies in the database.

JWT is used to facilitate authentication.

## Installation

1. Via Docker

- Clone this repository

- cd in the terminal into the cloned repository and type

```
docker compose up
```

- It will start the server on http://127.0.0.1:8000

2. Via PIP

- create a virtual environment and activate it
- clone this repository into the virtual environment created.
- cd into the cloned directory in terminal and type

```bash
pip3 install -r requirements.txt
```

- Once the installation is done, type:

```
python manage.py runserver
```

- It will start the server on http://127.0.0.1:8000

## Usage

[Swagger/OpenAPI](http://127.0.0.1:8000/api/schema/swagger-ui/)

[Postman Collection](https://www.postman.com/docking-module-technologist-16036849/workspace/timble-tech/collection/36196947-10f950ba-5de9-461f-a9a9-0212cd0eed0b?action=share&creator=36196947)

## Note

The movie database API is left declared in the django settings.py file to make the testing easier. I'm aware of the consequences of such action.
