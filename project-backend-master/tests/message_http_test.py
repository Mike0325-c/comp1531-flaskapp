import pytest
import requests
import json

from src.message import message_send_v1, message_edit_v1, message_remove_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src import config
from src.config import url
from datetime import datetime, timezone

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

 
     
def test_input_error():
    user = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    user1 =  user.json()
    token = user1.get('token')
    

    channel = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })

    channel_info = channel.json()
    channel_id = channel_info.get('channel_id')

    message = requests.post(url + 'message/send/v1', json = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : 'a' * 1001

    })
    
    assert message.status_code == 400

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1').json()

@pytest.fixture
def auth_user():
    email = "jjyyl@gamil.com"
    password = "password"
    first_name = "firstname"
    last_name = "lastname"
    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']
    return token

@pytest.fixture
def member():
    email = "jjyy1@gamil.com"
    password = "password"
    first_name = "first"
    last_name = "last"
    member = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return member

@pytest.fixture
def channel_id(auth_user, member):
    channel_id = requests.post(config.url + '/channels/create/v2', json={
        'token': auth_user,
        'name': "channel1",
        'is_public': False
    }).json()['channel_id']
    
    requests.post(config.url + 'channel/join/v2', json={'token': auth_user,
                                                        'channel_id': channel_id})
    return channel_id

def test_invalid_token(clear):
    response = requests.delete(config.url + 'message/remove/v1', json={'token': "invalid_token", 'message_id': 1})
    assert response.status_code == 403

@pytest.fixture
def test_unauthorised(clear, auth_user, member, channel_id):
    channel_message_id = requests.post(config.url + '/message/send/v1',
                                       json={'token': auth_user,
                                             'channel_id': channel_id,
                                             'message': 'hello'}).json()['message_id']
  
    response1 = requests.delete(config.url + 'message/remove/v1',
                                json={'token': member['token'], 'message_id': channel_message_id})
    
    assert response1.status_code == 403
 
@pytest.fixture
def test_unauthorised_2(clear, auth_user, member, channel_id):
    channel_message_id = requests.post(config.url + '/message/send/v1',
                                       json={'token': auth_user,
                                             'channel_id': channel_id,
                                             'message': 'hello'}).json()['message_id']
  
    response1 = requests.put(config.url + 'message/edit/v1',
                                json={'token': member['token'], 'message_id': channel_message_id})
    
    assert response1.status_code == 403
  

def test_invalid_message_id(clear, auth_user):
    response = requests.delete(config.url + 'message/remove/v1',
                               json={'token': auth_user, 'message_id': 1})
    assert response.status_code == 400

def test_input_error_2():
    user = requests.post(url + 'auth/register/v2', json = user1_reg_data)   

    user1 =  user.json()
    token = user1.get('token')
    
    
    
    channel = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })

    channel_info = channel.json()
    channel_id = channel_info.get('channel_id')

    message = requests.post(url + 'message/send/v1', json = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : 'a' * 1001

    })
    
    assert message.status_code == 400

    message2 = requests.post(url + 'message/send/v1', json = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : ''

    })
    
    assert message2.status_code == 400
   
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : token,
        'channel_id' : 66674,
        'message' : 'hello' *1000

    })
    
    assert message3.status_code == 400
    

#tests for when valid input is passed into message_send which returns a valid message_id.     
def test_valid_message_send():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response3.status_code == 200
    
    response4 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response3 = requests.post(config.url + 'channels/create/v2', 
    json = {
        "token": response2_data['token'],
        "name": "Channel1",
        "is_public": True
    })
    response3_data = response3.json()
    assert response3_data['channel_id'] == 1
        
    response6 = requests.post(config.url + 'channel/join/v2', 
    json = {
        "token": response4_data['token'],
        "channel_id": response3_data['channel_id']
    })    
    assert response6.status_code == 200
    message4 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'] + 1,
        'message' : 'hello, how are you?'

    })  
    assert message4.status_code == 400
    
    message5 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?' * 1000

    })    
    assert message5.status_code == 400

    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    message6 = requests.post(url + 'message/send/v1', json = {
        'token' : response4_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'

    })     
    assert message6.status_code == 403
   
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'

    }) 
    message3_data = message3.json()
    assert message3_data['message_id'] == 1   
    assert message3.status_code == 200

