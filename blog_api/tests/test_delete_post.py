import pytest


@pytest.mark.django_db
def test_delete_post_by_id_without_auth(api_client, sample_post):
    response = api_client.delete(f"/api/posts/{sample_post.id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_post_by_id_with_token_auth(api_client, sample_user, sample_post):
    api_client.credentials(HTTP_AUTHORIZATION="Token " + sample_user["token"])
    response = api_client.delete(f"/api/posts/{sample_post.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_post_by_id_with_session_auth(api_client, user_data, sample_post):
    api_client.login(username=user_data["username"], password=user_data["password"])
    response = api_client.delete(f"/api/posts/{sample_post.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_post_by_other_user(
    api_client, sample_user, user_data, sample_post, sample_post_by_other_user
):
    api_client.login(username=user_data["username"], password=user_data["password"])
    response = api_client.delete(f"/api/posts/{sample_post_by_other_user.id}/")
    assert response.status_code == 403
