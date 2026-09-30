from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def register_and_login():

    email = "test@example.com"

    client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "secret123",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "secret123",
        },
    )

    return response.json()[
        "access_token"
    ]


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_home_planner():

    token = register_and_login()

    response = client.post(
        "/api/generate-home",

        headers={
            "Authorization":
                f"Bearer {token}"
        },

        json={

            "budget": 50000,

            "rooms": [
                "Living Room"
            ],

            "items": [

                {
                    "category":
                        "furniture",

                    "item":
                        "Sofa",

                    "quantity":
                        1,

                    "style":
                        "modern",
                }

            ],

            "style":
                "modern",

            "city":
                "Chennai",
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["planner"]
        == "home"
    )