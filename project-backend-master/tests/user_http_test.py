import pytest
import requests
import json

from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src import config

user1_register_data = {
    "email": "crystaldcunha@gmail.com",
    "password": "Rocky1234",
    "name_first": "crystal",
    "name_last": "dcunha"
}

user2_register_data = {
    "email": "hollymcklin@gmail.com",
    "password": "Sherlock1234",
    "name_first": "Holly",
    "name_last": "McKlin"
}

user1_login_data = {
    "email": "crystaldcunha@gmail.com",
    "password": "Rocky1234"
}

user2_login_data = {
    "email": "hollymcklin@gmail.com",
    "password": "Sherlock1234"
}

   
#1. Tests for when two valid users register and login and then call users/all/v1 and user/profile/v1 of one user, successfully
def test_valid_input_users_all_and_profile():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    assert response.status_code == 200
    
    response4 = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response4_data = response4.json()
    assert response4.status_code == 200
    
    response5 = requests.get(config.url + 'users/all/v1', params={'token': response4_data['token']})
    response5_data = response5.json()
    assert response5.status_code == 200
    assert response5_data['users'] == [{"u_id": 1, "email": "crystaldcunha@gmail.com", "name_first": "crystal", "name_last": "dcunha", "handle_str": "crystaldcunha", 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}, {"u_id": 2, "email": "hollymcklin@gmail.com", "name_first": "Holly", "name_last": "McKlin", "handle_str": "hollymcklin", 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}]
    
    response6 = requests.get(config.url + 'user/profile/v1', params={'token': response4_data['token'], 'u_id': response4_data['auth_user_id']})
    response6_data = response6.json()
    assert response6.status_code == 200
    assert response6_data["user"] == {"u_id": 2, "email": "hollymcklin@gmail.com", "name_first": "Holly", "name_last": "McKlin", "handle_str": "hollymcklin", 'profile_img_url': 'http://localhost:8080/static/generic.jpg'}
    
#2. Tests for invalid session_id, users/all/v1, user/profile/v1, user/profile/setname/v1, user/profile/setemail/v1 and user/profile/sethandle/v1
def test_invalid_session_id():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    token = {
        "token": response_data2['token']
    }
    
    response4 = requests.post(config.url + 'auth/logout/v1', 
    json = token)
    assert response4.status_code == 200
    
    response5 = requests.get(config.url + 'users/all/v1', params={'token': response_data2['token']})
    assert response5.status_code == 403
    
    response6 = requests.get(config.url + 'user/profile/v1', params={'token': response_data2['token'], 'u_id': response_data2['auth_user_id']})
    assert response6.status_code == 403
    
    token = response_data2['token']
    
    data = {
        "token": token,
        "name_first": "ronald",
        "name_last": "mcdonald"
    }
    
    data2 = {
        "token": token,
        "email": "ronaldmcdonald@gmail.com"
    }
    
    data3 = {
        "token": token,
        "handle_str": "fastfood"
    }
    
    response3 = requests.put(config.url + 'user/profile/setname/v1', json = data)
    assert response3.status_code == 403
    
    response4 = requests.put(config.url + 'user/profile/setemail/v1', json = data2)
    assert response4.status_code == 403
    
    response5 = requests.put(config.url + 'user/profile/sethandle/v1', json = data3)
    assert response5.status_code == 403
    
    upload_info = {
        "token": response_data2['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": "0",
        "y_start": "0",
        "x_end": "100",
        "y_end": "100"
    }
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', 
    json = upload_info)
    assert response.status_code == 403
    
#3. Tests for invalid u_id in user/profile/v1
def test_invalid_u_id_in_profile():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    response6 = requests.get(config.url + 'user/profile/v1', params={'token': response_data2['token'], 'u_id': 2})
    assert response6.status_code == 400
    
#4. Tests user/profile/setname/v1, user/profile/setemail/v1, and user/profile/sethandle/v1 which successfully updates users first name, last name, email and handle_str
def test_update_name():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    token = response_data2['token']
    
    data = {
        "token": token,
        "name_first": "ronald",
        "name_last": "mcdonald"
    }
    
    data2 = {
        "token": token,
        "email": "ronaldmcdonald@gmail.com"
    }
    
    data3 = {
        "token": token,
        "handle_str": "fastfood"
    }
    
    response3 = requests.put(config.url + 'user/profile/setname/v1', json = data)
    assert response3.status_code == 200
    
    response4 = requests.put(config.url + 'user/profile/setemail/v1', json = data2)
    assert response4.status_code == 200
    
    response5 = requests.put(config.url + 'user/profile/sethandle/v1', json = data3)
    assert response5.status_code == 200
    
    response6 = requests.get(config.url + 'user/profile/v1', params={'token': response_data2['token'], 'u_id': response_data2['auth_user_id']})
    response6_data = response6.json()
    assert response6.status_code == 200
    assert response6_data['user'] == {
        'email': 'ronaldmcdonald@gmail.com',
        'handle_str': 'fastfood',
        'name_first': 'ronald',
        'name_last': 'mcdonald',
        'u_id': 1,
        'profile_img_url': 'http://localhost:8080/static/generic.jpg',
    }
    
