from src.config import data_path
import json

def clear_data() -> None:
    """ Resets the internal data of the application to it's initial state
    
    Return Value:
        Returns None on clearing of data
    """

    # initialise keys in data
    cleared_data = {
        'users': [],
        'channels': [],
        'dms': [],
        'user_count': 0,
        'channel_count': 0,
        'message_count': 0,
        'dm_count': 0,
        'owner_count' : 0
    }

    with open(data_path, 'w') as f:
        json.dump(cleared_data, f)

def get_data() -> dict:
    """Get data stored on data storage

    Return Value:
        Returns data (dict): data stored on the data storage
    """
    with open(data_path, 'r') as f:
        data = json.load(f)

    return data

def get_user_count() -> int:
    """TODO"""
    return get_data().get('user_count')

def get_channel_count() -> int:
    """TODO"""
    return get_data().get('channel_count')

def get_message_count() -> int:
    """TODO"""
    return get_data().get('message_count')

def get_dm_count() -> int:
    """TODO"""
    return get_data().get('dm_count')

def get_owner_count() -> int:
    """TODO"""
    return get_data().get('owner_count')

def get_user_index(u_id: int) -> int:
    """Get the index of the user in users list

    Return Value:
        Returns index on all conditions
    """
    data = get_data()
    for idx in range(len(data)-1):
        if data['users'][idx]['u_id'] == u_id:
            return idx
    return -1

def get_channel_index(channel_id: int) -> int:
    """Get the index of the channel in channels list

    Return Value:
        Returns index on all conditions
    """

    data = get_data()
    for idx in range(len(data)-1):
        if data['channels'][idx]['channel_id'] == channel_id:
            return idx
    return -1

def get_message_index(channel_idx: int, message_id: int) -> int:
    """Get the index of the user in users list

    Return Value:get
        Returns index on all conditions
    """
    data = get_data()
    for idx in range(len(data)-1):
        if data['channels'][channel_idx]['messages'][idx].get('message_id') == message_id:
            return idx
    return -1

def get_dm_index(dm_id: int) -> int:
    """Get the index of the user in users list

    Return Value:get
        Returns index on all conditions
    """
    data = get_data()
    for idx in range(len(data)-1):
        if data['dms'][idx]['dm_id'] == dm_id:
            return idx
    return -1

def get_users() -> list:
    """Get list of users from data storage
    
    Return Value:
        Returns list of users on all conditions
    """
    return get_data().get('users')

def get_channels() -> list:
    """Get list of channel from data storage
    
    Return Value:
        Returns list of channels on all conditions
    """
    return get_data().get('channels')

def get_dms() -> list:
    """ Get list of dms from data storage

    Return Value:
        Returns list of dms on all conditions
    """
    return get_data().get('dms')

def store_message(message: dict, channel_id: int) -> None:
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['messages'].append(message)
    data['message_count'] += 1
    
    with open(data_path, 'w') as f:
        json.dump(data, f)


def store_user(user: dict) -> None:
    """store the data of user on data storage
    
    Arguments:
        user (dict) - a user

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data.get('users').append(user)
    data['user_count'] += 1

    with open(data_path, 'w') as f:
        json.dump(data, f)


def store_session_id(u_id: int, session_id: int) -> None:
    """Update the user's session id
    
    Arguments:
        u_id (int) - The user's id
        session_id (int) - The user's session id

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['session_list'].append(session_id)

    with open(data_path, 'w') as f:
        json.dump(data, f)


def store_message_dm(message: dict, dm_id: int) ->None:
    """store message sent to dm on the data storage

    Arguments:
        message (dict) : dictionary contains message and some information of it
        dm_id (int) : id of dm

    Return Value:
        Returns None on all conditions

    """
    data = get_data()
    idx = get_dm_index(dm_id)

    data['dms'][idx]['messages'].append(message)
    data['message_count'] += 1

    with open(data_path, 'w') as f:
        json.dump(data, f)


