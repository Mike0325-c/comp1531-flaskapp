import pytest
import requests
import json

from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src import config
from src.channels import *

user1_register_data = {
    "email": "crystaldcunha@gmail.com",
    "password": "Rocky1234",
    "name_first": "crystal",
    "name_last": "dcunha"
}

user2_register_data = {
    "email": "project1531.dummy.email@gmail.com",
    "password": "Sherlock1234",
    "name_first": "Holly",
    "name_last": "McKlin"
}

user2_login_data = {
    "email": "project1531.dummy.email@gmail.com",
    "password": "Sherlock1234"
}

user3_register_wrong_data = {
    "email": "hollymcklin@gmail.com",
    "password": "Sherlock1234",
    "name_first": "abcdefghijklmnopqrstuvqxyzabcdefghijklmnopqrstuvwxyz",
    "name_last": "McKlin"
}

user4_register_wrong_data = {
    "email": "hollymcklin@gmail.com",
    "password": "Sherlock1234",
    "name_first": "Holly",
    "name_last": ""
}

user5_register_data = {
    "email": "samehandle@gmail.com",
    "password": "Bluesky1234",
    "name_first": "Holly",
    "name_last": "McKlin"
}

user5_login_data = {
    "email": "samehandle@gmail.com",
    "password": "Bluesky1234"
}

#Tests for registering a valid user
def test_register_valid_input():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
#Tests for when a valid user is registered, they are then able login successfully   
def test_login_valid_input():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
#Tests for when 2 valid users registers and give same handle
def test_same_handle():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user5_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 2
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user5_login_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 2
    
#Tests for unregistered email being logged in
def test_login_invalid_email():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    assert response.status_code == 400
    
#Tests for password not matching the email which was registered       
def test_login_invalid_password():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = {"email": "hollymcklin@gmail.com", "password": "Sherlock1"})
    assert response.status_code == 400


#Tests for first and last name not being between 1 and 50 characters
def test_register_invalid_first_last_name():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user3_register_wrong_data)
    assert response.status_code == 400
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user4_register_wrong_data)
    assert response.status_code == 400
    

#Tests for password being less than 6 characters
def test_register_invalid_password():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = {
    "email": "skymcdonald@gmail.com",
    "password": "sky",
    "name_first": "sky",
    "name_last": "Mcdonald"
    })
    assert response.status_code == 400
    
#Tests for duplicate email being registered twice
def test_auth_register_duplicate_email():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user3_register_wrong_data)
    assert response.status_code == 400
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 400
    
#Tests for email being registered of the wrong format      
def test_register_invalid_email():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = {
    "email": "gmail",
    "password": "Bluesky1234",
    "name_first": "Tokyo",
    "name_last": "Mcdonald"
    })
    assert response.status_code == 400
    
#Tests for when a user logs out successfully, this is tested better in channels_http_test.py whereby an invalidated token is passed into a channel function
def test_auth_logout():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response_data2 = response2.json()
    assert response2.status_code == 200
    assert response_data2['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/logout/v1', 
    json = { "token": response_data2['token']})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {}
    
#Tests for when a user logs out successfully, and then tries to logout again
def test_auth_logout_twice():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response_data2 = response2.json()
    assert response2.status_code == 200
    assert response_data2['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/logout/v1', 
    json = { "token": response_data2['token']})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {}
    
    response = requests.post(config.url + 'auth/logout/v1', 
    json = { "token": response_data2['token']})
    assert response.status_code == 403

    
#Tests for when a handle is either too long, or a duplicate
def test_invalid_handle():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    invalid1_register_data = {
        "email": "crystaldcunha@gmail.com",
        "password": "Rocky1234",
        "name_first": "crystaljonathan",
        "name_last": "dcunha"
    }
    
    invalid1_login_data = {
        "email": "crystaldcunha@gmail.com",
        "password": "Rocky1234"
    }

    invalid2_register_data = {
        "email": "hollymcklin@gmail.com",
        "password": "Sherlock1234",
        "name_first": "crystaljonathan",
        "name_last": "dcunh"
    }
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = invalid1_register_data)
    assert response.status_code == 200
    
    response2 = requests.post(config.url + 'auth/login/v2', 
    json = invalid1_login_data)
    assert response2.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = invalid2_register_data)
    assert response.status_code == 200
    
#Tests for when valid users registers and calls passwordresetrequest
def test_valid_password_request():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    email_user5 = {
        "email": "project1531.dummy.email@gmail.com"
    }
    response = requests.post(config.url + 'auth/passwordreset/request/v1', 
    json = email_user5)
    assert response.status_code == 200
    
    email_user6 = {
        "email": "unregistered@gmail.com"
    }
    response = requests.post(config.url + 'auth/passwordreset/request/v1', 
    json = email_user6)
    assert response.status_code == 200 
    
    
#Tests for when valid users registers, calls passwordreset/reset with an incorrect reset_code and invalid password length
def test_invalid_password_reset():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['auth_user_id'] == 1
    
    email_user5 = {
        "reset_code": "1039HDUFHCc",
        "new_password": "Hello1234"
    }
    response = requests.post(config.url + 'auth/passwordreset/reset/v1', 
    json = email_user5)
    assert response.status_code == 400
    
    email_user6 = {
        "reset_code": "1039HDUFHCc",
        "new_password": "Hello"
    }
    response = requests.post(config.url + 'auth/passwordreset/reset/v1', 
    json = email_user6)
    assert response.status_code == 400
    
    
  
    
    
