import pytest


@pytest.mark.django_db
def test_get_user_posts_without_auth(api_client):
    response = api_client.get("/api/user/1/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_user_posts_with_token_auth(api_client, sample_user, sample_post):
    api_client.credentials(HTTP_AUTHORIZATION="Token " + sample_user["token"])
    response = api_client.get(f"/api/user/{sample_user['user'].id}/")
    assert response.status_code == 200
    assert response.json()["results"][0]["author"] == sample_user["user"].id


@pytest.mark.django_db
def test_get_user_posts_with_session_auth(
    api_client, sample_user, user_data, sample_post
):
    api_client.login(username=user_data["username"], password=user_data["password"])
    response = api_client.get(f"/api/user/{sample_user['user'].id}/")
    assert response.status_code == 200
    assert response.json()["results"][0]["author"] == sample_user["user"].id
