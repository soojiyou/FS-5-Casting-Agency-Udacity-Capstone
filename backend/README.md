# FSND_Capstone
## Final project for Udacity Full Stack Web Dev Nanodegree
The motivation for this project was to practice the skills and demonstrate knowledge of the material presented in the course.
This app allows to create and manage movie list and actor list. There are two roles:
Asistant, which allows to only read each list of movie and actor and in detail information and
Producer, which allows all permission. 
Heroku Link: https://fsndapp107098.herokuapp.com

### Vital dependencies and platforms
-[Flask]
Flask is a lightweight microservices web framework that utilizes Python.
-[SQLAlchemy]
SQLAlchemy is a SQL ORM that allows user to write pythonic code and not raw SQL.
-[Auth0]
Auth0 is how authentication and authorization is achieved in this api.
-[PostgreSQL]
The relational database platform used in this API
-[Heroku]
The cloud platform this API has been deployed on.

# Getting Started:

### Python 3.10.10 (Virtual Environment)


### PIP Requirements and Environmental Variables
Once you have setup your virtual environment running, easily install requirements with the following command:
```bash
pip install -r requirements.txt
```
Set the necessary environment variables:
These can be found within the setup.sh file.

### Running Local Tests
First, a database must be created to restore the sql database provided.
```bash
createdb capstone
```
create simple database with model.py.
The database is reset for each run.


Configure the database path to connect to this new locally created postgres database:
```bash
export DATABASE_URL=<local_database_url>
```
Then deploy locally and run the tests from another terminal:
```bash
export FLASK_APP=app.py
flask run --reload
python test.py
```

#### authorization setup with Auth0

Setup an Auth0 account.

Environment variables needed: (setup.sh)

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="casting_agency" # name will varies. Create an API in Auth0
```

##### Roles

Create three roles for users under `Users & Roles` section in Auth0

* Casting Assistant
	* Can view actors and movies
* Casting Director
	* All permissions a Casting Assistant has and…
	* Add or delete an actor from the database
	* Modify actors or movies
* Executive Producer
	* All permissions a Casting Director has and…
	* Add or delete a movie from the database


##### Permissions

Following permissions should be created under created API settings.

* `get:actor`
* `get:movie`
* `get:actor-detail`
* `get:movie-detail`
* `post:actor`
* `post:movies`
* `patch:actor`
* `patch:movie`
* `delete:actor`
* `delete:movie`


##### Set JWT Tokens in `.env` or `auth0_config.json`

Use the following link to create users and sign them in. This way, you can generate 
```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
            "success": False,
            "error": 422,
            "message": "unprocessable"
}
```

The API will return three error types when requests fail:
- 400: Bad Request
- 401: authentication error
- 404: Not Found
- 422: unprocessable 
- 500: Internal Server Error




### Endpoints


#### GET /movies
* Get an movie ist with each id

* Requires `get:movie` permission

* **Example Request:** `curl 'http://localhost:5000/movies'`

* **Expected Result:**
 ```json
 {
    "movies": {
        "1": "movietest1"
    },
    "success": true
}
```


	
#### GET /actors
* Get an actors ist with each id

* Requires `get:actor` permission

* **Example Request:** `curl 'http://localhost:5000/actors'`

* **Expected Result:**
 ```json
 {
    "actors": {
        "1": "actortest1"
    },
    "success": true
}
```
	
#### GET /movies/<int:movie_id>
* Get movie detail with specific id

* Requires `get:movie-detail` permission

* **Example Request:** `curl 'http://localhost:5000/movies/1'`

* **Expected Result:**
 ```json
  {
    "movie_data": {
        "genres": "sci-fi",
        "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2",
        "movie_id": 1,
        "movie_title": "movietest1",
        "release_date": "20230315"
    },
    "success": true
}
```
#### GET /actors/<int:actor_id>
* Get actor detail with specific id

* Requires `get:actor-detail` permission

* **Example Request:** `curl 'http://localhost:5000/actors/1'`

* **Expected Result:**
 ```json
  {
    "actor_data": {
        "actor_age": "23",
        "actor_gender": "female",
        "actor_id": 1,
        "actor_name": "actortest1",
        "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
    },
    "success": true
}
```
	
#### POST /movies
* Creates a new movie.

* Requires `post:movie` permission

* Requires the title, release date, genres, image_link.

* **Example Request:** (Create)
    ```bash
	curl --location --request POST 'http://localhost:5000/movies' \
		--header 'Content-Type: application/json' \
		--data-raw '{
   
    "gneres":"romance",
    "movie_title": "romancemovie1",
    "release_date": "20230320",
    "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
}'
```
    
* **Example Response:**
    ```bash
	{
    "posted_movie_profile": {
        "genres": "romance",
        "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2",
        "movie_id": 2,
        "movie_title": "romancemovie1",
        "release_date": "20230320"
    },
    "success": true
}
	```

#### POST /actors
* Creates a new actor.

* Requires `post:actor` permission

* Requires the name, age, gender, image_link of the actor.

* **Example Request:** (Create)
    ```json
	curl --location --request POST 'http://localhost:5000/actors' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			  "age": "20",
        "gender": "male",
        "name": "actortest2",
        "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
        }'
    ```
    
* **Example Response:**
    ```json
	{
    "posted_actor_profile": {
        "actor_age": "20",
        "actor_gender": "male",
        "actor_id": 2,
        "actor_name": "actortest2",
        "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
    },
    "success": true
}
    ```

#### DELETE /movies/<int:movie_id>
* Deletes the movie with given id 

* Require `delete:movie` permission

* **Example Request:** `curl --request DELETE 'http://localhost:5000/movies/2'`

* **Example Response:**
    ```json
	{
		"deleted": 2,
    "success": true
    }
    ```
    
#### DELETE /actors/<int:actor_id>
* Deletes the actor with given id 

* Require `delete:actor` permission

* **Example Request:** `curl --request DELETE 'http://localhost:5000/actors/2'`

* **Example Response:**
    ```json
	{
		"deleted": 2,
		"success": true
    }
    ```

#### PATCH /movies/<int:movie_id>
* Updates the movie where <int:movie_id> is the existing movie id

* Require `patch:movie` permission

* Update the corresponding fields for Movie with id <movie_id>

* **Example Request:** 
	```json
    curl --location --request PATCH 'http://localhost:5000/movies/1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"title": "patch movie test"
        }'
  	```
  
* **Example Response:**
    ```json
	{
    "patched_movie_profile": {
        "genres": "sci-fi",
        "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2",
        "movie_id": 1,
        "movie_title": "patch movie test",
        "release_date": "20230315"
    },
    "success": true
}
    ```
	
#### PATCH /actors/<int:actor_id>
* Updates the actor where <int:actor_id> is the existing actor id

* Require `patch:actor`

* Update the given fields for Actor with id <actor_id>

* **Example Request:** 
	```json
    curl --location --request PATCH 'http://localhost:5000/actors/1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "patch actor test"
        }'
  ```
  
* **Example Response:**
    ```json
	{
    "patched_actor_profile": [
        {
            "actor_age": "23",
            "actor_gender": "female",
            "actor_id": 1,
            "actor_name": "patch actor test",
            "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
        }
    ],
    "success": true
}
	```
