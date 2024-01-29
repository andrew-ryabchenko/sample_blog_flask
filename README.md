### Sample Flask Blog
This Flask blog application is a user-friendly platform designed for ease of use and visual appeal. 
The homepage features a navigation bar at the top for quick access to various sections. 
Blog posts are displayed in an elegant grid layout, with each post encapsulated in a card that 
includes a title, tag, and a brief excerpt. Blog users have the capability to create and delete posts,
as well as specify a range of search criteria for locating specific posts.

#### Project Structure
- Application package - /app/
- Unit-tests - /tests/
- Pytest coverage report - /htmlcov/

#### Installation
```
cd <project_directory>
pipenv install
pipenv shell
flask run
```

#### Populate database with test data (optional)
Note: All generated test user accouts will have password - "password".
```
cd <project_directory>
pipenv shell
python -m tests
```
