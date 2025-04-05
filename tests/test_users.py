import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def postgres_container():
    # Use Testcontainers to spin up a PostgreSQL container
    with PostgresContainer("postgres:latest") as postgres:
        # Set environment variables for PostgreSQL user, password, and database
        postgres.with_env("POSTGRES_USER", "testuser") \
            .with_env("POSTGRES_PASSWORD", "testpassword") \
            .with_env("POSTGRES_DB", "testdb")

        # Get the connection URL
        database_url = postgres.get_connection_url()

        # Connect to the database and create the 'users' table for the tests
        import psycopg2
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

        # Yield the connection URL for use in tests
        yield database_url


@pytest.fixture(scope="module")
def setup_database(postgres_container):
    # Create a test database and insert a user
    import psycopg2
    conn = psycopg2.connect(postgres_container)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, email, password)
        VALUES ('testuser', 'testuser@example.com', 'testpassword')
    """)
    conn.commit()
    cur.close()
    conn.close()


def test_create_user(setup_database):
    response = client.post(
        "/users/",
        json={"username": "newuser", "email": "newuser@example.com", "password": "newpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"


def test_read_users(setup_database):
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0
    assert "username" in users[0]


def test_read_user(setup_database):
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "username" in data
    assert "email" in data


def test_read_non_existent_user():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
