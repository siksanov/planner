import httpx
import pytest

@pytest.mark.asyncio
async def test_sign_user_up(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuserform@pact.com",
        "password": "testpasswordform"
    }

    data = f'grant_type=password&username={payload["username"]}&password={payload["password"]}&scope=&client_id=&client_secret='

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    test_response = {
        "message": "User created successfully."
    }

    response = await default_client.post("api/v1/user/signup",
                                         json=data, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == test_response

@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuserform@pact.com",
        "password": "testpasswordform"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = f'grant_type=password&username={payload["username"]}&password={payload["password"]}&scope=&client_id=&client_secret='

    response = await default_client.post("api/v1/user/signin", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"