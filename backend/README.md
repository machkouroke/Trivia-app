# Backend - Udacitrivia

## Setting up the Backend

### Install Dependencies
In your `backend` directory:

1. Make sure python 3.7 or higher is installed on your machine
```bash
python3 --version
```
2. Create a virtual environment and activate it
- Linux Command Line
```bash
python3 -m venv env
source env/Scripts/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
**Note:** If you are using Windows, You can use git bash to run all the commands

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
cd flaskr
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Testing
If you want to run tests at home please follow these instructions:
(In the `backend` directory)
```bash
dropdb trivia_test && createdb trivia_test
psql trivia_test < trivia.psql
cd ..
python -m unittest backend/test_flaskr.py 
```
