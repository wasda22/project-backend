'''
import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear
def test_valid_input(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2
    u_id = user2.json().get('auth_user_id')

    response = requests.post(url + "admin/userpermission/change/v1", json ={
        'token': token1,
        'u_id': u_id,
        'permission_id': 1
    })
    assert response.status_code == 201

    ch_id = helper.create_channel(1, token1, 'big fish', True).json().get('channel_id')

    requests.post(url + "/channel/addowner/v1", json = {
        'token': token2,
        'channel_id': ch_id,
        'u_id': u_id
    })

    url2 = urlencode({"token": token1, "channel_id": ch_id})

    channel = requests.get(url + 'channel/details/v2?' + url2).json()
    assert u_id in [user['u_id'] for user in channel['owner_members']]


@clear
def test_invalid_u_id(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    u_id = user1.json().get('auth_user_id') + 20

    response = requests.post(url + "admin/userpermission/change/v1", json ={
        'token': token1,
        'u_id': u_id,
        'permission_id': 1
    })
    assert response.status_code == 400

@clear
def test_invalid_permission_id(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2
    u_id = user2.json().get('auth_user_id')

    response = requests.post(url + "admin/userpermission/change/v1", json ={
        'token': token1,
        'u_id': u_id,
        'permission_id': 10
    })
    assert response.status_code == 400

@clear
def test_auth_user_not_Dream_owner(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    u_id = user1.json().get('auth_user_id')

    response = requests.post(url + "admin/userpermission/change/v1", json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': 2
    })
    assert response.status_code == 403
'''