def update_name_first(u_id: int, name_first: str) -> None:
    """Update the user's first name
    
    Arguments:
        u_id (int) - The user's id
        name_first (str) - The user's last name

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['name_first'] = name_first

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_name_last(u_id: int, name_last: str) -> None:
    """Update the user's last name
    
    Arguments:
        u_id (int) - The user's id
        name_last (str) - The user's last name

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['name_last'] = name_last

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_email(u_id: int, email: str) -> None:
    """Update the user's email
    
    Arguments:
        u_id (int) - The user's id
        email (str) - The user's handle

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['email'] = email

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_handle_str(u_id: int, handle_str: str) -> None:
    """Update the user's handle (i.e. display name)
    
    Arguments:
        u_id (int) - The user's id
        handle_str (str) - The user's handle

    Return Value:
        Returns None if updated user's handle_str successfully
    """
    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['handle_str'] = handle_str 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def store_channel(channel: dict) -> bool:
    """Store the data of channel on data storage

    Arguments:
        channel (list): List of channel

    Return Value:
        True if the channel data stored successfully
        False if fail to store channel data
    """
    data = get_data()

    data['channels'].append(channel)
    data['channel_count'] += 1

    with open(data_path, 'w') as f:
        json.dump(data, f)

    if get_channels() == data["channels"]:
        return True
    return False

def append_channel_all_members(channel_id: int, user: dict) -> None:
    """Append a user to channel all members

    Arguments:
        channel_id (int) - id of channel
        user (dict) - the user's data

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['all_members'].append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

def append_channel_owner_members(channel_id: int, user: dict) -> None:
    """Append a user to channel owner members

    Arguments:
        channel_id (int) - id of channel
        user (dict) - the user's data

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['owner_members'].append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_owner_members(channel_id: int, owner_members: list) -> None:
    """Update the owners users of a channel

    Arguments:
        channel_id (int) - id of channel
        owner_members (list) - the users that are owners of a channel

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['owner_members'] = owner_members 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_all_members(channel_id : int, all_members: list) -> None:
    """Update the member users of a channel

    Arguments:
        channel_id (int) - id of channel
        all_members (list) - the users that are members of a channel

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['all_members'] = all_members 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_permission_id(auth_user_id : int, permission_id: int) -> None:
    """Update the permission id of a user

    Arguments:
        auth_user_id (int) - id of user
        permission_id (int) - new permission id assigned to user

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]['permission_id'] = permission_id

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_dm_list(dms: list) -> None:
    data = get_data()
    data['dms'] = dms

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_dm_users(dm_users: list, dm_id: int) -> None:
    data = get_data()
    idx = get_dm_index(dm_id)
    data['dms'][idx]['u_ids'] = dm_users

    with open(data_path, 'w') as f:
        json.dump(data, f)

def store_dm(dm: dict) -> None:
    """store the dm in storage
    
    Arguments:
        dm (dict) - a dm

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data.get('dms').append(dm)

    data['dm_count'] += 1
    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_owner_count(owner_count : int) -> None:
    """ update the count of owner 

    Arguments:
        owner_count (int) - new count for owner
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data['owner_count'] = owner_count
    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_user_count(user_count: int) -> None:
    """ update the count of user 

    Arguments:
        user_count (int) - new count for user
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data['owner_count'] = user_count
    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_removed_flag(auth_user_id : int, flag: bool) -> None:
    """ update the removed flag of user 

    Arguments:
        auth_user_id (int) - id of user
        flag (bool) - True if user being removed, False if not
    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]['removed'] = flag
    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_user_all_channel_message(auth_user_id : int, ch_id: dict, message: str) -> None:
    """ update the contents of msg sent by a user in channel

    Arguments:
        auth_user_id (int) - id of user
        ch_id (int) - id of channel
        message (str) - new message 
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_channel_index(ch_id)
    msgs = data['channels'][idx]['messages']
    i = 0
    while i < len(msgs):
        if msgs[i]['u_id'] == auth_user_id:
            msgs[i]['message'] = message
        i += 1
    data['channels'][idx]['messages'] = msgs
    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_user_all_dm_message(auth_user_id: int, dm_id: dict, message: str) -> None:
    """ update the contents of msg sent by a user in dm

    Arguments:
        auth_user_id (int) - id of user
        dm_id (int) - id of dm
        message (str) - new message 
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_dm_index(dm_id)
    msgs = data['dms'][idx]['messages']
    i = 0
    while i < len(msgs):
        if msgs[i]['u_id'] == auth_user_id:
            msgs[i]['message'] = message
        i += 1
    data['dms'][idx]['messages'] = msgs
    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_message(message_id: int, channel_id: int, remove: bool) -> None:
    """TODO"""
    data = get_data()
    channel_idx = get_channel_index(channel_id)
    message_idx = get_message_index(channel_idx, message_id)

    if remove:
        del data['channels'][channel_idx]['messages'][message_idx]
    else:
        """TODO"""
        pass

    with open(data_path, 'w') as f:
        json.dump(data, f)
