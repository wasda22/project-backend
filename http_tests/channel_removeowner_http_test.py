import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode


@clear
def test_valid_input():
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    creator_id = user1.json().get('auth_user_id')

    u_id = user2.json().get('auth_user_id')

    ch = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'big fish!',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    requests.post(url + "/channel/addowner/v1", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })

    response = requests.post(url + "/channel/removeowner/v1", json = {
        'token': token2,
        'channel_id' : ch_id,
        'u_id': creator_id
    })
    assert response == 201

    url2 = urlencode({"token": token2, "channel_id": ch_id})

    channel = requests.get(url + 'channel/details/v2?' + url2).json()

    assert creator_id not in [user['u_id'] for user in channel['owner_members']]


@clear
def test_invalid_channel_id():
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    u_id = user2.json().get('auth_user_id')

    ch_id = 10

    response = requests.post(url + "/channel/removeowner/v1", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })
    assert response.status_code == 400

@clear
def test_user_the_only_owner():
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    u_id = user1.json().get('auth_user_id')

    ch = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'big fish!',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    response = requests.post(url + "/channel/removeowner/v1", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })
    assert response.status_code == 400

@clear
def test_auth_user_not_owner():
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    u_id = user2.json().get('auth_user_id')

    ch = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'big fish!',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    response = requests.post(url + "/channel/removeowner/v1", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })
    assert response.status_code == 400

@clear
def test_auth_user_no_access():
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    user3 = helper.register_user(3)

    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    u_id = user3.json().get('auth_user_id')

    ch = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'big fish!',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    requests.post(url + "/channel/addowner/v1", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })

    response = requests.post(url + "/channel/removeowner/v1", json = {
        'token': token2,
        'channel_id' : ch_id,
        'u_id': u_id
    })
    assert response.status_code == 403

@clear
def test_auth_user_global_owner():
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    user3 = helper.register_user(3)

    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    u_id = user3.json().get('auth_user_id')

    ch = requests.post(url + 'channels/create/v2', json = {
        'token': token2,
        'name': 'big fish!',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    requests.post(url + "/channel/addowner/v1", json = {
        'token': token2,
        'channel_id' : ch_id,
        'u_id': u_id
    })

    response = requests.post(url + "/channel/removeowner/v1", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })
    assert response == 201

    url2 = urlencode({"token": token2, "channel_id": ch_id})

    channel = requests.get(url + 'channel/details/v2?' + url2).json()

    assert u_id not in [user['u_id'] for user in channel['owner_members']]
