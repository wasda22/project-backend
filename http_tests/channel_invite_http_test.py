import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.base.helper import token_to_auth_user_id
from urllib.parse import urlencode

@clear 
def test_valid_input(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    invitor_token = user1.json().get('token')
    invitee_token = user2.json().get('token')
    invitee_id = user2.json().get('auth_user_id')
    assert invitor_token
    assert invitee_token
    ch = requests.post(url + 'channels/create/v2', json = {
        'token': invitor_token,
        'name': 'channel_test1',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    requests.post(url + "/channel/invite/v2", json = {
        'token': invitor_token,
        'channel_id': ch_id,
        'u_id': invitee_id

    })
    assert response.status_code == 201

    url2 = urlencode({"token": invitee_token})
    channels = requests.get(url + 'channel/list/v2?' + url2).json()
    
    assert ch_id in [channel['channel_id'] for channel in channels['channels']]

@clear
def test_invalid_channel_id(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    invitor_token = user1.json().get('token')
    invitee_id = user2.json().get('auth_user_id')
    assert invitor_token

    ch_id = 10

    response = requests.post(url + "/channel/invite/v2", json = {
        'token': invitor_token,
        'channel_id': ch_id,
        'u_id': invitee_id

    })
    assert response.status_code == 400

@clear
def test_invalid_u_id(helper):
    user1 = helper.register_user(1)

    invitor_token = user1.json().get('token')
    assert invitor_token

    ch = requests.post(url + 'channels/create/v2', json = {
        'token': invitor_token,
        'name': 'channel_test1',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    invitee_id = 10

    response = requests.post(url + "/channel/invite/v2", json = {
        'token': invitor_token,
        'channel_id': ch_id,
        'u_id': invitee_id

    })
    assert response.status_code == 400

@clear
def test_auth_user_not_member(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    invitor_token = user2.json().get('token')
    invitee_token = user1.json().get('token')
    invitee_id = user1.json().get('auth_user_id')
    assert invitor_token
    assert invitee_token

    ch = requests.post(url + 'channels/create/v2', json = {
        'token': invitee_token,
        'name': 'channel_test1',
        'is_public': True
    })
    ch_id = ch.json().get('channel_id')

    requests.post(url + "/channel/invite/v2", json = {
        'token': invitor_token,
        'channel_id': ch_id,
        'u_id': invitee_id
    })
    assert response.status_code == 403