import pytest


@pytest.mark.django_db
def test_change_post_by_id_without_auth(api_client, sample_post):
    response = api_client.patch(
        f"/api/posts/{sample_post.id}/",
        {"title": "test1", "body": "test1"},
        format="json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_change_post_by_id_with_token_auth(api_client, sample_user, sample_post):
    api_client.credentials(HTTP_AUTHORIZATION="Token " + sample_user["token"])
    data = {"title": "test1", "body": "test1"}
    response = api_client.patch(f"/api/posts/{sample_post.id}/", data, format="json")
    assert response.status_code == 200
    assert response.json()["title"] == "test1"
    assert response.json()["body"] == "test1"


@pytest.mark.django_db
def test_change_post_by_id_with_session_auth(api_client, user_data, sample_post):
    api_client.login(username=user_data["username"], password=user_data["password"])
    data = {"title": "test1", "body": "test1"}
    response = api_client.patch(f"/api/posts/{sample_post.id}/", data, format="json")
    assert response.status_code == 200
    assert response.json()["title"] == "test1"
    assert response.json()["body"] == "test1"


@pytest.mark.django_db
def test_change_post_of_other_user(
    api_client, user_data, sample_post, sample_post_by_other_user
):
    api_client.login(username=user_data["username"], password=user_data["password"])
    data = {"title": "test1", "body": "test1"}
    response = api_client.patch(
        f"/api/posts/{sample_post_by_other_user.id}/", data, format="json"
    )
    assert response.status_code == 403
