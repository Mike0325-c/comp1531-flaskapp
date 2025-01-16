from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import decode_jwt
from src import config
import string
import re
import hashlib
import jwt
import urllib.request
import requests
import sys
from PIL import Image
import io
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def users_all_v1(token):
    '''
<Takes the token of a user and returns a list of all users and their details>

Arguments:
    <token> (<string>) - <contains user_id and session_id

Exceptions:
    AccessError  - Occurs when token is of a invalid format, or the session_id is invalid i.e the user has logged out. 

Return Value:
    Returns <users> which consists of <u_id, email, name_first, name_last, handle_str>
    '''

    store = data_store.get()
    users_all_data = []
    decoded_object = decode_jwt(token)
    
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    
    for user in store['users']:
        generic_handle = "generic"        
        for image in store['images']:
            if image['user_id'] == user[0]:
                if image["file_address"] == 'static/' + user[5] + '.jpg':
                    generic_handle = user[5]
                       
        profile_img_url = config.url + 'static/' + generic_handle +'.jpg'
        user_dict = {'u_id': user[0], 'email': user[1], 'name_first': user[3], 'name_last': user[4], 'handle_str': user[5], 'profile_img_url': profile_img_url}
        users_all_data.append((user_dict))
        
    data_store.set(store)
    
    return {
        'users': users_all_data
    }
    
def user_profile_v1(token, u_id):
    '''
<Takes the u_id of a user and returns their details>

Arguments:
    <token> (<string>) - <contains user_id and session_id
    <u_id> (<string/integer>) - <u_id of users profile, should be of a valid format

Exceptions:
    AccessError  - Occurs when token is of a invalid format, or the session_id is invalid i.e the user has logged out.   

Return Value:
    Returns <user> which consists of <u_id, email, name_first, name_last, handle_str>
    '''
    
    store = data_store.get()
    user_profile_data = {}
    auth_user_id = int(u_id)
    
    decoded_object = decode_jwt(token)
    
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    #checking for a invalid u_id
    counter = 0
    handle =""
    for user in store['users']:
        if (user[0] == auth_user_id):
            handle = user[5]
            counter += 1
    
    if (counter == 0):        
        raise InputError(description="Invalid user_id - unregistered user")
    
    generic_handle = "generic"        
    for image in store['images']:
        if image['user_id'] == auth_user_id:
            if image["file_address"] == 'static/' + handle + '.jpg':
                generic_handle = handle
                
                
    profile_img_url = config.url + 'static/' + generic_handle +'.jpg'
    
    for user in store['users']:
        if (user[0] == auth_user_id):
            user_profile_data = {
                'u_id': auth_user_id,
                'email': user[1],
                'name_first': user[3],
                'name_last': user[4],
                'handle_str': user[5],
                'profile_img_url': profile_img_url
            }
        
    data_store.set(store)
    
    return {
        'user': user_profile_data
    }
    
def user_profile_setname_v1(token, name_first, name_last):
    '''
<Takes the token of a user and updates their first and last name>

Arguments:
    <token> (<string>) - <contains user_id and session_id
    <name_first> (<string>) - < first name of user, should be of a valid format
    <name_last> (<string>) - < last name of user, should be of a valid format

Exceptions:
    AccessError  - Occurs when token is of a invalid format, or the session_id is invalid i.e the user has logged out.   
    InputError  - Occurs when first and last name isn't between 1 and 50 characters.

Return Value:
    Returns {}
    '''
    
    store = data_store.get()   
    decoded_object = decode_jwt(token)
    
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
        
    #checking for invalid length of first_name
    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError(description="First name not between 1 and 50 characters")        
    
    #checking for invalid length of last_name
    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError(description="Last name not between 1 and 50 characters")  
    
    user_id = decoded_object['user_id']
    
    for user in store['users']:
        if(user[0] == user_id):
            if (user[3] != name_first):
                user[3] = name_first
            if (user[4] != name_last):
                user[4] = name_last
        
    data_store.set(store)
    
    return {}
    
