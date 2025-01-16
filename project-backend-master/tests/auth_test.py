'''
import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError
from src.other import clear_v1

#Tests for registering a valid user
def test_register_valid_input():
    clear_v1()
    data = auth_register_v1('goodemail@yahoo.com', 'bluesky', \
     'Shaggy','Wilson')
    assert(data['auth_user_id'] == 1)

#Tests for when a valid user is registered, they are then able login successfully   
def test_login_valid_input():
    clear_v1()
    auth_register_v1('goodemail@yahoo.com', 'bluesky', \
     'Shaggy','Wilson')
    login_data = auth_login_v1('goodemail@yahoo.com', 'bluesky')
    assert(login_data['auth_user_id'] == 1)

#Tests for unregistered email being logged in
def test_login_invalid_email():
    clear_v1()
    auth_register_v1('goodemail@yahoo.com', 'bluesky', 'Shaggy','Wilson')
    with pytest.raises(InputError):
        auth_login_v1('notthere@gmail.com', 'bluesky')

#Tests for password not matching the email which was registered       
def test_login_invalid_password():
    clear_v1()
    auth_register_v1('goodemail@yahoo.com', 'bluesky', 'Shaggy','Wilson')
    with pytest.raises(InputError):
        auth_login_v1('goodemail@yahoo.com', 'wrongpassword')

#Tests for first and last name not being between 1 and 50 characters
def test_register_invalid_first_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('validemail@yahoo.com', 'bluesky', 'abcdefghijklmnopqrstuvqxyzabcdefghijklmnopqrstuvwxyz', 'Doe')
        auth_register_v1('goodemail@yahoo.com', 'yellowsky', 'John', 'abcdefghijklmnopqrstuvqxyzabcdefghijklmnopqrstuvwxyz')
        auth_register_v1('goodemail@yahoo.com', 'yellowsky', '','')

#Tests for password being less than 6 characters
def test_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('goodemail@yahoo.com', 'sky', 'Shaggy','Wilson')

#Tests for duplicate email being registered twice
def test_auth_register_duplicate_email():
    clear_v1()
    auth_register_v1('crystal@gmail.com', 'laptop', 'Crystal', 'Smith')
    with pytest.raises(InputError):
        assert auth_register_v1('crystal@gmail.com', 'computer', 'Jane', 'Smith')

#Tests for email being registered of the wrong format      
def test_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('yahoo', 'finepassword', 'Oscar', 'Poly')
'''
