# Personal Test Data Generator

A Python FastAPI project for generating personal test data, backed by MariaDB and tested with pytest. Postman is used to test the API endpoints.

## Table of Contents

- [1. Project Structure](#1-project-structure)
- [2. Requirements](#2-requirements)
- [3. Get the Project](#3-get-the-project)
- [4. Install Python and uv](#4-install-python-and-uv)
- [5. Set Up the Python Environment](#5-set-up-the-python-environment)
- [6. Configure Environment Variables](#6-configure-environment-variables)
- [7. Start the Database](#7-start-the-database)
- [8. Run the API](#8-run-the-api)
- [9. Test the API](#9-test-the-api)
- [10. Run Automated Tests](#10-run-automated-tests)
- [11. Set Up Postman](#11-set-up-postman)
- [12. Git and GitHub Workflow](#12-git-and-github-workflow)
- [13. Troubleshooting](#13-troubleshooting)

---

## 1. Project Structure

The repository is organized approximately as follows:

```text
Person-Test-Data-Generator/
├── .postman/                  # Postman Native Git configuration/resources
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── database.py        # Database connection
│   │   ├── data_loader.py     # Data-loading functionality
│   │   ├── generators.py      # Test-data generation
│   │   └── models/             # Data models
│   ├── tests/                  # Automated tests
│   ├── .env                    # Local environment variables (not committed)
│   ├── pyproject.toml          # Python project and dependencies
│   ├── uv.lock                 # Locked dependency versions
│   └── compose.yaml            # Docker Compose configuration, if present
├── data/                       # Project data files
├── postman/                    # Saved Postman requests
└── README.md                   # Project documentation
```

The exact files may change as the project develops.

**Important:** Keep `.postman` and `postman` in the repository root unless the project's Postman Native Git configuration specifies otherwise.

## 2. Requirements

Install or have access to the following:

- **Python 3.13** — the project has been developed using Python 3.13.7.
- **uv** — Python project and dependency manager.
- **Docker Desktop** — to run MariaDB in a container.
- **Git** — to clone and synchronize the repository.
- **Postman** — to send API requests and inspect responses.
- **Visual Studio Code** or another code editor.

## 3. Get the Project

Repository: https://github.com/Gervig/Person-Test-Data-Generator

### Option A: Clone the repository

Use this option when setting up a new laptop that does not yet have a local copy.

1. Open a terminal in your preferred parent directory.
2. Clone the repository:

   ```powershell
   git clone https://github.com/Gervig/Person-Test-Data-Generator.git
   ```

3. Open the project folder in Visual Studio Code or your preferred editor.

   ```powershell
   cd Person-Test-Data-Generator
   ```

### Option B: Open an existing local project

If the project is already downloaded, open the existing `Person-Test-Data-Generator` folder. Do not clone it again into the same project directory.

Before proceeding, confirm that the folder contains the `backend` directory and the Postman folders.

## 4. Install Python and uv

### Check Python

Open PowerShell and run:

```powershell
python --version
```

The expected version for the current development setup is Python 3.13.x.

### Install uv

If `uv` is not installed, use the official installation instructions:

https://docs.astral.sh/uv/getting-started/installation/

On Windows, the PowerShell installer is one option.

### Verify uv

```powershell
uv --version
```

If PowerShell says that `uv` is not recognized, check whether the executable exists here:

```powershell
& "$HOME\.local\bin\uv.exe" --version
```

If that works, temporarily add its directory to the current PowerShell session:

```powershell
$env:Path = "$HOME\.local\bin;$env:Path"
```

Then check again:

```powershell
uv --version
```

To make this change permanent for your Windows user, run:

```powershell
$uvPath = "$HOME\.local\bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

if (($userPath -split ';') -notcontains $uvPath) {
    $newPath = (@($userPath, $uvPath) | Where-Object { $_ }) -join ';'
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
}
```

Close and reopen PowerShell before checking `uv --version` again.

## 5. Set Up the Python Environment

Change to the backend directory:

```powershell
cd backend
```

Check that the project files are present:

```powershell
Get-ChildItem
```

The directory should contain `pyproject.toml` and, if tracked in the repository, `uv.lock`.

Install the project's dependencies:

```powershell
uv sync
```

This command creates the local `.venv` environment if necessary and installs the dependencies defined by the project.

**Why use `uv sync`?** It helps recreate the same dependency environment on different computers using the project's dependency definitions and lockfile.

Run commands from the `backend` directory unless otherwise specified.

## 6. Configure Environment Variables

The backend uses a local `.env` file for database settings.

1. Check whether `backend/.env` exists.
2. If it does not exist, create it using the variable names and format expected by `backend/app/database.py` and the database configuration.
3. Enter the appropriate local database credentials and settings.

Do not guess variable names. Check the existing configuration or ask the project maintainer for the required values.

Example format only:

```dotenv
# Replace these example names with the exact names expected by the application.
# Do not use real credentials in a committed example file.
```

The `.env` file must not be committed to Git because it may contain passwords or other private configuration.

If the project needs a template, create a separate `.env.example` containing only variable names and safe placeholder values.

## 7. Start the Database

The project uses MariaDB in Docker.

First, ensure Docker Desktop is installed and running.

From the `backend` directory, run:

```powershell
docker compose up -d
```

This starts the services defined in the Docker Compose configuration in the background.

Check the running containers:

```powershell
docker compose ps
```

If a container is not running, inspect its logs:

```powershell
docker compose logs
```

Before starting the API, ensure that the database service is running and that the credentials and database settings in `backend/.env` match the Docker configuration.

To stop the database services later:

```powershell
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to remove associated volumes and understand the data-loss implications.

## 8. Run the API

From the `backend` directory, start FastAPI:

```powershell
uv run uvicorn app.main:app --reload
```

The `--reload` option automatically restarts the development server when application code changes.

When the server starts successfully, open:

- API root: http://127.0.0.1:8000/
- Interactive API documentation: http://127.0.0.1:8000/docs
- Postal codes endpoint: http://127.0.0.1:8000/postal-codes

The root endpoint should return the configured API status message.

Keep the terminal open while using the API. Stop the server with `Ctrl+C`.

## 9. Test the API

You can test the API using Postman or directly in a browser for simple GET endpoints.

### API status

Send a `GET` request to:

```text
http://127.0.0.1:8000/
```

The response should be JSON containing the API's status message.

### Postal codes

Send a `GET` request to:

```text
http://127.0.0.1:8000/postal-codes
```

The response should be a JSON array of postal-code records.

Use the interactive documentation at `/docs` to see the currently implemented endpoints and their expected inputs.

## 10. Run Automated Tests

Open a second PowerShell terminal and change to the backend directory.

Run the tests:

```powershell
uv run pytest -v
```

The `-v` option displays the individual test names and their results.

To run tests with coverage, if `pytest-cov` is installed in the project environment:

```powershell
uv run pytest --cov=app --cov-report=term-missing
```

Review failing tests before committing changes.

If dependencies are missing, check `pyproject.toml` and install the project environment with `uv sync`.

## 11. Set Up Postman

The repository contains two important Postman-related folders:

- `postman/` — saved API requests.
- `.postman/` — Postman Native Git configuration and resource definitions.

Keep both folders in the repository root unless the existing Native Git configuration requires a different structure.

### Connect the project

1. Open Postman.
2. Open the workspace connected to the repository, if it is available.
3. Check the Native Git configuration and ensure it points to the correct local repository.
4. If the repository is not on the laptop, clone it first.
5. Check that the saved requests are visible in Postman.

If the requests are saved locally but do not appear in the Postman interface, inspect the Native Git configuration before importing individual files. Do not assume that the files can all be imported as one JSON collection.

### Configure the base URL

The API request collection uses a `base_url` variable:

```text
http://127.0.0.1:8000
```

The requests can then use URLs such as:

```text
{{base_url}}/
```

and:

```text
{{base_url}}/postal-codes
```

Make sure the FastAPI server is running before sending requests.

### Run the requests

1. Select the relevant collection.
2. Open a request and click **Send**.
3. Check the status code and response body.
4. Run the collection or use the Collection Runner to execute multiple requests.
5. Confirm that the response tests pass.

The existing requests include checks for HTTP status, valid JSON, response time, expected response content, and postal-code fields.

## 12. Git and GitHub Workflow

Before making changes, check your working tree:

```powershell
git status
```

Pull the latest changes when appropriate:

```powershell
git pull
```

After making and testing changes, review the files:

```powershell
git status
git diff
```

Stage the files you intend to commit:

```powershell
git add .
```

Commit your changes:

```powershell
git commit -m "Describe the changes"
```

Push the commit to GitHub:

```powershell
git push
```

Be careful when staging files. Check that `.env`, virtual environments, caches, and other local-only files are not included.

A typical `.gitignore` should exclude at least:

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/

# Virtual environments
.venv/
venv/

# Local secrets
.env

# Editor and operating-system files
.vscode/
.DS_Store
Thumbs.db
```

Keep the dependency files, source code, tests, data files intended for the repository, and required Postman resources under version control.

## 13. Troubleshooting

### `uv` is not recognized

Check:

```powershell
& "$HOME\.local\bin\uv.exe" --version
```

If that works, add `$HOME\.local\bin` to your PATH and restart PowerShell.

### Python dependencies are missing

From `backend`, run:

```powershell
uv sync
```

### The API cannot connect to MariaDB

Check that Docker Desktop is running:

```powershell
docker compose ps
```

Review the database logs:

```powershell
docker compose logs
```

Verify the `.env` values against the Docker Compose configuration. Confirm that the database is ready before starting the API.

### The API is already using port 8000

Stop the other server with `Ctrl+C`, or identify the process using the port before starting another server.

### Postman requests fail

Check that:

- FastAPI is running.
- The `base_url` variable is set to `http://127.0.0.1:8000`.
- The request method and path are correct.
- The database is running if the endpoint requires it.
- Postman is using the intended collection and environment.

### Tests fail

Run:

```powershell
uv run pytest -v
```

Read the first relevant error and check the fixture data, model validation, database configuration, and dependencies as appropriate.

---

## Quick Start Checklist

For subsequent sessions, when the project is already installed:

- [ ] Open the project in your editor.
- [ ] Start Docker Desktop.
- [ ] Open PowerShell in `backend`.
- [ ] Start the database with `docker compose up -d`.
- [ ] Start FastAPI with `uv run uvicorn app.main:app --reload`.
- [ ] Open `http://127.0.0.1:8000/docs` or run the saved Postman requests.
- [ ] Run `uv run pytest -v` after code changes.
- [ ] Commit and push changes when ready.

**Remember:** The initial setup is a one-time task on each computer. After that, you generally only need to start the database and API, run your tests, and synchronize your Git changes.
