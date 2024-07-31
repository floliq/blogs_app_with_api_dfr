from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from blog.models import Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {"username": "test", "password": "test"}


@pytest.fixture
def sample_user(user_data):
    user = User.objects.create_user(
        username=user_data["username"], password=user_data["password"]
    )
    token = Token.objects.get(user=user)
    return {"user": user, "token": token.key}


@pytest.fixture
def post_data(sample_user):
    user = sample_user["user"]
    return {
        "title": "test",
        "author": user.id,
        "body": "test",
    }


@pytest.fixture
def sample_post(sample_user):
    user = sample_user["user"]
    post = Post.objects.create(title="test", author=user, body="test")
    return post


@pytest.fixture
def sample_post_by_other_user():
    other_user = User.objects.create_user(username="other_test", password="other_test")
    post = Post.objects.create(title="test2", author=other_user, body="test2")
    return post
