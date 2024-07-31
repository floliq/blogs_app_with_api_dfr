import pytest


def test_without_authorization(api_client):
    response = api_client.get("/api/posts/")
    assert response.status_code == 403


def test_with_admin_auth(admin_client):
    response = admin_client.get("/api/posts/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_with_session_auth(api_client, sample_user, user_data):
    api_client.login(username=user_data["username"], password=user_data["password"])
    response = api_client.get("/api/posts/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_with_token_auth(api_client, sample_user):
    api_client.credentials(HTTP_AUTHORIZATION="Token " + sample_user["token"])
    response = api_client.get("/api/posts/")
    assert response.status_code == 200
