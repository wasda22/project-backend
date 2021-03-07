import time
from .data import data
from .error import InputError, AccessError
from .helper import user_exists, get_user_data, get_channel_data, channel_exists, user_is_member, user_is_owner

def channel_invite_v1(auth_user_id, channel_id, u_id):
    """Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited, the user is added to the channel immediately

    Arguments:
        auth_user_id (int) - The ID of authorised user (invitor).
        channel_id (int) - The channel ID of the channel.
        u_id (int) - The user ID of the invitee.

    Exceptions:
        InputError - Occurs when channel_id does not refer to a valid channel
        InputError - Occurs when u_id does not refer to a valid user

    Return Value:
        Returns {} (dict) on invited user.
    """    

    global data

    if not user_exists(auth_user_id):
        raise InputError(f'u_id {auth_user_id} does not refer to a valid user')

    if not user_exists(u_id):
        raise InputError(f'u_id {u_id} does not refer to a valid user')

    channel = get_channel_data(channel_id)

    if not channel:
        raise InputError(f'channel_id {channel_id} does not refer to a valid channel')
    
    if not user_is_member(channel, auth_user_id):
        raise AccessError(f'the authorised user {auth_user_id} is not already a member of the channel')

    user_data = get_user_data(u_id)
    name_first = user_data['name_first']
    name_last = user_data['name_last']
    channel['all_members'].append({'u_id' : u_id,
                                    'name_first' : name_first,
                                    'name_last' : name_last})
    return {}

def channel_details_v1(auth_user_id, channel_id):
    """Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel

    Args:
        auth_user_id (integer): ID of authorised user

        channel_id (integer): The channel ID

    Returns:
        { name, owner_members, all_members }: [description]
    """    
    # TODO: AccessError exceptoin
    
    channel = get_channel_data(channel_id)

    if not channel:
        raise InputError(f'Channel ID {channel_id} is not a valid channel')    

    if not user_is_member(channel, auth_user_id):
        raise AccessError(f'Authorised user {auth_user_id} is not a member of channel with channel_id {channel_id}')

    name = channel['name']
    owner_members = channel['owner_members']
    all_members = channel['all_members']
    return {
        'name': name,
        'owner_members': owner_members,
        'all_members': all_members,
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    """Given a Channel ID that the authorised user is part of, return up to 50 messages starting from most recent.
    It returns a new index "end" which is the value of "start + 50". If this function has returned hte least recent messages in the channel, returns -1 in "end" to indicate
    There are no more messages
    I
    Args:
        auth_user_id (int): ID of authorised user

        channel_id (int): Channel ID
        start (int): An index for the chronological order of messages

    Returns:
        { messages, start, end }: [description]
    """ 
    limit = 50

    for channel in data['channels']:
        if channel['id'] == channel_id:
            # check if start is valid
            messages = channel['messages']
            if start > len(messages):
                raise InputError(f'Start {start} is greater than the total number of messages in the channel')
            end = start + limit
            if end > len(messages):
                end = -1
            time_created = int(time.time())

            return {
                'messages': [
                    {
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': time_created,
                    }
                ],
                'start': start,
                'end': end,
            }

    raise InputError(f'Channel ID {channel_id} is not a valid channel')   

def channel_leave_v1(auth_user_id, channel_id):
    """[summary]

    Args:
        auth_user_id ([type]): [description]
        channel_id ([type]): [description]

    Returns:
        [type]: [description]
    """    
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    """ Add user as the member of channel with specified ID

    Arguments: 
        auth_user_id (int) - ID of authorised user
        channel_id (int) - ID of the channel

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid
        AccessError - Occurs when the channel is private 
        InputError - Occurs when the channel_id is invalid
        InputError - Occurs when the channel with id entered is not created
        InputError - Occurs when the channel is private and the user is not owner of it

    Return Value:
        Return nothing
    """
    global data

    # TODO: does this need to be here?
    if not user_exists(auth_user_id):
        raise AccessError('User ID is invaild')

    if not channel_exists(channel_id):
        raise InputError(f'Channel ID {channel_id} is not a valid channel')

    for user in data['users']:
        if user['id'] == auth_user_id:
            name_first = user['name_first']
            name_last = user['name_last']
            break
    
    user_dict = {
        'u_id': auth_user_id,
        'name_first': name_first,
        'name_last': name_last,
    }

    channel_data = get_channel_data(channel_id)

    if not channel_data['is_public']:
        raise AccessError(f'channel_id {channel_id} refers to a channel that is private')
    if user_is_member(channel_data, auth_user_id):
        raise InputError('The user is already in the channel')

    channel_data['all_members'].append(user_dict)

    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    """[summary]

    Args:
        auth_user_id ([type]): [description]
        channel_id ([type]): [description]
        u_id ([type]): [description]

    Returns:
        [type]: [description]
    """    
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    """[summary]

    Args:
        auth_user_id ([type]): [description]
        channel_id ([type]): [description]
        u_id ([type]): [description]

    Returns:
        [type]: [description]
    """    
    return {
    }