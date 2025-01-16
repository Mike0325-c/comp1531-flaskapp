import pytest
import requests
import json

from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.dm import *
from src.auth import *
from src.error import InputError, AccessError
from src import config
from src.other import clear_v1

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
    
#1. Tests if the dm_create_v1 successfully creates a channel. 
def test_dm_create_successful():
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
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    
#2. Tests if the dm_list_v1 successfully list the Dms the member is part of 
def test_dm_list_successful():
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
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    
    response9 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response5_data['auth_user_id']]
    
    })
    
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1

    response9_data = response9.json()
    assert response9.status_code == 200
    assert response9_data['dm_id'] == 2
    
    response6 = requests.get(config.url + 'dm/list/v1', params={"token": response5_data['token']})
    response6_data = response6.json()
    assert response6.status_code == 200
    assert response6_data['dms'] == [{'dm_id': 1, 'name': 'HollyMcKlin, JaneDoe, MollySurich'}, {'dm_id': 2, 'name': 'HollyMcKlin, MollySurich'}]
    
    response7 = requests.get(config.url + 'dm/list/v1', params={"token": response4_data['token']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['dms'] == [{'dm_id': 1, 'name': 'HollyMcKlin, JaneDoe, MollySurich'}]
    
    
    response8 = requests.get(config.url + 'dm/list/v1', params={"token": response2_data['token']})
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['dms'] == [{'dm_id': 1, 'name': 'HollyMcKlin, JaneDoe, MollySurich'},{'dm_id': 2, 'name': 'HollyMcKlin, MollySurich'}]
    
    
    
    
#3. Tests if the dm_details_v1 successfully returns basic info of DMs 
def test_dm_details_successful():
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
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id":response3_data['dm_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['name'] == 'HollyMcKlin, JaneDoe, MollySurich'
    assert response7_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 2, 'email': 'happybornday@gmail.com', 'handle_str': 'janedoe', 'name_first': 'Jane', 'name_last': 'Doe', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 3,'email': 'validemailn@gmail.com','handle_str': 'mollysurich', 'name_first': 'Molly', 'name_last': 'Surich', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    
    
#4. Tests if the dm_remove_v1 successfully removes a channel 
def test_dm_remove_successful():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_reg_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response6 = requests.delete(config.url + 'dm/remove/v1', params={'token': response2_data['token'], 'dm_id': response3_data['dm_id']})
    assert response6.status_code == 200
    
    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id":response3_data['dm_id']})
    response7_data = response7.json()
    assert response7.status_code == 400
    assert response7_data['name'] == 'System Error'

    
#5. Tests if the dm_leave_v1 successfully removes a user from the member's list of the DM. 
def test_dm_leave_successful():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_reg_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response5_data['token'], "dm_id":response3_data['dm_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['name'] == 'HollyMcKlin, JaneDoe, MollySurich'
    assert response7_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 2, 'email': 'happybornday@gmail.com', 'handle_str': 'janedoe', 'name_first': 'Jane', 'name_last': 'Doe', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 3,'email': 'validemailn@gmail.com','handle_str': 'mollysurich', 'name_first': 'Molly', 'name_last': 'Surich', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    response6 = requests.post(config.url + 'dm/leave/v1', 
    json = {
        "token": response5_data['token'],
        "dm_id": response3_data['dm_id']
    })
    assert response6.status_code == 200
    
    response8 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id":response3_data['dm_id']})
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['name'] == 'HollyMcKlin, JaneDoe, MollySurich'
    assert response8_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 2, 'email': 'happybornday@gmail.com', 'handle_str': 'janedoe', 'name_first': 'Jane', 'name_last': 'Doe', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    
#6. Tests if the dm_create_v1 successfully returns correct output for two DMs. 
def test_dm_create_two_successful():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_reg_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response9 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response5_data['auth_user_id']]
    
    })
    response9_data = response9.json()
    assert response9.status_code == 200
    assert response9_data['dm_id'] == 2
    
    resp = requests.get(config.url + '/dm/messages/v1', params={
        'token': None,
        'dm_id': 1,
        'start': 0
    })
    status_code = resp.status_code
    assert status_code == 403
    
    
    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response5_data['token'], "dm_id":response3_data['dm_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['name'] == 'HollyMcKlin, JaneDoe, MollySurich'
    assert response7_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 2, 'email': 'happybornday@gmail.com', 'handle_str': 'janedoe', 'name_first': 'Jane', 'name_last': 'Doe', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 3,'email': 'validemailn@gmail.com','handle_str': 'mollysurich', 'name_first': 'Molly', 'name_last': 'Surich', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    response8 = requests.get(config.url + 'dm/details/v1', params={"token": response5_data['token'], "dm_id":response9_data['dm_id']})
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['name'] == 'HollyMcKlin, MollySurich'
    assert response8_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 3,'email': 'validemailn@gmail.com','handle_str': 'mollysurich', 'name_first': 'Molly', 'name_last': 'Surich', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]

