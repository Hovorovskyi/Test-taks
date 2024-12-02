# Test Task for Chi 🎯

This project is a **backend solution** for a test task, built with **Flask**, **SQLAlchemy**, and Docker. It includes CI/CD pipelines configured using **GitHub Actions**.

---

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Migrate
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Pytest, Pytest-Cov
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose

---
## 📦 Installation

### Prerequisites
- Python 3.12+
- Docker and Docker Compose
- PostgreSQL client installed locally (optional)

1. Clone the repository:
   ```bash
   git clone https://github.com/Hovorovskyi/Test-taks.git
   cd Test-taks
   ```
   
2. Install dependencies using Poetry:
    ```
    poetry install
   ```

3. Set up your environment variables. Create a .env file in the root directory:
    ```
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret
    DATABASE_URL=postgresql://<USER>:<PASSWORD>@db:5432/<DB_NAME>
    POSTGRES_USER=<USER>
    POSTGRES_PASSWORD=<PASSWORD>
    POSTGRES_DB=<DB_NAME>
   ```
---
## 🐳 Running with Docker

1. Build and start the containers:
    ```
   docker-compose up --build
   ```
   
2. Access the application at http://localhost:5050.
---
## 🧪 Running Tests
1. ```
    docker-compose run app pytest --cov=app tests/
   ```
---
## ⚙️ CI/CD Pipeline
- This project uses GitHub Actions to run tests and ensure code quality for every commit. 
- The configuration is in the .github/workflows/ci.yml file.
---
## 🛠️ Commands
- Apply database migrations:
    ```
  docker-compose run app alembic upgrade head
  ```

- Create a new migration:
    ```
  docker-compose run app alembic revision --autogenerate -m "Migration message"
  ```
