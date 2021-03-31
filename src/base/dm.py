"""TODO"""

from src.base.error import InputError, AccessError
from src.base.helper import get_dm_name, get_current_user, get_dm, user_is_dm_member, get_user
from src.data.helper import get_dm_count, store_dm, get_dms, update_dm_list, get_users, update_dm_users
def dm_create(auth_user_id, u_ids):
    """TODO"""
    #using auth user in place of token
    dm_id = get_dm_count() + 1
    dm_name = get_dm_name(u_ids)
    dm = {
        'auth_user_id' : auth_user_id,
        'dm_id': dm_id,
        'dm_name': dm_name,
        'u_ids': u_ids
    }
    store_dm(dm)

    return {
        'dm_id': dm_id,
        'dm_name': dm_name
    }

def dm_list_v1(auth_user_id):
    """TODO"""
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")
    
    dm_list = []
    for dm in get_dms():
        if user_is_dm_member(dm['dm_id'], auth_user_id):
            dm_list.append(get_dm(dm['dm_id']))

    return dm_list

def dm_details_v1(auth_user_id, dm_id):
    """TODO"""
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")

    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f"auth_user {auth_user_id} is not member of dm {dm_id}")

    dm = get_dm(dm_id)
    members = []
    for u_id in dm['u_ids']:
        user = get_user(u_id)
        if user:
            members.append(user)
    
    return {'name': dm['dm_name'], 'members': members}

#def dm_leave_v1(u_id, dm_id):

def dm_invite_v1(auth_user_id, dm_id, u_id):
    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")

    #consider case where u_id is already in u_ids???
    if not get_current_user(u_id):
        raise InputError(f"u_id {auth_user_id} does not refer to a valid user")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f'user with user_id {auth_user_id} is not part of the dm')

    dm_users = get_dm(dm_id).get('u_ids')
    dm_users.append(u_id)
    update_dm_users(dm_users, dm_id)



def dm_remove_v1(auth_user_id, dm_id):
    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")
    
    if get_dm(dm_id).get('auth_user_id') != auth_user_id:
        raise AccessError(f'auth_user_id with user_id {auth_user_id} is not creator')

    dm_list = get_dms()
    dm = get_dm(dm_id)
    dm_list.remove(dm)
    update_dm_list(dm_list)

