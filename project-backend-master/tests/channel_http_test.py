import pytest
import requests
import json

from src.channel import channel_invite_v1, channel_details_v1,channel_messages_v1, channel_join_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src import config
from src.config import url

user1_reg_data = {
    "email": "happybornday@gmail.com",
    "password": "Watson1234",
    "name_first": "Jane",
    "name_last": "Doe"
}

user1_log_data = {
    "email": "happybornday@gmail.com",
    "password": "Watson1234"
}

user2_reg_data = {
    "email": "hollymcklin@gmail.com",
    "password": "Sherlock1234",
    "name_first": "Holly",
    "name_last": "McKlin"
}

user2_log_data = {
    "email": "hollymcklin@gmail.com",
    "password": "Sherlock1234"
}

user3_reg_data = {
    "email": "validemailn@gmail.com",
    "password": "Jasper1234",
    "name_first": "Molly",
    "name_last": "Surich"
}

user3_log_data = {
    "email": "validemailn@gmail.com",
    "password": "Jasper1234"
}

#2. Tests for valid channel_id which doesn't match one returned when creating channel
def test_channel_invite_valid_channel_id():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response4_data['auth_user_id']
    })
    
    assert response5.status_code == 200

#3. Tests for invalid channel_id which doesn't match one returned when creating channel
def test_channel_invite_invaild_channel_id():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": 989,
        "u_id": response4_data['token']
    })
    
    assert response5.status_code == 400


#4. Tests for inviting a u_id that is already a member and tests for invalid channel_id for channel_invite
def test_channel_invite_already_member_invalid():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": 989,
        "u_id": 9090
    })
    
    response5 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": 989,
        "u_id": "Invalid u_id"
    })
    
    assert response4.status_code == 400
    assert response5.status_code == 400
    
    response5 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response2_data['auth_user_id']
    })
    assert response5.status_code == 400

#5. Tests for inviting a member which is already a member of the channel
def test_channel_invite_already_member():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": "Channel1",
        "u_id": response2_data['token']
    })
    assert response4.status_code == 400

#6. Tests for when a non_member tries to invite a user to the channel
def test_channel_invite_is_not_member():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response6 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response4_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response5_data['auth_user_id']
    })
    assert response6.status_code == 403


#7. Tests for when invalid channel is passed into channel_join
def test_channel_join_v1_invaild_channel():	
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": 87878
    })
    assert response4.status_code == 400



#8. Tests for when a user that is already part of the channel tries to join it again
def test_channel_join_v1_already_member():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response6 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response5_data['token'],
        "name": "Channel2",
        "is_public": True
    })
    response6_data = response6.json()
    assert response6_data['channel_id'] == 2
    
    response7 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id']
    })
    
    response8 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response6_data['channel_id']
    })
    
    assert response7.status_code == 400
    assert response8.status_code == 400


#9. Tests for when a non-member tries to join a private channel
def test_channel_join_v1_is_not_member():	
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response6 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    
    assert response6.status_code == 403


#10. Tests for when a global owner tries to join a channel		    
def test_channel_join_v1_is_global_owner():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response5_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response6 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id']
    })
    
    assert response6.status_code == 200

#valid user passed into channel_details
def test_channel_details_v2_valid():	
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    assert response3.status_code == 200
    
    response6 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id']
    })
    
    assert response6.status_code == 200


# invalid user passed into channel_details
def test_channel_details_v2_is_not_member():	
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response6 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    
    assert response6.status_code == 403

#Tests for an invalid session_id for features in channel.py
def test_invalid_session_id_channel():	
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response_data2 = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/logout/v1', 
    json = {"token": response_data2['token']})
    assert response4.status_code == 200
    
    response6 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response_data2['token'],
        "channel_id": 1
    })
    assert response6.status_code == 403
    
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': response_data2['token'],
        'channel_id': 1,
        'start': 0
    })
    status_code = resp.status_code
    assert status_code == 403
    
    response5 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response_data2['token'],
        "channel_id": 1,
        "u_id": response_data2['auth_user_id']
    })
    assert response5.status_code == 403
    
    response6 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response_data2['token'],
        "channel_id": 1
    })
    assert response6.status_code == 403  
    
    response6 = requests.post(config.url + 'channel/leave/v1', 
    json = {
        "token": response_data2['token'],
        "channel_id": 1
    })
    assert response6.status_code == 403   
    
    response6 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response_data2['token'],
        "channel_id": 1,
        "u_id": 1
    })
    assert response6.status_code == 403 
    
    response6 = requests.post(config.url + 'channel/removeowner/v1', 
    json = {
        "token": response_data2['token'],
        "channel_id": 1,
        "u_id": 1
    })
    assert response6.status_code == 403   

