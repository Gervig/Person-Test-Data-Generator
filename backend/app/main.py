from fastapi import FastAPI, HTTPException

from app.database import get_connection

app = FastAPI(title="Personal Test Data Generator API")


@app.get("/")
def home():
    return {"message": "Personal Test Data Generator API is running!"}


@app.get("/postal-codes")
def get_postal_codes():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT cPostalCode, cTownName FROM postal_code ORDER BY cPostalCode"
        )

        rows = cursor.fetchall()

        return [
            {"postal_code": postal_code, "town": town}
            for postal_code, town in rows
        ]

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve postal codes from the database.",
        ) from exc

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