#7. Tests if the dm_create_v1 successfully creats the DM when there is empty u_ids 
def test_dm_create_empty_u_ids():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": []
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id":response3_data['dm_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['name'] == 'HollyMcKlin'
    assert response7_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
#8. Tests if the dm_create_v1 successfully raises errors 
def test_dm_create_error_check():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    response1_data = response1.json()
    assert response1.status_code == 200
    
    response20 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response20_data = response20.json()
    assert response20.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response6 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    assert response6.status_code == 200
    
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response20_data['auth_user_id']]
    
    })
    assert response3.status_code == 200
    
    response4 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": "",
        "u_ids": [response1_data['token']]
    
    })
    assert response4.status_code == 403
    
    response5 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [100]
    
    })
    assert response5.status_code == 400
    
    response7 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [11, 9, 10]
    
    })
    assert response7.status_code == 400
    
    
    
#9. Tests if the dm_list_v1 successfully raises erros 
def test_dm_list_error_check():
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
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })

    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1

    
    response6 = requests.get(config.url + 'dm/list/v1', params={"token": response5_data['token']})
    response6_data = response6.json()
    assert response6.status_code == 200
    assert response6_data['dms'] == [{'dm_id': 1, 'name': 'HollyMcKlin, JaneDoe, MollySurich'}]
    
    response7 = requests.get(config.url + 'dm/list/v1', params={"token": "randomtoken"})
    assert response7.status_code == 403

#10. Tests if the dm_leave_v1 successfully raises erros 
def test_dm_leave_error_check():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_reg_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response5_data['token'], "dm_id":response3_data['dm_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['name'] == 'HollyMcKlin, JaneDoe, MollySurich'
    assert response7_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 2, 'email': 'happybornday@gmail.com', 'handle_str': 'janedoe', 'name_first': 'Jane', 'name_last': 'Doe', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 3,'email': 'validemailn@gmail.com','handle_str': 'mollysurich', 'name_first': 'Molly', 'name_last': 'Surich', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    response12 = requests.get(config.url + 'dm/list/v1', params={"token": response5_data['token']})
    assert response12.status_code == 200
    
    response6 = requests.post(config.url + 'dm/leave/v1', 
    json = {
        "token": response5_data['token'],
        "dm_id": response3_data['dm_id']
    })
    assert response6.status_code == 200
    
    response8 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id":response3_data['dm_id']})
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['name'] == 'HollyMcKlin, JaneDoe, MollySurich'
    assert response8_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {'u_id': 2, 'email': 'happybornday@gmail.com', 'handle_str': 'janedoe', 'name_first': 'Jane', 'name_last': 'Doe', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    response11 = requests.get(config.url + 'dm/list/v1', params={"token": response5_data['token']})
    assert response11.status_code == 403
    
    response9 = requests.post(config.url + 'dm/leave/v1', 
    json = {
        "token": response5_data['token'],
        "dm_id": 3
    })
    assert response9.status_code == 400
    
    response10 = requests.post(config.url + 'dm/leave/v1', 
    json = {
        "token": "dvlg",
        "dm_id": response3_data['dm_id']
    })
    assert response10.status_code == 403
    
    response13 = requests.post(config.url + 'dm/leave/v1', 
    json = {
        "token": response5_data['token'],
        "dm_id": response3_data['dm_id']
    })
    assert response13.status_code == 403
    
#11. Tests if the dm_remove_v1 successfully raises errors 
def test_dm_remove_check():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_reg_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response4 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response4_data = response4.json()
    assert response1.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id'], response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    
    response8 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response4_data['auth_user_id']]
    
    })
    response8_data = response8.json()
    assert response8.status_code == 200
    assert response8_data['dm_id'] == 2
    
    response6 = requests.delete(config.url + 'dm/remove/v1', params={'token': response2_data['token'], 'dm_id': 7})
    assert response6.status_code == 400
    
    response15 = requests.delete(config.url + 'dm/remove/v1', params={'token': "sds", 'dm_id': response3_data['dm_id']})
    assert response15.status_code == 403
    
    response16 = requests.delete(config.url + 'dm/remove/v1', params={'token': response5_data['token'], 'dm_id': response8_data['dm_id']})
    assert response16.status_code == 403