#tests for when valid input is passed into message_edit which returns a valid message_id.     
def test_valid_message_edit():
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
    
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'

    }) 
    message3_data = message3.json()
    assert message3_data['message_id'] == 1   
    assert message3.status_code == 200 
    
    message4 = requests.put(url + 'message/edit/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'],
        'message' : 'sorry sent mistyped message'

    }) 
    assert message4.status_code == 200
    
    message6 = requests.put(url + 'message/edit/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'],
        'message' : 'sorry sent mistyped message' * 1000

    }) 
    assert message6.status_code == 400
    
    message7 = requests.put(url + 'message/edit/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'] + 1,
        'message' : 'sorry sent mistyped message'

    }) 
    assert message7.status_code == 400
    
    message8 = requests.delete(url + 'message/remove/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'] + 1,
        'message' : 'sorry sent mistyped message'

    }) 
    assert message8.status_code == 400
    
    message5 = requests.delete(url + 'message/remove/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id']
    }) 
    assert message5.status_code == 200     



def test_message_sendlater():
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

    message = 'a' * 10000
    timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    status_code = requests.post(config.url + 'message/sendlater/v1', json={
        'token': response2_data['token'],
        'channel_id': response3_data['channel_id'],
        'message': message,
        'time_sent': timestamp
    }).status_code
    assert status_code == 400
    
    message1 = requests.post(config.url + 'message/sendlater/v1', 
    json={
        'token': response2_data['token'],
        'channel_id': response3_data['channel_id'],
        'message': 'hello',
        'time_sent': timestamp,
    })
    message1_data = message1.json()
    assert message1_data['message_id'] == 1
    assert message1.status_code == 200
    
    message2 = requests.post(config.url + 'message/sendlater/v1', 
    json={
        'token': response2_data['token'],
        'channel_id': response3_data['channel_id'],
        'message': 'hello2',
        'time_sent': timestamp - 3.0,
    })
    assert message2.status_code == 400
    
    message3 = requests.post(config.url + 'message/sendlater/v1', 
    json={
        'token': response2_data['token'],
        'channel_id': response3_data['channel_id'] + 5,
        'message': 'hello2',
        'time_sent': timestamp,
    })
       
    assert message3.status_code == 400
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
   
    message4 = requests.post(config.url + 'message/sendlater/v1', 
    json={
    'token': response4_data['token'],
        'channel_id': response3_data['channel_id'] ,
        'message': 'hello3',
        'time_sent': timestamp,
    })

    assert message4.status_code == 403

def test_message_react():
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
    
   
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'

    }) 
    message3_data = message3.json()   
    assert message3.status_code == 200 
    
    message4 = requests.post(url + 'message/react/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'],    
        'react_id' : 0
    }) 
    assert message4.status_code == 400
    
    message5 = requests.post(url + 'message/react/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'] + 5,    
		'react_id' : 1
    }) 
    assert message5.status_code == 400
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)

    assert response4.status_code == 200
        
    requests.post(config.url + 'message/react/v1',
                 json={'token': response2_data['token'], 'message_id': message3_data['message_id'], 'react_id': 1}) 
    channel_status_code = requests.post(config.url + 'message/react/v1',
                 json={'token': response2_data['token'], 'message_id': message3_data['message_id'], 'react_id': 1}).status_code

    assert channel_status_code == 200
    
    requests.post(config.url + 'message/unreact/v1',
                 json={'token': response2_data['token'], 'message_id': message3_data['message_id'], 'react_id': 1}) 
    channel_status_code = requests.post(config.url + 'message/unreact/v1',
                 json={'token': response2_data['token'], 'message_id': message3_data['message_id'], 'react_id': 1}).status_code

    assert channel_status_code == 500
    channel_resp = requests.post(config.url + 'message/react/v1', json={
        'token': response2_data['token'],
        'message_id': message3_data['message_id'],
        'react_id': 1}).json()
    

    assert channel_resp == {}
  
    
