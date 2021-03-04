import pytest
from src.channels import channels_list_v1,channels_create_v1
from src.error import InputError,AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from .helper import helper

def test_invaild_userID():
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channels_list_v1("invaild id here")
        assert 'User ID is invaild' in str(e)

def test_vaild_input(helper):
    clear_v1()
    helper.register_users(9)
    helper.create_channels(2)
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']

    channels_create_v1(user_id, "correct", True)
    channels_create_v1(user_id, "correct2", True)
    channels_create_v1(user_id, "correct3", True)

    result = channels_list_v1(user_id)['channels']
    assert len(result) == 0

def test_multiple_user_exists(helper):
    clear_v1()
    helper.register_users(5)
    helper.create_channels(5)
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']
    channels_create_v1(user_id, "correct4", True)
    channels_create_v1(user_id, "correct5", True)

    user_2 = auth_register_v1('janetsmith4@gmail.com','12345678','Janet','Smith')
    user_id_2 = user_2['auth_user_id']
    channels_create_v1(user_id_2, "correct6", True)
    channels_create_v1(user_id_2, "correct7", True)

    result = channels_list_v1(user_id)['channels']
    assert len(result) == 0

def test_no_channel_exists(helper):
    clear_v1()
    auth_user_id = 10
    assert channels_list_v1(auth_user_id) == []