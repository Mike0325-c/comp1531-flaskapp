import sys
import signal
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import *
from src.other import clear_v1
from src.channels import *
from src.message import *
from src.channel import *
from src.user import *
from src.dm import *
from src.standup import *

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')
    data = dm_messages_v1(token, dm_id, start)
    return jsonify(data) 

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    channel_leave_v1(data['token'], data['channel_id'])
    return dumps({})
    
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    channel_addowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})
    
@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    channel_removeowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(channel_details_v1(token, channel_id))


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    data = channel_messages_v1(token, channel_id, start)
    return jsonify(data)  


@APP.route("/auth/register/v2", methods=['POST'])
def register():
    data = request.get_json()
    ret = auth_register_v1(data['email'], data['password'],
     data['name_first'], data['name_last'])
     
    return dumps({
        'token': ret['token'],
        'auth_user_id': ret['auth_user_id']
    })

@APP.route("/auth/login/v2", methods=['POST'])
def login():
    data = request.get_json()
    ret = auth_login_v1(data['email'], data['password'])
     
    return dumps({
        'token': ret['token'],
        'auth_user_id': ret['auth_user_id']
    })

@APP.route("/auth/logout/v1", methods=['POST'])
def logout():
    data = request.get_json()
    auth_logout_v1(data['token'])
    return dumps({})  

@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def password_request():
    data = request.get_json()
    auth_passwordreset_request_v1(data['email'])
     
    return dumps({})
    
@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def password_reset():
    data = request.get_json()
    auth_passwordreset_reset_v1(data['reset_code'], data['new_password'])
     
    return dumps({})
    
@APP.route("/channels/create/v2", methods=['POST'])
def create_channels():
    data = request.get_json()
    ret = channels_create_v1(data['token'], data['name'], data['is_public'])
     
    return dumps({
        'channel_id': ret['channel_id']
    })

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    channel_join_v1(data['token'], data['channel_id'])
    return dumps({})
    
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    channel_invite_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})

@APP.route("/channels/list/v2", methods=['GET'])
def channel_list():
    data = request.args.get('token')
    ret = channels_list_v1(data)
     
    return dumps({
        'channels': ret['channels']
    })

   
@APP.route("/channels/listall/v2", methods=['GET'])
def channel_listall():
    data = request.args.get('token')
    ret = channels_listall_v1(data)
     
    return dumps({
        'channels': ret['channels']
    })   
    
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    data = request.args.get('token')
    ret = users_all_v1(data)
     
    return dumps({
        'users': ret['users']
    })
    
@APP.route("/user/profile/v1", methods=['GET'])
def user_profile():
    data = request.args.to_dict()
    ret = user_profile_v1(data['token'], data['u_id'])
     
    return dumps({
        'user': ret['user']
    })
    
@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname():
    data = request.get_json()
    user_profile_setname_v1(data['token'], data['name_first'], data['name_last'])
    
    return dumps({})
  
@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail():
    data = request.get_json()
    user_profile_setemail_v1(data['token'], data['email'])
    
    return dumps({})
    
@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    data = request.get_json()
    user_profile_sethandle_v1(data['token'], data['handle_str'])
    
    return dumps({})
    
@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_upload():
    data = request.get_json()
    user_profile_uploadphoto_v1(data['token'], data['img_url'], data['x_start'], data['y_start'], data['x_end'], data['y_end'])
     
    return dumps({})

@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    data = request.get_json()
    ret = dm_create_v1(data['token'], data['u_ids'])
    return dumps({'dm_id': ret['dm_id']})
    


@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    data = request.args.get('token')
    ret = dm_list_v1(data)
     
    return dumps({
        'dms': ret['dms'],
    })

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    data = request.args.get('token')
    data2 = request.args.get('dm_id')
    ret = dm_details_v1(data, data2)
     
    return dumps({
        'name': ret['name'],
        'members': ret['members']
    })

@APP.route("/dm/remove/v1", methods=['DELETE'])
def remove():
    data = request.args.get('token')
    data_2 = request.args.get('dm_id')
    dm_remove_v1(data, data_2)
    return dumps({})
    
@APP.route("/dm/leave/v1", methods=['POST'])
def leave():
    data = request.get_json()
    dm_leave_v1(data['token'], data['dm_id'])
    return dumps({})

@APP.route('/message/send/v1', methods=['POST'])
def messages_send():
    data = request.get_json()
    message_id = message_send_v1(
        data['token'], data['channel_id'], data['message'])
    return jsonify(message_id)

@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    data = request.get_json()
    message_edit_v1(data['token'], data['message_id'], data['message'])
    return jsonify({})

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    data = request.get_json()
    remove = message_remove_v1(data['token'], data['message_id'])
    return jsonify(remove)    
    
@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    data = request.get_json()
    message_react_v1(data['token'], data['message_id'], data['react_id'])
    return jsonify({})

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    data = request.get_json()
    message_unreact_v1(data['token'], data['message_id'], data['react_id'])
    return jsonify({})

@APP.route("/message/pin/v1", methods=["POST"])
def message_pin():
    data = request.get_json()
    message_pin_v1(data['token'], data['message_id'])
    return jsonify({})

@APP.route("/message/unpin/v1", methods=["POST"])
def message_unpin():
    data = request.get_json()
    message_unpin_v1(data['token'], data['message_id'])   
    return jsonify({})

@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    data = request.get_json()
    ret = message_sendlater_v1(data['token'], data['channel_id'], data['message'], data['time_sent'])
    return jsonify(ret)
    
@APP.route('/message/senddm/v1', methods=['POST'])
def messages_senddm():
    data = request.get_json()
    message_id = message_senddm_v1(
        data['token'], data['dm_id'], data['message'])
    return jsonify(message_id)

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    data = request.get_json()
    ret = message_sendlaterdm_v1(data['token'], data['dm_id'], data['message'], data['time_sent'])
    return jsonify(ret)

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1() 
    return dumps({})
    
@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    data = request.get_json()
    ret = standup_start_v1(data['token'], data['channel_id'], data['length'])
     
    return dumps({
        'time_finish': ret['time_finish']
    })
    
@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    data = request.get_json()
    standup_send_v1(data['token'], data['channel_id'], data['message'])
     
    return dumps({})
    
@APP.route("/standup/active/v1", methods=['GET'])
def standup_active():
    data = request.args.get('token')
    data2 = request.args.get('channel_id')
    #ret = standup_active_v1(data, data2)
    return dumps(standup_active_v1(data, data2))
    
@APP.route("/search/v1", methods=['GET'])
def search():
    data = request.args.get('token')
    data2 = request.args.get('query_str')
    return dumps(search_v1(data, data2))

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
