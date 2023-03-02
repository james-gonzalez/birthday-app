import pytest
import json

from src.app import app


def test_get_route():
    response = app.test_client().get("/hello/tom")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    expected = {"message": "Hello tom! I dont know your birthday."}
    assert json.loads(response.get_data(as_text=True)) == expected


def test_put_route():
    response = app.test_client().put("/hello/john", json={"dateOfBirth": "1982-01-20"})
    assert response.status_code == 204


def test_put_route_invalid_username():
    response = app.test_client().put("/hello/1234", json={"dateOfBirth": "1982-01-20"})
    assert response.status_code == 200
    assert response.content_type == "application/json"
    expected = {"message": "Invalid username. It must contain only letters."}
    assert json.loads(response.get_data(as_text=True)) == expected


def test_put_route_date_in_future():
    response = app.test_client().put("/hello/john", json={"dateOfBirth": "2025-01-20"})
    assert response.status_code == 200
    assert response.content_type == "application/json"
    expected = {"message": "Error: The date must be in the past."}
    assert json.loads(response.get_data(as_text=True)) == expected
