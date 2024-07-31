import pytest


@pytest.mark.django_db
def test_create_new_post_without_auth(api_client, post_data):
    response = api_client.post("/api/posts/", post_data, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_new_post_with_token_auth(api_client, sample_user, post_data):
    api_client.credentials(HTTP_AUTHORIZATION="Token " + sample_user["token"])
    response = api_client.post("/api/posts/", post_data, format="json")
    assert response.status_code == 201
    assert response.json()["title"] == post_data["title"]
    assert response.json()["body"] == post_data["body"]
    assert response.json()["author"] == post_data["author"]


@pytest.mark.django_db
def test_create_new_post_with_session_auth(api_client, user_data, post_data):
    api_client.login(username=user_data["username"], password=user_data["password"])
    response = api_client.post("/api/posts/", post_data, format="json")
    assert response.status_code == 201
    assert response.json()["title"] == post_data["title"]
    assert response.json()["body"] == post_data["body"]
    assert response.json()["author"] == post_data["author"]
