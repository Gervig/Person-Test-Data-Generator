from types import SimpleNamespace
from unittest.mock import MagicMock

import mariadb
import pytest

from app.exceptions import DatabaseError, PostalCodeUnavailableError
from app.models.postal_code import PostalCode

# Adjust to wherever postal_code_repository.py lives in your project
from app.repositories import postal_code_repository as repo


@pytest.fixture
def db(monkeypatch):
    """A fake connection and cursor that return one postal code by default."""
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchall.return_value = [("1301", "København K")]
    cursor.fetchone.return_value = ("1301", "København K")
    monkeypatch.setattr(repo, "get_connection", lambda: connection)
    return SimpleNamespace(connection=connection, cursor=cursor)


CALLS = [
    pytest.param(repo.get_all, id="get_all"),
    pytest.param(repo.get_random, id="get_random"),
]


# Behavior shared by both functions

@pytest.mark.parametrize("call", CALLS)
def test_closes_cursor_and_connection_on_success(db, call):
    call()
    db.cursor.close.assert_called_once()
    db.connection.close.assert_called_once()


@pytest.mark.parametrize("call", CALLS)
def test_execute_error_is_wrapped_and_resources_are_closed(db, call):
    db.cursor.execute.side_effect = mariadb.Error("query failed")

    with pytest.raises(DatabaseError) as exc_info:
        call()

    assert isinstance(exc_info.value.__cause__, mariadb.Error)
    db.cursor.close.assert_called_once()
    db.connection.close.assert_called_once()


@pytest.mark.parametrize("call", CALLS)
def test_cursor_error_still_closes_connection(db, call):
    db.connection.cursor.side_effect = mariadb.Error("no cursor")

    with pytest.raises(DatabaseError):
        call()

    db.connection.close.assert_called_once()


@pytest.mark.parametrize("call", CALLS)
def test_connection_error_is_wrapped(monkeypatch, call):
    def fail():
        raise mariadb.Error("database is down")

    monkeypatch.setattr(repo, "get_connection", fail)

    with pytest.raises(DatabaseError):
        call()


# get_all

def test_get_all_returns_postal_codes_in_row_order(db):
    db.cursor.fetchall.return_value = [
        ("1301", "København K"),
        ("2200", "København N"),
    ]

    assert repo.get_all() == [
        PostalCode(postal_code="1301", town="København K"),
        PostalCode(postal_code="2200", town="København N"),
    ]


def test_get_all_strips_whitespace_from_postal_code(db):
    db.cursor.fetchall.return_value = [("1301 ", "København K")]

    assert repo.get_all()[0].postal_code == "1301"


def test_get_all_returns_empty_list_for_empty_table(db):
    db.cursor.fetchall.return_value = []

    assert repo.get_all() == []


# get_random

def test_get_random_returns_postal_code(db):
    assert repo.get_random() == PostalCode(
        postal_code="1301", town="København K"
    )


def test_get_random_strips_whitespace_from_postal_code(db):
    db.cursor.fetchone.return_value = ("1301 ", "København K")

    assert repo.get_random().postal_code == "1301"


def test_get_random_raises_when_no_postal_codes_exist(db):
    db.cursor.fetchone.return_value = None

    with pytest.raises(PostalCodeUnavailableError):
        repo.get_random()

    db.cursor.close.assert_called_once()
    db.connection.close.assert_called_once()