from fastapi.testclient import TestClient

from app.database import get_connection
from app.main import app

client = TestClient(app)


def test_database_connection_and_postal_codes():
    """Verify that we can connect to MariaDB and read postal codes."""
    connection = get_connection()

    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT cPostalCode, cTownName
                FROM postal_code
                WHERE cPostalCode = ?
                """,
                ("1301",),
            )
            result = cursor.fetchone()
        finally:
            cursor.close()

        assert result is not None
        assert result[0].strip() == "1301"
        assert result[1] == "København K"

    finally:
        connection.close()


def test_postal_codes_api_returns_database_data():
    """Verify that the API returns postal codes from MariaDB."""
    response = client.get("/postal-codes")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    assert {
        "postal_code": "1301",
        "town": "København K",
    } in data