def user_profile_setemail_v1(token, email):
    '''
<Takes the token of a user and updates their email>

Arguments:
    <token> (<string>) - <contains user_id and session_id
    <email> (<string>) - < email of user, should be of a valid format

Exceptions:
    AccessError  - Occurs when token is of a invalid format, or the session_id is invalid i.e the user has logged out.   
    InputError  - email is not valid and if email address is already registered

Return Value:
    Returns {}
    '''
    
    store = data_store.get()   
    decoded_object = decode_jwt(token)
    
    #checking for invalid email
    if (re.fullmatch(regex, email) == None):
        raise InputError(description="Invalid Email")
        
    #if email has already been registered
    for user in store['users']:
        if (user[1] == email):
            raise InputError(description="Email has already been registered")
    
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    user_id = decoded_object['user_id']
    
    for user in store['users']:
        if(user[0] == user_id):
            if (user[1] != email):
                user[1] = email
        
    data_store.set(store)
    
    return {}
    
def user_profile_sethandle_v1(token, handle_str):
    '''
<Takes the token of a user and updates their handle>

Arguments:
    <token> (<string>) - <contains user_id and session_id
    <handle_str> (<string>) - < email of user, should be of a valid format

Exceptions:
    AccessError  - Occurs when token is of a invalid format, or the session_id is invalid i.e the user has logged out.   
    InputError  - handle is not between 3 and 20 characters, contains characters which are not alphanumeric, and if the handle already exists

Return Value:
    Returns {}
    '''
    
    store = data_store.get()   
    decoded_object = decode_jwt(token)
    
    #checking if handle is already in user
    for user in store['users']:
        if user[5] == handle_str:
            raise InputError(description="handle_str already in use")
    
    #checking for valid length of handle_str
    if (len(handle_str) < 3) or (len(handle_str) > 20):
        raise InputError(description="handle_str must be between 3 and 30 characters")
        
    #checking if handle is alphanumeric
    if (handle_str.isalnum() != True):
        raise InputError(description="handle is not alphanumeric")
    
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    user_id = decoded_object['user_id']
    
    for user in store['users']:
        if(user[0] == user_id):
            if (user[5] != handle_str):
                user[5] = handle_str
            
    data_store.set(store)
    
    return {}
    
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''
<Takes the token of a user and updates their handle>

Arguments:
    <token> (<string>) - <contains user_id and session_id
    <handle_str> (<string>) - < email of user, should be of a valid format

Exceptions:
    AccessError  - Occurs when the session_id is invalid i.e the user has logged out.   
    InputError  - img_url return an HTTP status other than 200, x_start, y_start, x_end , y_end are not within dimensions of image, x_end < x_start, or y_end < y_start, image is not jpg. 

Return Value:
    Returns {}
    '''
    
    store = data_store.get()   
    decoded_object = decode_jwt(token)
    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)
    
    #checks the HTTP status returned 
    response = requests.get(img_url, stream=True)
    if response.status_code != 200:
        raise InputError(description='Img_url is not valid')
    
    image_bytes = io.BytesIO(response.content)
    #checks if image uploaded is a jpg
    img = Image.open(image_bytes)    
    if (img.format != 'JPEG'):
        raise InputError(description='Image needs to be of format JPG or JPEG')
        
    #checks for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
            
    #checks whether basic input is correct and does not contradict
    if (x_end < x_start) or (y_end < y_start):
        raise InputError(description='Dimension not valid')
    
    #checks that sizes inputted does not exceed size of image    
    width, height = img.size
    if (width < x_end) or (height < y_end):
        raise InputError(description='Dimension exceed those of image') 
    
    if (x_start < 0) or (y_start < 0):
        raise InputError(description='Dimension exceed those of image') 
    
    handle =""
    user_id = int(decoded_object['user_id'])
    for user in store['users']:
        if user_id == user[0]:
            handle = user[5]
            
    filename = handle + "." + "jpg"

    urllib.request.urlretrieve(img_url, 'static/' + filename)
    imageObject = Image.open('static/' + filename)
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save('static/' + filename)
    
    image_dict = {"user_id": user_id, "file_address": 'static/' + filename}
    store['images'].append((image_dict))        
    data_store.set(store)
    
    return {}