def test_message_unreact():
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
    assert response3.status_code == 200
    
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'

    }) 
    message3_data = message3.json()
    assert message3_data['message_id'] == 1   
    assert message3.status_code == 200 
    
    message4 = requests.post(url + 'message/unreact/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'],    
		'react_id' : 0
    }) 
    assert message4.status_code == 400
    
    message5 = requests.post(url + 'message/unreact/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'] + 5,    
        'react_id' : 1
    }) 
    assert message5.status_code == 400
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    
    message6 = requests.post(url + 'message/unreact/v1', json = {
        'token' : response4_data['token'],
        'message_id' : message3_data['message_id'],
        'react_id' : 1
        })
    assert message6.status_code == 500

def test_message_pin():
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
    assert response3.status_code == 200
    
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'
    }) 
    message3_data = message3.json()
    assert message3_data['message_id'] == 1   
    assert message3.status_code == 200 
    
    message4 = requests.post(url + 'message/pin/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'] + 5,    
    }) 
    assert message4.status_code == 400
    
    message7 = requests.post(url + 'message/pin/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'],    
    }) 
    assert message7.status_code == 200
    
    message5 = requests.post(url + 'message/pin/v1', json = {
        'token' : 1,
        'message_id' : message3_data['message_id'],    
    }) 
    assert message5.status_code == 403
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    message6 = requests.post(url + 'message/pin/v1', json = {
        'token' : response4_data['token'],
        'message_id' : message3_data['message_id'],    
    }) 
    assert message6.status_code == 400

def test_message_unpin():
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
    assert response3.status_code == 200
    
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'
    }) 
    message3_data = message3.json()
    assert message3_data['message_id'] == 1   
    assert message3.status_code == 200 
    
    message4 = requests.post(url + 'message/unpin/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'] + 5,    
    }) 
    assert message4.status_code == 400
    
    message5 = requests.post(url + 'message/unpin/v1', json = {
        'token' : 1,
        'message_id' : message3_data['message_id'],    
    }) 
    assert message5.status_code == 403
    
    message7 = requests.post(url + 'message/unpin/v1', json = {
        'token' : response2_data['token'],
        'message_id' : message3_data['message_id'],    
    }) 
    assert message7.status_code == 400
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    
    message6 = requests.post(url + 'message/unpin/v1', json = {
        'token' : response4_data['token'],
        'message_id' : message3_data['message_id'],    
    }) 
    assert message6.status_code == 400

   
