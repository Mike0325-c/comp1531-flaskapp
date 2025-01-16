import pytest
import requests
import json

from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src import config

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

#1. Tests if the channels_create_v1 successfully creates a channel 
def test_channel_create_successful():
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
        "is_public": False
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1

#2. Tests if the channels_create_v1 successfully creates multiple channels 
def test_channel_create_two_successful():
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
        "is_public": False
    
    })
    
    response4 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel2",
        "is_public": True
    
    })
    
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1
    
    response4_data = response4.json()
    assert response4.status_code == 200
    assert response4_data['channel_id'] == 2


#3. Tests if it raises InputError when provided an empty channel name.
def test_channel_create_empty_name():
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
        "name": "",
        "is_public": True
    
    })

    assert response3.status_code == 400



#4. Tests if it raises InputError when provided a long channel name.
def test_channel_create_too_long_name():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user1_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Very long channel name test",
        "is_public": True
    
    })

    assert response3.status_code == 400

'''
#5. Tests for when a user is registered, yet has not created a channel but is invited into one, therefore should have a channel listed. 
def test_channel_list_member():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200

    woody_data = auth_register_v1('sheriff.hugh@gmail.com', 'woody123#',
     'sheriff', 'woody')
    zerg_data = auth_register_v1('zerg.hugh@gmail.com', 'zerg123#', 'lord',
     'zerg')
    ch = channels_create_v1(woody_data['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(woody_data['auth_user_id'], ch, 
    zerg_data['auth_user_id'])
    assert(channels_list_v1(zerg_data['auth_user_id']) == {'channels':
     [{'channel_id': 1, 'name': 'Channel1'}]})
'''
    
#6. Tests when invalid user_id is passed in to channels_create, channels_list and channels_listall    	
def test_channel_invalid_user_id():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response_data2 = response2.json()
    assert response2.status_code == 200
    
    response = requests.post(config.url + 'auth/logout/v1', 
    json = { "token": response_data2['token']})
    assert response.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response_data2['token'],
        "name": "Channel1",
        "is_public": "False"
    
    })
    assert response3.status_code == 403
    
    response4 = requests.get(config.url + 'channels/list/v2', params={'token': response_data2['token']})
    assert response4.status_code == 403
    
    response5 = requests.get(config.url + 'channels/listall/v2', params={'token': response_data2['token']})
    assert response5.status_code == 403


#7. Tests for when two channels are created with one user's id, they should be listed as followed  	
def test_channel_list_two_channels():
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
        "is_public": "False"
    
    })
    assert response3.status_code == 200
    
    response4 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel2",
        "is_public": "True"
    
    })
    assert response4.status_code == 200
    
    response5 = requests.get(config.url + 'channels/list/v2', params={'token': response2_data['token']})
    response5_data = response5.json()
    assert response5.status_code == 200
    assert response5_data['channels'] == [{"channel_id": 1, "name": "Channel1"}, {"channel_id": 2, "name": "Channel2"}]


#8. Tests for when one user creates three channels of which are all listed      
def test_channel_list_private_three_channels():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user1_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Fish Channel 1",
        "is_public": "False"
    
    })
    assert response3.status_code == 200
    
    response4 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Fish Channel 2",
        "is_public": "False"
    
    })
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Fish Channel 3",
        "is_public": "False"
    
    })
    assert response5.status_code == 200
    
    response6 = requests.get(config.url + 'channels/list/v2', params={'token': response2_data['token']})
    response6_data = response6.json()
    assert response6.status_code == 200
    assert response6_data['channels'] == [{"channel_id": 1, "name": "Fish Channel 1"}, {"channel_id": 2, "name": "Fish Channel 2"}, {"channel_id": 3, "name": "Fish Channel 3"}]
     
#9. Tests for when two users create a channel each of which channel_list only lists user 1's channel     
def test_channel_list_one_channel():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user1_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response3.status_code == 200
    
    response4 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Fish Channel 1",
        "is_public": "False"
    
    })
    assert response5.status_code == 200
    
    response6 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response4_data['token'],
        "name": "Channel 2",
        "is_public": "True"
    
    })
    assert response6.status_code == 200
    
    response7 = requests.get(config.url + 'channels/list/v2', params={'token': response2_data['token']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['channels'] == [{"channel_id": 1, "name": "Fish Channel 1"}]

#10. Tests for when two users create seperate channels and another user wants to list all channels
def test_channel_list_all_three_channels():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user1_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response3.status_code == 200
    
    response4 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response5 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Fish Channel 1",
        "is_public": "False"
    
    })
    assert response5.status_code == 200
    
    response6 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response4_data['token'],
        "name": "Channel 2",
        "is_public": "True"
    
    })
    assert response6.status_code == 200
    
    response7 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response7.status_code == 200
    
    response8 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response8_data = response8.json()
    assert response8.status_code == 200
    
    response9 = requests.get(config.url + 'channels/listall/v2', params={'token': response8_data['token']})
    response9_data = response9.json()
    assert response9.status_code == 200
    assert response9_data['channels'] == [{"channel_id": 1, "name": "Fish Channel 1"}, {'channel_id': 2, 'name': 'Channel 2'}]

#11. Tests for when a registered user tries to list channels that haven't been created
def test_when_no_channels():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.get(config.url + 'channels/list/v2', params={'token': response2_data['token']})
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channels'] == []
    
    response4 = requests.get(config.url + 'channels/listall/v2', params={'token': response2_data['token']})
    response4_data = response4.json()
    assert response4.status_code == 200
    assert response4_data['channels'] == []