#Tests for an invalid token for features in channel.py
def test_invalid_token_channel():	
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response_data2 = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/logout/v1', 
    json = {"token": response_data2['token']})
    assert response4.status_code == 200
    
    response6 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": None,
        "channel_id": 1
    })
    assert response6.status_code == 403
    
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': None,
        'channel_id': 1,
        'start': 0
    })
    status_code = resp.status_code
    assert status_code == 403
    
    response5 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": None,
        "channel_id": 1,
        "u_id": response_data2['auth_user_id']
    })
    assert response5.status_code == 403
    
    response6 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": None,
        "channel_id": 1
    })
    assert response6.status_code == 403    

#invalid channel_id passed into channel_details
def test_channel_details_v2_invaild_channel():	
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response2_data['token'],
        "channel_id": 666
    })
    assert response4.status_code == 400

#pytest fixture for clear feature    
@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

#pytest fixture for generating a token
@pytest.fixture
def token():
    email = "email@gamil.com"
    password = "password3"
    first_name = "firstname"
    last_name = "lastname"
    auth_resp = requests.post(config.url + '/auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    token = auth_resp['token']
    return token

#pytest fixture for creating a channel_id
@pytest.fixture
def channel_id(token):
    resp = requests.post(config.url + '/channels/create/v2', json={
        'token': token,
        'name': "channelName1",
        'is_public': True
    }).json()

    channel_id = resp['channel_id']
    return channel_id

#tests for invalid channel_id in channel_messages
def test_invalid_channel_id(clear, token, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': 0,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 400

#tests for valid channel_id in channel_messages
def test_valid_messages():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    assert response3.status_code == 200
    
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': response2_data['token'],
        'channel_id': response3_data['channel_id'],
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 200


#tests for invalid user passed into channel_messages
def test_user_not_in_channel(clear, channel_id):
    not_member_token = requests.post(config.url + 'auth/register/v2', 
    json=user3_reg_data)
    not_member_token = not_member_token.json()['token']

    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': not_member_token,
        'channel_id': channel_id,
        'start': 0
    })
    status_code = resp.status_code
    assert status_code == 403

#tests for invalid start code passed into channel_messages
def test_invalid_start(clear, token, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 51
    })

    status_code = resp.status_code
    assert status_code == 400
    
#Tests for a valid user leaving a channel
def test_valid_user_channel_leave_v1():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response7 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response7 = requests.post(config.url + 'channel/leave/v1', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response8 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id']
    })
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data == {
        'all_members': [{'email': 'validemailn@gmail.com', 'handle_str': 'mollysurich', 'name_first': 'Molly', 'name_last': 'Surich', 'u_id': 1, 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}], 
        'is_public': True, 
        'name': 'Channel1', 
        'owner_members': [{'email': 'validemailn@gmail.com', 'handle_str': 'mollysurich', 'name_first': 'Molly', 'name_last': 'Surich', 'u_id': 1, 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}],
    }
    
#Tests for a valid owner leaving a channel
def test_owner_channel_leave_v1():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response7 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response7 = requests.post(config.url + 'channel/leave/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response8 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['all_members'] == [{'email':'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'u_id': 2, 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    assert response8_data['owner_members'] == []
 
#Tests for an owner being added to a channel successfully
def test_valid_channel_addowner_v1():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response7 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response7 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response5_data['auth_user_id']
    })
    assert response7.status_code == 200
    
    
    response8 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['owner_members'] == [
        {'email': 'validemailn@gmail.com',
        'handle_str': 'mollysurich',
        'name_first': 'Molly', 'name_last': 'Surich',
        'profile_img_url': 'http://localhost:8080/static/generic.jpg',
        'u_id': 1}, {'email': 'hollymcklin@gmail.com',
        'handle_str': 'hollymcklin', 'name_first': 'Holly', 
        'name_last': 'McKlin',
        'profile_img_url': 'http://localhost:8080/static/generic.jpg',
        'u_id': 2}]   
    
