import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_setname_v1, user_profile_sethandle_v1
from src.helper import token_to_auth_user_id

user_blueprint = Blueprint('user_blueprint', __name__)

#TODO ALL AUTHUSERIDS MUST BE CHANGED
@user_blueprint.route("/user/profile/v2", methods=['GET'])
def user_profile():
    #token
    token = request.args.get('token')

    auth_user_id = token_to_auth_user_id(token)
    u_id = request.args.get('u_id')

    user = user_profile_v1(auth_user_id, int(u_id))

    return dumps(user)

@user_blueprint.route("/user/profile/setname/v2", methods=['PUT'])
def user_profile_setname():

    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    name_first = data.get('name_first')
    name_last = data.get('name_last')

    #need to change to token
    user_profile_setname_v1(auth_user_id, name_first, name_last)

    return dumps({
    })


#NEED TO CHANGE TO TOKEN

@user_blueprint.route("/user/profile/setemail/v2", methods=['PUT'])
def user_profile_setemail():

    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    email = data.get('email')

    user_profile_setemail_v1(auth_user_id, email)
    
    return dumps({
    })

@user_blueprint.route("/user/profile/sethandle/v2", methods=['PUT'])
def user_profile_sethandle():

    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    handle_str = data.get('handle_str')

    user_profile_sethandle_v1(auth_user_id, handle_str)
    
    return dumps({
    })
