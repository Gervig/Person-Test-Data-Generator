# Local Database Setup — Personal Test Data Generator

This guide explains how to set up the MariaDB database used by the Personal Test Data Generator project. The database runs in Docker, and DataGrip is used to connect to it, inspect the schema, and query the data.

## Prerequisites

Install the following tools:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [DataGrip](https://www.jetbrains.com/datagrip/)
- The project repository, including `data/addresses.sql`

The commands below use Windows PowerShell.

## 1. Project structure

The relevant project files are organised as follows:

```text
Person Test Data Generator/
├── backend/
│   └── compose.yaml
└── data/
    ├── addresses.sql
    └── person-names.json
```

The `addresses.sql` file contains the provided postal-code and town data.

## 2. Configure MariaDB with Docker

Create a file named `compose.yaml` in the `backend` directory:

```yaml
services:
  mariadb:
    image: mariadb:11
    container_name: test-data-mariadb
    restart: "no"
    environment:
      MARIADB_ROOT_PASSWORD: local_dev_password
      MARIADB_DATABASE: test_data
    ports:
      - "3306:3306"
    volumes:
      - mariadb_data:/var/lib/mysql

volumes:
  mariadb_data:
```

### Configuration details

- **Image:** MariaDB 11
- **Container name:** `test-data-mariadb`
- **Port:** `3306`
- **Initial database:** `test_data`
- **Persistent storage:** `mariadb_data`
- **Restart policy:** `no`, so Docker does not automatically restart the container

The password shown is for local development only. Do not use it for a publicly accessible database or production deployment.

## 3. Start and stop the database

Open PowerShell and navigate to the `backend` directory:

```powershell
cd path\to\Person Test Data Generator\backend
```

Start MariaDB:

```powershell
docker compose up -d
```

Check the container status:

```powershell
docker compose ps
```

To stop MariaDB when finished:

```powershell
docker compose stop
```

To start it again later, run `docker compose up -d` from the same directory.

The named Docker volume preserves the database contents when the container is stopped.

**Important:** Do not run `docker compose down -v` unless you intend to delete the database volume and its stored data.

## 4. Prepare the SQL dump

The provided `addresses.sql` file is a phpMyAdmin dump containing MariaDB-specific statements, including database selection and a stored procedure.

The original dump selects a database named `addresses`. To keep the imported table in the intended `test_data` database, the dump was edited before import.

In `data/addresses.sql`, replace these statements:

```sql
CREATE DATABASE IF NOT EXISTS `addresses`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE `addresses`;
```

with:

```sql
USE `test_data`;
```

Keep the remaining table definitions, stored procedure statements, and insert data intact.

## 5. Copy the SQL dump into the container

From the `backend` directory, copy the file into the running MariaDB container:

```powershell
docker cp "..\data\addresses.sql" test-data-mariadb:/tmp/addresses.sql
```

The relative path works because the `data` directory is one level above `backend`.

If the SQL file is edited again, copy it into the container again before importing it.

## 6. Import the data

Open the MariaDB client inside the running container:

```powershell
docker exec -it test-data-mariadb mariadb -uroot -plocal_dev_password test_data
```

At the MariaDB prompt, execute the dump:

```sql
source /tmp/addresses.sql
```

The `source` command is a MariaDB client command, so it is entered at the MariaDB prompt rather than as an ordinary SQL query.

During the import, the client should report successful statements and inserted rows. In the initial import, **589 rows were inserted**.

The prompt may change to `MariaDB [addresses]>` if the dump still selects the original database. If that happens, check the database location before proceeding.

Exit the MariaDB client with:

```sql
exit
```

## 7. Verify the import

Connect to the database and check the current database:

```sql
SELECT DATABASE();
```

List the available tables:

```sql
SHOW TABLES;
```

Check the imported postal-code data:

```sql
SELECT cPostalCode, cTownName
FROM postal_code
LIMIT 10;
```

The query should return postal codes and their corresponding town names.

## 8. Connect DataGrip to MariaDB

1. Open DataGrip.
2. Create a new data source using **MariaDB**.
3. Configure the connection:

   | Setting | Value |
   |---|---|
   | Host | `localhost` |
   | Port | `3306` |
   | User | `root` |
   | Password | `local_dev_password` |
   | Database | `test_data` |

4. Download the MariaDB driver if DataGrip prompts you.
5. Click **Test Connection** and confirm that it succeeds.
6. Apply the settings and expand the connection in the Database panel.
7. Refresh the connection and enable the relevant database/schema if it is not visible.

To inspect the data, expand the database, open **Tables**, and select `postal_code`. Use **View Data** or **Jump to Data** to open the table in a grid.

If the dump created the table in `addresses` instead of `test_data`, select `addresses` in DataGrip or correct the dump and import it into the intended database.

## 9. Notes for team members

- Docker provides a consistent MariaDB environment across team members' computers.
- DataGrip is a database client; it does not replace the MariaDB server.
- The database files persist in the Docker volume, so stopping the container does not normally delete the data.
- The `addresses.sql` file must be available locally before importing it.
- Each team member should use their own local development credentials and avoid committing real secrets.
- If port `3306` is already in use, change the host-side port mapping and use that port in DataGrip and the Python connection configuration.

## Troubleshooting

### Docker cannot find the SQL file

Confirm that PowerShell is in the `backend` directory and run:

```powershell
Get-ChildItem -Path .. -Filter addresses.sql -Recurse -File
```

Use the path returned by the command to correct the `docker cp` command.

### DataGrip cannot connect

Check that Docker Desktop is running and that the MariaDB container is healthy:

```powershell
docker compose ps
docker logs test-data-mariadb
```

Verify the host, port, username, password, and selected database in DataGrip.

### The table is not visible

Refresh the DataGrip connection and ensure the database containing `postal_code` is selected. Run `SHOW TABLES;` to confirm which database contains the table.

### Import errors

Inspect the reported SQL statement. Dumps containing `DELIMITER`, stored procedures, or a `DEFINER` clause may require special handling. Do not assume the entire dump imported successfully just because some statements succeeded; verify the table and data with the queries above.

---

**Result:** A locally running MariaDB instance in Docker, accessible through DataGrip, with the project's postal-code and town data available for development and testing.