#12. Tests if the dm_create_v1 successfully raises errors for all the functions.
def test_dm_create_session_error():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response5 = requests.post(config.url + 'auth/register/v2', 
    json = user1_reg_data)
    response5_data = response5.json()
    assert response1.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response5_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    response4 = requests.post(config.url + 'auth/logout/v1', 
    json = {"token": response2_data['token']})
    assert response4.status_code == 200
    
    response6 = requests.get(config.url + 'dm/list/v1', params={"token": response2_data['token']})
    assert response6.status_code == 403
    
    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id":response3_data['dm_id']})
    assert response7.status_code == 403
    
    resp = requests.get(config.url + '/dm/messages/v1', params={
        'token': response2_data['token'],
        'dm_id': 1,
        'start': 0
    })
    status_code = resp.status_code
    assert status_code == 403
    
    response8 = requests.delete(config.url + 'dm/remove/v1', params={'token': response2_data['token'], 'dm_id': response3_data['dm_id']})
    assert response8.status_code == 403
    
    response9 = requests.post(config.url + 'dm/leave/v1', 
    json = {
        "token": response2_data['token'],
        "dm_id": response3_data['dm_id']
    })
    assert response9.status_code == 403
    
    response10 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response5_data['auth_user_id']]
    
    })
    assert response10.status_code == 403
    
    
#13. Tests if the dm_detail_v1 successfully raises errors 
def test_dm_detail_error_check():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    assert response1.status_code == 200
    
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response10 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    response10_data = response10.json()
    assert response10.status_code == 200
    
    
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": []
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1

    response7 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id": response3_data['dm_id']})
    response7_data = response7.json()
    assert response7.status_code == 200
    assert response7_data['name'] == 'HollyMcKlin'
    assert response7_data['members'] == [{'u_id': 1, 'email': 'hollymcklin@gmail.com', 'handle_str': 'hollymcklin', 'name_first': 'Holly', 'name_last': 'McKlin', 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    response8 = requests.get(config.url + 'dm/details/v1', params={"token": response2_data['token'], "dm_id": 5})
    assert response8.status_code == 400
    
    response9 = requests.get(config.url + 'dm/details/v1', params={"token": response10_data['token'], "dm_id": response3_data['dm_id']})
    assert response9.status_code == 403
    
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
def dm_id(token):
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": token,
        "u_ids": []
    
    })
    response3_data = response3.json()
    dm_id = response3_data['dm_id']
    return dm_id
    
#14 tests for invalid dm_id in dm_messages
def test_invalid_dm_id(clear, token, dm_id):
    resp = requests.get(config.url + '/dm/messages/v1', params={
        'token': token,
        'dm_id': 0,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 400
    
    
#15. tests for valid dm_id in dm_messages
def test_valid_dm_messages():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response1 = requests.post(config.url + 'auth/register/v2', 
    json = user3_reg_data)
    assert response1.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user3_log_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    
    response10 = requests.post(config.url + 'auth/register/v2', 
    json = user2_reg_data)
    response10_data = response10.json()
    assert response10.status_code == 200
    
    response3 = requests.post(config.url + 'dm/create/v1', 
    json = {
        "token": response2_data['token'],
        "u_ids": [response10_data['auth_user_id']]
    
    })
    response3_data = response3.json()
    assert response3.status_code == 200
    assert response3_data['dm_id'] == 1
    
    resp = requests.get(config.url + '/dm/messages/v1', params={
        'token': response2_data['token'],
        'dm_id': response3_data['dm_id'],
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 200


#16. tests for invalid user passed into dm_messages
def test_user_not_in_dm(clear, dm_id):
    not_member_token = requests.post(config.url + 'auth/register/v2', 
    json=user3_reg_data)
    not_member_token = not_member_token.json()['token']

    resp = requests.get(config.url + '/dm/messages/v1', params={
        'token': not_member_token,
        'dm_id': dm_id,
        'start': 0
    })
    status_code = resp.status_code
    assert status_code == 403

#17. tests for invalid start code passed into dm_messages
def test_invalid_dm_tart(clear, token, dm_id):
    resp = requests.get(config.url + '/dm/messages/v1', params={
        'token': token,
        'dm_id': dm_id,
        'start': 51
    })

    status_code = resp.status_code
    assert status_code == 400