#5. Tests user/profile/setname/v1 when name_first or name_last is of an invalid length
def test_invalid_name():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    invalid_data1 = {
        "token": response_data2['token'],
        "name_first": "",
        "name_last": "mcdonald"
    }
    
    invalid_data2 = {
        "token": response_data2['token'],
        "name_first": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
        "name_last": "mcdonald"
    }
    
    invalid_data3 = {
        "token": response_data2['token'],
        "name_first": "ronald",
        "name_last": ""
    }
    
    invalid_data4 = {
        "token": response_data2['token'],
        "name_first": "ronald",
        "name_last": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    }
    
    response3 = requests.put(config.url + 'user/profile/setname/v1', json = invalid_data1)
    assert response3.status_code == 400
    
    response4 = requests.put(config.url + 'user/profile/setname/v1', json = invalid_data2)
    assert response4.status_code == 400
    
    response5 = requests.put(config.url + 'user/profile/setname/v1', json = invalid_data3)
    assert response5.status_code == 400
    
    response6 = requests.put(config.url + 'user/profile/setname/v1', json = invalid_data4)
    assert response6.status_code == 400

#6. Tests user/profile/setemail/v1 when email is of an invalid format and when email is already being used
def test_invalid_email():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    assert response.status_code == 200
    
    invalid_data1 = {
        "token": response_data2['token'],
        "email": "invalidemail"
    }
    
    invalid_data2 = {
        "token": response_data2['token'],
        "email": "hollymcklin@gmail.com"
    }
    
    response3 = requests.put(config.url + 'user/profile/setemail/v1', json = invalid_data1)
    assert response3.status_code == 400
    
    response4 = requests.put(config.url + 'user/profile/setemail/v1', json = invalid_data2)
    assert response4.status_code == 400

#7. Tests user/profile/sethandle/v1 when handle_str is either of an invalid length, contains characters that aren't alphanumeric and when handle is already being used
def test_invalid_handle():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    assert response.status_code == 200
    
    invalid_data1 = {
        "token": response_data2['token'],
        "handle_str": "hi"
    }
    
    invalid_data2 = {
        "token": response_data2['token'],
        "handle_str": "invalid@ handle"
    }
    
    invalid_data3 = {
        "token": response_data2['token'],
        "handle_str": "hollymcklin"
    }
    
    response3 = requests.put(config.url + 'user/profile/sethandle/v1', json = invalid_data1)
    assert response3.status_code == 400
    
    response4 = requests.put(config.url + 'user/profile/sethandle/v1', json = invalid_data2)
    assert response4.status_code == 400   
    
    response5 = requests.put(config.url + 'user/profile/sethandle/v1', json = invalid_data3)
    assert response5.status_code == 400   

    
#8. Tests user/profile/uploadphoto/v1, user/profile/v1 and users/all/v1 work successfully together
def test_upload_photo_valid():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    response_data3 = response.json()
    assert response.status_code == 200
    
    upload_info = {
        "token": response_data2['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": "0",
        "y_start": "0",
        "x_end": "100",
        "y_end": "100"
    }
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', 
    json = upload_info)
    assert response.status_code == 200
    
    response6 = requests.get(config.url + 'user/profile/v1', params={'token': response_data2['token'], 'u_id': response_data2['auth_user_id']})
    response6_data = response6.json()
    assert response6.status_code == 200
    assert response6_data['user'] == {
        'email': 'crystaldcunha@gmail.com',
        'handle_str': 'crystaldcunha',
        'name_first': 'crystal',
        'name_last': 'dcunha',
        'profile_img_url': 'http://localhost:8080/static/crystaldcunha.jpg',
        'u_id': 1,
    } 
    
    response6 = requests.get(config.url + 'users/all/v1', params={'token': response_data3['token']})
    response6_data = response6.json()
    assert response6.status_code == 200
    assert response6_data['users'] == [
        {'email': 'crystaldcunha@gmail.com',
        'handle_str': 'crystaldcunha',
        'name_first': 'crystal',
        'name_last': 'dcunha',
        'profile_img_url': 'http://localhost:8080/static/crystaldcunha.jpg',
        'u_id': 1},
        {'email': 'hollymcklin@gmail.com',
        'handle_str': 'hollymcklin',
        'name_first': 'Holly',
        'name_last': 'McKlin',
        'profile_img_url': 'http://localhost:8080/static/generic.jpg',
        'u_id': 2}
    ] 

#9. Tests user/profile/uploadphoto/v1 when a png url is inputted
def test_upload_photo_png_url():
    response = requests.delete(config.url + 'clear/v1')
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user1_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user1_login_data)
    response_data2 = response.json()
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/register/v2', 
    json = user2_register_data)
    assert response.status_code == 200
    
    response = requests.post(config.url + 'auth/login/v2', 
    json = user2_login_data)
    assert response.status_code == 200
    
    upload_info = {
        "token": response_data2['token'],
        "img_url": "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png",
        "x_start": "0",
        "y_start": "0",
        "x_end": "100",
        "y_end": "100"
    }
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', 
    json = upload_info)
    assert response.status_code == 400
    
    upload_info = {
        "token": response_data2['token'],
        "img_url": "https://google.com/404",
        "x_start": "0",
        "y_start": "0",
        "x_end": "100",
        "y_end": "100"
    }
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', 
    json = upload_info)
    assert response.status_code == 400
    
    upload_info = {
        "token": response_data2['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": "100",
        "y_start": "100",
        "x_end": "50",
        "y_end": "50"
    }
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', 
    json = upload_info)
    assert response.status_code == 400 
    
    upload_info = {
        "token": response_data2['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": "0",
        "y_start": "0",
        "x_end": "1000",
        "y_end": "1000"
    }
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', 
    json = upload_info)
    assert response.status_code == 400 
    
    upload_info = {
        "token": response_data2['token'],
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": "-1",
        "y_start": "-1",
        "x_end": "100",
        "y_end": "100"
    }
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', 
    json = upload_info)
    assert response.status_code == 400 
