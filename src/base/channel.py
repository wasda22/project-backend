""" Invite, list and join channels.

This module demonstrates the inviting, listing and joining of a channel as specified by the COMP1531 Major Project specification.
"""

import time
from src.base.error import InputError, AccessError
from src.base.helper import user_exists, get_user_data, get_channel_data, channel_exists, user_is_member,\
     user_is_Dream_owner, user_is_owner, remove_from_owner_members, remove_from_all_members
from src.data.helper import get_channels, append_channel_all_members, append_channel_owner_members

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

    if not user_exists(auth_user_id):
        raise InputError(f'u_id {auth_user_id} does not refer to a valid user')

    if not user_exists(u_id):
        raise InputError(f'u_id {u_id} does not refer to a valid user')

    channel = get_channel_data(channel_id)

    if not channel:
        raise InputError(f'channel_id {channel_id} does not refer to a valid channel')
    
    if not user_is_member(channel, auth_user_id):
        raise AccessError(f'the authorised user {auth_user_id} is not already a member of the channel')

    user = get_user_data(u_id)
    append_channel_all_members(channel_id, user)
    return {}

def channel_details_v1(auth_user_id, channel_id):
    """Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel

    Arguments:
        auth_user_id (integer) - ID of authorised user
        channel_id (integer) - The channel ID

    Exceptions:
        InputError - Channel ID is not a valid channel
        AccessError - Authorised user is not a member of channel with channel_id

    Return Value:
        Returns { name, owner_members, all_members } (dict) on valid channel_id and auth_user_id
    """    
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
    Arguments:
        auth_user_id (int) - ID of authorised user
        channel_id (int) - Channel ID
        start (int) - An index for the chronological order of messages

    Exceptions:
        InputError - Channel ID is not a valid channel
        InputError - start is greater than the total number of messages in the channel
        AcessError - Authorised user is not a member of channel with channel_id

    Return Value:
        Returns { messages, start, end } (dict): [description]
    """ 
    limit = 50

    channel = get_channel_data(channel_id)
    if not channel_exists(channel_id):
        raise InputError(f'Channel ID {channel_id} is not a valid channel')   

    if not user_is_member(channel, auth_user_id):
        raise AccessError(f'Authorised user {auth_user_id} is not a member of channel with channel_id {channel_id}')

    channel = get_channel_data(channel_id)
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


def channel_leave_v1(auth_user_id, channel_id):
    """ Remove user with u_id from owner list of channel with channel_id

    Args:
        auth_user_id (should be token): [description]
        channel_id (int): id of channel

    Exceptions:
        AccessError - Occurs when the token is invalid
        AccessError - Occurs when the auth_user is not member of channel
        InputError - Occurs when the channel_id is invalid

    Returns:
        Returns {} (dict) on success
    """   
    if not user_exists(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not channel_exists(channel_id):
        raise InputError(f'channel_id {channel_id} does not refer to a valid channel')

    channel = get_channel_data(channel_id)

    if not user_is_member(channel, auth_user_id):
        raise AccessError(f'user with {auth_user_id} is not member of channel')
    
    remove_from_owner_members(channel_id, auth_user_id)
    remove_from_all_members(channel_id, auth_user_id)
    return {}

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
        Returns {} (dict) on success
    """

    if not user_exists(auth_user_id):
        raise AccessError('User ID is invaild')

    if not channel_exists(channel_id):
        raise InputError(f'Channel ID {channel_id} is not a valid channel')

    channel_data = get_channel_data(channel_id)

    if not channel_data['is_public']:
        raise AccessError(f'channel_id {channel_id} refers to a channel that is private')
    if user_is_member(channel_data, auth_user_id):
        raise InputError('The user is already in the channel')
    
    user = get_user_data(auth_user_id)
    append_channel_all_members(channel_id, user)

    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    """ Add user with u_id as owner of channel with channel_id

    Args:
        auth_user_id (should be token): [description]
        channel_id (int): id of channel
        u_id (int): id of user being added to channel

    Exceptions:
        AccessError - Occurs when the token is invalid
        AccessError - Occurs when the auth_user is not owner of channel or owner of 'Dreams' 
        InputError - Occurs when the channel_id is invalid
        InputError - Occurs when user with u_id is already owner of channel

    Returns:
        Returns {} (dict) on success
    """    
    if not user_exists(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not channel_exists(channel_id):
        raise InputError(f'channel_id {channel_id} does not refer to a valid channel')

    channel = get_channel_data(channel_id)

    if not user_is_Dream_owner(auth_user_id) and not user_is_owner(channel, auth_user_id):
        raise AccessError(f'Auth_user with id {auth_user_id} is not owner of channel or owner of dreams')

    if user_is_owner(channel, u_id):
        raise InputError(f' user with ID {u_id} is arleady owner of channel')

    user = get_user_data(u_id)
    append_channel_owner_members(channel_id, user)
    append_channel_all_members(channel_id, user)

    return {}

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    """ Remove user with u_id from owner list of channel with channel_id

    Args:
        auth_user_id (should be token): [description]
        channel_id (int): id of channel
        u_id (int): id of user whose owner permission being removed

    Exceptions:
        AccessError - Occurs when the token is invalid
        AccessError - Occurs when the auth_user is not owner of channel or owner of 'Dreams' 
        InputError - Occurs when the channel_id is invalid
        InputError - Occurs when user with u_id is not owner of channel
        InputError - Occurs when user is the only owner in the channel

    Returns:
        Returns {} (dict) on success
    """   
    if not user_exists(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not channel_exists(channel_id):
        raise InputError(f'channel_id {channel_id} does not refer to a valid channel')

    channel = get_channel_data(channel_id)

    if not user_is_Dream_owner(auth_user_id) and not user_is_owner(channel, auth_user_id):
        raise AccessError(f'Auth_user with id {auth_user_id} is not owner of channel or owner of dreams')
    
    if not user_is_owner(channel, u_id):
        raise InputError(f'user with {u_id} is not owner of channel')
    
    if user_is_owner(channel, u_id) and len(channel['owner_members']) == 1:
        raise InputError(f'user with {u_id} is the only owner of channel')

    remove_from_owner_members(channel_id, u_id)

    return {}