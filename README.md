FastAPI with PostgreSQL and Testcontainers
This project demonstrates a FastAPI application that interacts with a PostgreSQL database using Psycopg2 for database interaction and Testcontainers for PostgreSQL integration testing. The application provides basic CRUD operations to manage users and includes unit tests for API endpoints using pytest.

Project Structure
graphql
Copy
my_fastapi_project/
│
├── app/                      # Core FastAPI application code
│   ├── __init__.py
│   ├── main.py               # FastAPI app initialization and routes
│   ├── crud.py               # CRUD operations for the database
│   └── database.py           # Database connection setup
│
├── tests/                     # Unit tests for FastAPI endpoints
│   ├── __init__.py
│   ├── test_postgresql.py    # Tests for PostgreSQL integration using Testcontainers
│   ├── test_users.py         # Tests for user-related API endpoints
│
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

**Requirements**

* Python 3.8+
* Docker (for Testcontainers)

**Dependencies**
* FastAPI: Web framework for building APIs.
* Psycopg2: PostgreSQL database adapter for Python.
* pytest: Testing framework.
* Testcontainers: Library for managing Docker containers in tests.
* Uvicorn: ASGI server to run the FastAPI app.

**Installation**
Follow the steps below to set up and run the application:

1. Clone the repository:
`git clone https://github.com/yourusername/my_fastapi_project.git
cd my_fastapi_project`

2. Set up a virtual environment and install dependencies:
`python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt`

3. Ensure Docker is running on your machine (since Testcontainers will use Docker to spin up PostgreSQL).

**Running the Application**
To start the FastAPI application, use Uvicorn:

`uvicorn app.main:app --reload`
This will start the FastAPI development server. By default, it will be available at http://127.0.0.1:8000.

**API Documentation:** You can view the automatically generated API documentation at http://127.0.0.1:8000/docs.

**Endpoints**

**POST** /users/

Create a new user.

**Request:**

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "password123"
}

**Response:**

{
  "id": 1,
  "username": "testuser",
  "email": "testuser@example.com"
}

**GET** /users/
Get a list of users with optional pagination.

**Request:**

**GET** /users/?skip=0&limit=100

**Response:**

[
  {
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com"
  }
]

**GET** /users/{user_id}

Get a user by ID.

**Request**:

**GET** /users/1

**Response**:

{
  "id": 1,
  "username": "testuser",
  "email": "testuser@example.com"
}

**Testing**
This project includes pytest for testing the API endpoints. Testcontainers is used to spin up a PostgreSQL container during testing.

**Tests Overview**
The following tests are included:

`Test creating a new user (POST /users/).

Test fetching all users (GET /users/).

Test fetching a user by ID (GET /users/{user_id}).

Test fetching a non-existent user (404 error for GET /users/{non-existent-user-id}).`

**Running Tests**
To run the tests, ensure that Docker is running on your machine (as Testcontainers uses Docker to create a PostgreSQL container for the tests).

**Run the tests using pytest:**

`pytest`

This will start the PostgreSQL container, run the tests, and then shut down the container once the tests are completed.

**Test Workflow**
Testcontainers spins up a PostgreSQL container.

The database schema and test data are set up for the tests.

pytest runs the test suite and ensures the correctness of the application by making requests to the FastAPI app.

After tests finish, the container is torn down.

Test Example
Here's an example of a test that creates a user and verifies the response:

`
def test_create_user(setup_database):
    response = client.post(
        "/users/",
        json={"username": "newuser", "email": "newuser@example.com", "password": "newpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"`

**Docker and Testcontainers**
This project uses Testcontainers to manage PostgreSQL containers for integration testing. When tests are run, Testcontainers will automatically pull a PostgreSQL image and run the database in a container, ensuring that each test runs with a fresh database instance.

**Docker Installation**
Ensure that Docker is installed and running on your machine. You can download Docker from Docker's official website.


Additional Notes
The project includes a simple PostgreSQL database setup with a users table. 
