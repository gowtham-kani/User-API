# User API

Welcome to the **User API** built with FastAPI! This application provides a simple and efficient way to manage user data with CRUD operations.

## Features

- **Create** users with unique IDs, names, and emails.
- **Read** user data by ID or retrieve a list of all users.
- **Update** user details.
- **Delete** users by ID.
- **In-memory database** for quick development and testing.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)

## Getting Started

### Prerequisites

Make sure you have Python 3.7 or higher installed. You can check your Python version with:

```bash
python --version

git clone https://github.com/gowtham-kani/User-API.git
cd user-api

pip3 install fastapi uvicorn

uvicorn User_FastApi:app --reload

[Access User API](http://127.0.0.1:8000/users)