#Tests for a valid owner removing another owner from a channel
def test_valid_channel_remove_v1():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response7 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response7 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response5_data['auth_user_id']
    })
    assert response7.status_code == 200
    
    response8 = requests.post(config.url + 'channel/removeowner/v1', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response2_data['auth_user_id']
    })
    assert response8.status_code == 200
    
    response8 = requests.get(config.url + 'channel/details/v2', 
    params = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['owner_members'] == [{'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'u_id': 2, 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}] 
    
#Tests for an invalid channel_id in channel_leave, channel_addowner and channel_removeowner
def test_invalid_channel_id_leave_addowner_removeowner():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response6 = requests.post(config.url + 'channel/leave/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": 1
    })
    assert response6.status_code == 400
    
    response7 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": 1,
        "u_id": response5_data['auth_user_id']
    })
    assert response7.status_code == 400
    
    response8 = requests.post(config.url + 'channel/removeowner/v1', 
    json = {
        "token": response5_data['token'],
        "channel_id": 1,
        "u_id": response2_data['auth_user_id']
    })
    assert response8.status_code == 400
   
#Tests for an invalid auth_user_id in channel_leave whereby the user is not a member of the channel given
def test_channel_leave_not_member():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response6 = requests.post(config.url + 'channel/leave/v1', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response6.status_code == 403

#Tests for an invalid u_id in channel_addowner and channel_removeowner
def test_invalid_u_id_addowner_removeowner():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response6 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": 5
    })
    assert response6.status_code == 400
    
    response6 = requests.post(config.url + 'channel/removeowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": 5
    })
    assert response6.status_code == 400

#Tests for when a u_id passed into channel_addowner is already an owner
def test_u_id_already_owner_addowner():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response6 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response2_data['auth_user_id']
    })
    assert response6.status_code == 400 

#Tests for when a u_id passed into channel_removeowner is not an owner so can't be removed
def test_u_id_not_owner_removeowner():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user1_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response7 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response6 = requests.post(config.url + 'channel/removeowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response5_data['auth_user_id']
    })
    assert response6.status_code == 400 
    
#Tests for when a u_id passed into channel_removeowner is the only owner so can't be removed
def test_only_owner_removeowner():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response6 = requests.post(config.url + 'channel/removeowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response2_data['auth_user_id']
    })
    assert response6.status_code == 400 
    
#Tests for when a token passed into channel_addowner and channel_removeowner does not have owner permissions
def test_no_owner_permissions():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'auth/login/v2', 
    json = user1_log_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response7 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id']
    })
    assert response7.status_code == 200
    
    response6 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response5_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response5_data['auth_user_id']
    })
    assert response6.status_code == 403 
    
    response6 = requests.post(config.url + 'channel/addowner/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response5_data['auth_user_id']
    })
    assert response6.status_code == 200
    
    response9 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response9.status_code == 200
    
    response19 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response19_data = response19.json()
    assert response19.status_code == 200
    
    response6 = requests.post(config.url + 'channel/removeowner/v1', 
    json = {
        "token": response19_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response2_data['auth_user_id']
    })
    assert response6.status_code == 403 
    
#Tests for global owner being passed into channel_invite 
def test_channel_invite_global_owner():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response9 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response9.status_code == 200
    
    response8 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response8_data = response8.json()
    assert response8.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response8_data['token'],
        "name": "Channel1",
        "is_public": False
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
    
    response5 = requests.post(config.url + 'channel/invite/v2', 
    json = {
        "token": response8_data['token'],
        "channel_id": response3_data['channel_id'],
        "u_id": response2_data['auth_user_id']
    })
    assert response5.status_code == 200