#. Tests if the message.py successfully raises errors (Dev)
def test_raise_errors_success():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response5.status_code == 200
    
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
    assert response3.status_code == 200 
    assert response3_data['channel_id'] == 1
    
    response4 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": ""
    })
    response4_data = response4.json()
    assert response4.status_code == 200 
    assert response4_data['dm_id'] == 1
    
    long_text = 'aaa' * 1001
    #Input error 1 for message/senddm/v1
    
    message3 = requests.post(url + 'message/senddm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : 4,
        'message' : 'hello, how are you?'

    }) 

    assert message3.status_code == 400 
    
    #Input error 2 for message/senddm/v1
    
    message3 = requests.post(url + 'message/senddm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : response4_data['dm_id'],
        'message' : ''

    }) 

    assert message3.status_code == 400 
    
    #Input error 3 for message/senddm/v1
    
    message3 = requests.post(url + 'message/senddm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : response4_data['dm_id'],
        'message' : long_text

    })  
    assert message3.status_code == 400 
    
    #AccessError 1 for message/senddm/v1
    
    message3 = requests.post(url + 'message/senddm/v1', json = {
        'token' : 'dd',
        'dm_id' : response4_data['dm_id'],
        'message' : 'hello, how are you?'

    }) 
  
    assert message3.status_code == 403 
    
    #AccessError 2 for message/senddm/v1
    
    message3 = requests.post(url + 'message/senddm/v1', json = {
        'token' : response5_data['token'],
        'dm_id' : response4_data['dm_id'],
        'message' : 'hello, how are you?'
    })  
    assert message3.status_code == 403 
    
    timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    future_time = timestamp + 1
    past_time = timestamp -2
    #Input error 1 for message/sendlaterdm/v1
    
    message3 = requests.post(url + 'message/sendlaterdm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : 4,
        'message' : 'hello, how are you?',
        'time_sent' : future_time

    }) 
 
    assert message3.status_code == 400 
    
    #Input error 2 for message/sendlaterdm/v1
    
    message3 = requests.post(url + 'message/sendlaterdm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : response4_data['dm_id'],
        'message' : 'hello',
        'time_sent' : past_time

    }) 
  
    assert message3.status_code == 400 
    
    #Input error 3 for message/sendlaterdm/v1
    
    message3 = requests.post(url + 'message/sendlaterdm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : response4_data['dm_id'],
        'message' : long_text,
        'time_sent' : future_time

    }) 
  
    assert message3.status_code == 400 
    
    #AccessError 1 for message/sendlaterdm/v1
    
    message3 = requests.post(url + 'message/sendlaterdm/v1', json = {
        'token' : 'dd',
        'dm_id' : response4_data['dm_id'],
        'message' : 'hello, how are you?',
        'time_sent' : future_time

    }) 
    
    assert message3.status_code == 403 
    
    #AccessError 2 for message/sendlaterdm/v1
    
    message3 = requests.post(url + 'message/sendlaterdm/v1', json = {
        'token' : response5_data['token'],
        'dm_id' : response4_data['dm_id'],
        'message' : 'hello, how are you?',
        'time_sent' : future_time

    }) 

    assert message3.status_code == 403 
   
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hello, how are you?'

    }) 

    assert message3.status_code == 200 
    
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'hi, are you lost?'

    }) 

    assert message3.status_code == 200
    
    message3 = requests.post(url + 'message/send/v1', json = {
        'token' : response2_data['token'],
        'channel_id' : response3_data['channel_id'],
        'message' : 'Are you ok?'

    }) 
 
    assert message3.status_code == 200  
    
    response7 = requests.get(config.url + 'search/v1', params={"token": response2_data['token'], "query_str": ''})

    assert response7.status_code == 400

    
    response7 = requests.get(config.url + 'search/v1', params={"token": response2_data['token'], "query_str": long_text})

    assert response7.status_code == 400
    
    response7 = requests.get(config.url + 'search/v1', params={"token": response2_data['token'], "query_str": 'you'})
    assert response7.status_code == 200

#Tests for when valid input is passed into message_senddm which returns a valid message_id. (Dev)
def test_valid_message_senddm():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response3.status_code == 200
    
    response4 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response5 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id']]
    
    })
    response5_data = response5.json()
    assert response5.status_code == 200
    assert response5_data['dm_id'] == 2
   
    
    message3 = requests.post(url + 'message/senddm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : response3_data['dm_id'],
        'message' : 'hello, how are you?'

    }) 
    message3_data = message3.json()
    assert message3_data['message_id'] == 1   
    assert message3.status_code == 200
    
    message3 = requests.post(url + 'message/senddm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : response3_data['dm_id'],
        'message' : 'hello'

    }) 
    message3_data = message3.json()
    assert message3_data['message_id'] == 2   
    assert message3.status_code == 200
    
    timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    future_time = timestamp + 2
    
    message3 = requests.post(url + 'message/sendlaterdm/v1', json = {
        'token' : response2_data['token'],
        'dm_id' : response3_data['dm_id'],
        'message' : "Hello World",
        'time_sent' : future_time

    }) 
    message3_data = message3.json()   
    assert message3.status_code == 200 
