import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.base.helper import get_dm_name

@clear

def test_basic(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')

    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    dm_info = dm.json()
    dm_id = dm_info.get('dm_id')

    msg_senddm = requests.post(url + 'message/senddm/v1', json = {
        'token' : token,
        'dm_id' : dm_id,
        'message' : 'i hope this works'
    })

    msg_dm_info = msg_senddm.json()
    assert msg_dm_info.get('message_id') == 1



