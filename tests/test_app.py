import pytest

from src.app import app


def test_get_route():
    response = app.test_client().get("/hello/john")
    assert response.status_code == 200


def test_put_route():
    response = app.test_client().put("/hello/john", json={"dateOfBirth": "1982-01-20"})
    assert response.status_code == 204


def test_put_route_invalid_username():
    response = app.test_client().put("/hello/1234", json={"dateOfBirth": "1982-01-20"})
    assert response.status_code == 200
    assert (
        response.data.decode("utf-8")
        == "Invalid username. It must contain only letters."
    )


def test_put_route_date_in_future():
    response = app.test_client().put("/hello/john", json={"dateOfBirth": "2025-01-20"})
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Error: The date must be in the past."
