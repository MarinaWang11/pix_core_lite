# PIX Core Lite

A simplified REST API for simulating PIX payment operations.

This project was developed as part of a practical challenge and implements user authentication, PIX key management, money transfers, transaction history, and transfer idempotency.

## 🛠 Tech Stack

* **Python 3.10+**
* **FastAPI** — REST API framework
* **Pydantic** — data validation
* **SQLAlchemy** — ORM
* **SQLite** — local persistent database
* **JWT (JSON Web Token)** — authentication
* **bcrypt** — password hashing
* **Uvicorn** — ASGI server
* **Poetry** — dependency and environment management

## 📋 Prerequisites

Before running the project, make sure you have:

* Python 3.10 or higher
* Poetry

## 🚀 Getting Started

### Installation

Clone the repository:

```bash
git clone https://github.com/MarinaWang11/pix_core_lite.git
```

Enter the project directory:

```bash
cd pix_core_lite
```

Install the project dependencies using Poetry:

```bash
poetry install
```

The project uses a Poetry-managed virtual environment.

You can run commands using:

```bash
poetry run <command>
```

## 🗄️ Database

The project uses **SQLite** as its database.

The database is persisted in a local file and the required tables are created automatically from the SQLAlchemy models when the application starts.

The database contains three main tables:

* `users`
* `pix_keys`
* `transfers`

## 🌱 Database Seeding

Run the seed script with:

```bash
poetry run python seed.py
```

The seed creates pre-registered users with:

* CPF
* bcrypt-hashed password
* Initial account balance

These users can then be used to test the authentication and PIX operations.

> **Note:** The seed should be executed before the first use of the API.

## ▶️ Running the API

Start the development server with:

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

After starting the server, access:

```text
http://127.0.0.1:8000/docs
```

The five API endpoints can be tested directly through the Swagger interface.

Recommended testing flow:

1. Run the database seed.
2. Start the API.
3. Authenticate using `/auth/login`.
4. Authorize the JWT token in Swagger.
5. Check the account balance.
6. Register PIX keys for the test users.
7. Perform a PIX transfer.
8. Repeat the same transfer using the same `X-Idempotency-Key`.
9. Verify that the balance is not deducted twice.
10. Check the transfer history.

## 📦 Postman Collection

A Postman collection containing the API requests is available in:

```text
collections/PIX_Core_Lite.postman_collection.json
```

## 👩‍💻 Author

[Marina Wang](https://github.com/MarinaWang11)
