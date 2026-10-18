from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import DatabaseError, PostalCodeUnavailableError
from app.routes import address, health, person, postal_codes

app = FastAPI(title="Personal Test Data Generator API")


async def database_exception_handler(
    request: Request,
    exc: DatabaseError | PostalCodeUnavailableError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Could not retrieve data from the database."},
    )


app.add_exception_handler(DatabaseError, database_exception_handler)
app.add_exception_handler(PostalCodeUnavailableError, database_exception_handler)
app.include_router(health.router)
app.include_router(postal_codes.router)
app.include_router(address.router)
app.include_router(person.router)
