import pytest
import requests
import json
import random
import string
import time
import datetime
from src.data_store import data_store
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.dm import *
from src.auth import *
from src.error import InputError, AccessError
from src import config
from src.other import clear_v1
from src.standup import *

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
    
#1. Tests if the standup_start_v1 raises error. 
def test_standup_errors_successful():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200

    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1
    
    #AccessError invalid token
    response6 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": '',
        "channel_id": response3_data['channel_id'],
        "length": 2
    })
    
    assert response6.status_code == 403
    
    #AccessError authorised member not in the channel
    response6 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response4_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": 2
    })
    
    
    assert response6.status_code == 403


    #InputError Invalid channel_id
    response7 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": 5,
        "length": 2
    })
    
    assert response7.status_code == 400
    
    #InputError already active

    response8 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": 3
    })
    
    assert response8.status_code == 200
    
    time.sleep(2)
    
    response8 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": 1
    })
    
    assert response8.status_code == 400
    
    time.sleep(2)
    
    #InputError length is negative
    response8 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": -2
    })

    assert response8.status_code == 400

#2. Tests if the standup_start_v1 successfully starts the standup 
def test_standup_start_successful():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)

    assert response5.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1

    
    response6 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": 2
    })


    assert response6.status_code == 200
    
    
#3. Tests if the standup_active_v1 raises errors 
def test_standup_active_errors():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1

    
    #AccessError authorised member not in the channel
    response7 = requests.get(config.url + 'standup/active/v1', params={"token": response5_data['token'], "channel_id": response3_data['channel_id']})
    response7_data = response7.json()
    assert response7.status_code == 403
    
    #AccessError invalid token
    response7 = requests.get(config.url + 'standup/active/v1', params={"token": 's', "channel_id": response3_data['channel_id']})
    response7_data = response7.json()
    assert response7.status_code == 403
    
     #InputError Invalid channel_id
    response7 = requests.get(config.url + 'standup/active/v1', params={"token": response2_data['token'], "channel_id": 4})
    response7_data = response7.json()
    assert response7.status_code == 400

    # Returns is_active False since there is no stand up running and time_finish = None
    response7 = requests.get(config.url + 'standup/active/v1', params={"token": response2_data['token'], "channel_id": response3_data['channel_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['is_active'] == False
    assert response7_data['time_finish'] == None
    
    #Start Standup
    response6 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": 2
    })


    assert response6.status_code == 200
    
    # Returns is_active True since there is no stand up running and time_finish
    response7 = requests.get(config.url + 'standup/active/v1', params={"token": response2_data['token'], "channel_id": response3_data['channel_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['is_active'] == True
    
    time.sleep(2)
    
    response7 = requests.get(config.url + 'standup/active/v1', params={"token": response2_data['token'], "channel_id": response3_data['channel_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['is_active'] == False
    
#3. Tests if the standup_send_v1 raises error. 
def test_standup_send_errors_successful():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": False
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1
    
    #AccessError invalid token
    response6 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": '',
        "channel_id": response3_data['channel_id'],
        "message": "Hello"
    })

    assert response6.status_code == 403
    
    #AccessError authorised member not in the channel
    response6 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": response4_data['token'],
        "channel_id": response3_data['channel_id'],
        "message": "Hi"
    })
    
    assert response6.status_code == 403


    #InputError Invalid channel_id
    response6 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": 5,
        "message": "Hello"
    })

    assert response6.status_code == 400

    
    #InputError message > 1000
    long_message = 1001 * 'a'
    response8 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "message": long_message
    })

    assert response8.status_code == 400
    
    #Start Standup
    response7 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": 2
    })

    assert response7.status_code == 200
    
    
    response6 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "message": "Message_1"
    })
    assert response6.status_code == 200
    
    time.sleep(1)
    
    response6 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "message": "Message_2"
    })

    assert response6.status_code == 200
    
    time.sleep(1)
    
    response6 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "message": "Message_3"
    })

    assert response6.status_code == 400
    
#4. Tests if the standup successfully raises session errors for all the functions.
def test_standup_start_v1_session_error():
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
    assert response3.status_code == 200
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'auth/logout/v1', 
    json = {"token": response2_data['token']})
    assert response4.status_code == 200
    
    response6 = requests.post(config.url + 'standup/send/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "message": "Hello"
    })
    assert response6.status_code == 403
    
    response7 = requests.get(config.url + 'standup/active/v1', params={"token": response2_data['token'], "channel_id": response3_data['channel_id']})

    assert response7.status_code == 403
    
    response7 = requests.post(config.url + 'standup/start/v1', 
    json = {
        "token": response2_data['token'],
        "channel_id": response3_data['channel_id'],
        "length": 1
    })
    assert response7.status_code == 403
    
