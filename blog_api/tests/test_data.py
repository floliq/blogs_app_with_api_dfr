from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from blog.models import Post


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def get_new_user():
    return {
        'username': 'test',
        'password': 'test'
    }
@pytest.fixture
def create_user_db(get_new_user):
    user = User.objects.create_user(
        username=get_new_user['username'],
        password=get_new_user['password']
    )
    token = Token.objects.get(user=user)
    return {'user': user, 'token': token.key}

@pytest.fixture
def get_new_post(create_user_db):
    user = create_user_db['user']
    return {
        'title': 'test',
        'author': user.id,
        'body': 'test',
    }

@pytest.fixture
def create_post_db(create_user_db):
    user = create_user_db['user']
    post = Post.objects.create(
        title="test",
        author=user,
        body="test"
    )
    return post



def test_without_authorization(api_client):
    response = api_client.get('/api/posts/')
    print(response.json())
    assert response.status_code == 403


def test_with_admin_auth(admin_client):
    response = admin_client.get('/api/posts/')
    print(response.json())
    assert response.status_code == 200


@pytest.mark.django_db
def test_with_session_auth(api_client, create_user_db, get_new_user):
    api_client.login(username=get_new_user['username'], password=get_new_user['password'])
    response = api_client.get('/api/posts/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_with_token_auth(api_client, create_user_db):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + create_user_db['token'])
    response = api_client.get('/api/posts/')
    print(response.json())
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_new_post_without_auth(api_client, get_new_post):
    response = api_client.post('/api/posts/', get_new_post, format='json')
    print(response.json())
    assert response.status_code == 403

@pytest.mark.django_db
def test_create_new_post_with_token_auth(api_client, create_user_db, get_new_post):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + create_user_db['token'])
    response = api_client.post('/api/posts/', get_new_post, format='json')
    print(response.json())
    assert response.status_code == 201
    assert response.json()['title'] == get_new_post['title']
    assert response.json()['body'] == get_new_post['body']
    assert response.json()['author'] == get_new_post['author']

@pytest.mark.django_db
def test_create_new_post_with_session_auth(api_client, get_new_user, get_new_post):
    api_client.login(username=get_new_user['username'], password=get_new_user['password'])
    response = api_client.post('/api/posts/', get_new_post, format='json')
    print(response.json())
    assert response.status_code == 201
    assert response.json()['title'] == get_new_post['title']
    assert response.json()['body'] == get_new_post['body']
    assert response.json()['author'] == get_new_post['author']

@pytest.mark.django_db
def test_get_post_by_id_without_auth(api_client):
    response = api_client.get('/api/posts/1/')
    print(response.json())
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_post_by_id_with_token_auth(api_client, create_user_db, create_post_db):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + create_user_db['token'])
    response = api_client.get(f'/api/posts/{create_post_db.id}/')
    print(response.json())
    assert response.status_code == 200
    assert response.json()['id'] == create_post_db.id

@pytest.mark.django_db
def test_get_post_by_id_with_session_auth(api_client, get_new_user, create_post_db):
    api_client.login(username=get_new_user['username'], password=get_new_user['password'])
    response = api_client.get(f'/api/posts/{create_post_db.id}/')
    print(response.json())
    assert response.status_code == 200
    assert response.json()['id'] == create_post_db.id

@pytest.mark.django_db
def test_delete_post_by_id_without_auth(api_client, create_post_db):
    response = api_client.delete(f'/api/posts/{create_post_db.id}/')
    print(response.json())
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_post_by_id_with_token_auth(api_client, create_user_db, create_post_db):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + create_user_db['token'])
    response = api_client.delete(f'/api/posts/{create_post_db.id}/')
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_post_by_id_with_session_auth(api_client, get_new_user, create_post_db):
    api_client.login(username=get_new_user['username'], password=get_new_user['password'])
    response = api_client.delete(f'/api/posts/{create_post_db.id}/')
    assert response.status_code == 204
ТЕСТ БЕЗ ДОСТУПА
@pytest.mark.django_db
def test_update_post_by_id_without_auth(api_client, create_post_db):
    response = api_client.put(f'/api/posts/{create_post_db.id}/', {'title': 'test1', 'body': 'test1'}, format='json')
    print(response.json())
    assert response.status_code == 403

@pytest.mark.django_db
def test_update_post_by_id_with_token_auth(api_client, create_user_db, create_post_db):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + create_user_db['token'])
    data = {'title': 'test1', 'body': 'test1', 'author': create_user_db['user'].id}
    response = api_client.put(f'/api/posts/{create_post_db.id}/', data, format='json')
    assert response.status_code == 200
    assert response.json()['title'] == 'test1'
    assert response.json()['body'] == 'test1'
    assert response.json()['author'] == create_user_db['user'].id

@pytest.mark.django_db
def test_update_post_by_id_with_session_auth(api_client, create_user_db, get_new_user, create_post_db):
    api_client.login(username=get_new_user['username'], password=get_new_user['password'])
    data = {'title': 'test1', 'body': 'test1', 'author': create_user_db['user'].id}
    response = api_client.put(f'/api/posts/{create_post_db.id}/', data, format='json')
    assert response.status_code == 200
    assert response.json()['title'] == 'test1'
    assert response.json()['body'] == 'test1'
    assert response.json()['author'] == create_user_db['user'].id
# нет доступа

@pytest.mark.django_db
def test_change_post_by_id_without_auth(api_client, create_post_db):
    response = api_client.patch(f'/api/posts/{create_post_db.id}/', {'title': 'test1', 'body': 'test1'}, format='json')
    print(response.json())
    assert response.status_code == 403

@pytest.mark.django_db
def test_change_post_by_id_with_token_auth(api_client, create_user_db, create_post_db):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + create_user_db['token'])
    data = {'title': 'test1', 'body': 'test1'}
    response = api_client.patch(f'/api/posts/{create_post_db.id}/', data, format='json')
    assert response.status_code == 200
    assert response.json()['title'] == 'test1'
    assert response.json()['body'] == 'test1'

@pytest.mark.django_db
def test_change_post_by_id_with_session_auth(api_client, get_new_user, create_post_db):
    api_client.login(username=get_new_user['username'], password=get_new_user['password'])
    data = {'title': 'test1', 'body': 'test1'}
    response = api_client.patch(f'/api/posts/{create_post_db.id}/', data, format='json')
    assert response.status_code == 200
    assert response.json()['title'] == 'test1'
    assert response.json()['body'] == 'test1'

# НЕТ ДОСТУПА