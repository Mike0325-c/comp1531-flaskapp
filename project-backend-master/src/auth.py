from src.data_store import data_store
from src.error import InputError, AccessError
import string
import re
import hashlib
import jwt
import smtplib, ssl
import random
import string
import secrets
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 

SESSION_TRACKER = 0
SECRET = 'CREATED11OWN'

def generate_new_session_id():
    '''Generates a session id, adding onto the previous one
    
    Returns:
        number: the next session ID
    '''
    global SESSION_TRACKER
    SESSION_TRACKER += 1
    return SESSION_TRACKER
    
def generate_jwt(user_id, session_id=None):
    '''Generates a JWT using the global SECRET
    
    Arguments:
        user_id([string]): the user_id
        session_id([string], optional): the session id, 
        if none is provided will generate a new one. Defaults to None
    
    Returns:
    string: A JWT encoded string
    '''
    if session_id == None:
        session_id = generate_new_session_id()
    return jwt.encode({'user_id': user_id, 'session_id': session_id}, SECRET,
     algorithm='HS256')
     
def decode_jwt(encoded_jwt):
    '''Decodes a JWT string into an object of the data
    
    Arguments:
        encoded_jwt([string]): the encoded JWT as a string
        
    Returns:
        object: An object storing the body of the JWT encoded string
    '''
    try:
        token = jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])
        return token
    except:
        raise AccessError(description="invalid token") from None


def auth_login_v1(email, password):
    '''
Takes the user email and password which has been registered and returns the user id

Arguments:
    <email> (<string>)    - <should be valid (include @ symbol etc) and have been registered>
    <password> (<string>)    - <should be valid, longer than 6 characters and have been registered>

Exceptions:
    InputError  - Occurs when password entered does not match the one registered with the email, and when email has not been registered yet

Return Value:
    Returns <user_id> when valid <email, password> have been inputted
'''
    store = data_store.get()
    user_id = 0
    session_id = 0
    for user in store['users']:
        if (user[1] == email):
            user_id = user[0]
            if (user[2] != hashlib.sha256(password.encode()).hexdigest()):
                raise InputError(description="Incorrect Password")
            else:
                session_id = generate_new_session_id()
                user[6].append(session_id)
    
    #to test if email is registered
    if (user_id == 0):
        raise InputError(description="Email is not registered") 
    
    data_store.set(store)
    
    return {
        'token': generate_jwt(user_id, session_id),
        'auth_user_id': user_id,
    }


def auth_register_v1(email, password, name_first, name_last):
    '''
<Takes the email, password, first and last name of a user and registers them>

Arguments:
    <email> (<string>)    - <email owned by user, should be of a valid format (include @symbol, . symbol)>
    <password> (<string>)    - <should be longer than 6 characters>
    <name_first> (<string>)    - <first name of user, should be of appropriate length>
    <name_last> (<string>)    - <last name of user, should be of appropriate length>

Exceptions:
    InputError  - Occurs when email is of a invalid format, when password is too short, first and last name isn't between 1 and 50 characters and email 
    has already been registered.  

Return Value:
    Returns <user_id> when valid <email, password> have been inputted
'''
    store = data_store.get()
    
    if (re.fullmatch(regex, email) == None):
        raise InputError(description="Invalid Email")

    # if password is less than 6 characters long
    if (len(password) < 6): 
        raise InputError(
        description="Invalid Password - Needs to be more than 6 characters")
    
    #if first name is not between 1 to 50 characters    
    if (len(name_first) > 50) or (len(name_first) < 1):
        raise InputError(description="Invalid First Name - Needs to be \
        between 1 and 50 characters")
    
    #if last name is not between 1 to 50 characters    
    if (len(name_last) > 50) or (len(name_last) < 1):
        raise InputError(description= "Invalid Last Name - \
        Needs to be between 1 and 50 characters")
    
    #if email has already been registered
    for user in store['users']:
        if (user[1] == email):
            raise InputError(description="Email has already been registered")
    
    user_id = len(store['users']) + 1
    #concatenate handle
    handle_str = (name_first + name_last).lower()
    
    #removing character not alphanumeric
    unwanted_characters = string.punctuation + ' ' + '-'
    for i in unwanted_characters:
        handle_str = handle_str.replace(i, '')
    
    #cuts handle_str at 20 characters
    if (len(handle_str) > 20):
        handle_str = [handle_str[i:20] for i in range(0, 1)]
        handle_str = handle_str[0]
    
    #searched for duplicate handle_str and adds integer at end     
    integer = 0
    for user in store['users']:
        if (user[5][0:len(handle_str)] == handle_str):
            integer += 1
    
    #if there is a duplicate case, then add this integer 
    #onto the end of handle_str          
    if (integer - 1 >= 0):     
        handle_str = handle_str + str(integer - 1)
    
    #added during iteration 2
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    
    session_id = generate_new_session_id()
    session_list = [session_id]
    
    store['users'].append([user_id, email, password_hashed, name_first, \
    name_last, handle_str, session_list])
    data_store.set(store) 

    
    return {
        'token': generate_jwt(user_id, session_id),
        'auth_user_id': user_id,
    }

def auth_logout_v1(token):
    '''
Takes in an active user token and invalidates it, logging the user out

Arguments:
    <token> (<string>) - < jwt encoded string

Exceptions:
    InputError - invalid token

Return Value:
    Returns empty dictionary
    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    
    for user in store['users']:
        if (user[0] == decoded_object['user_id']):
            if decoded_object['session_id'] in user[6]:
                user[6].remove(decoded_object['session_id'])
            else:
                raise AccessError(description="Invalid Token")
    
    data_store.set(store)
    
    return {}
 
def auth_passwordreset_request_v1(email):
    '''
Takes in an active user email and sends them a reset code

Arguments:
    <email> (<string>) - < string

Exceptions:
    -

Return Value:
    Returns empty dictionary
    '''
    store = data_store.get()
    
    num = 10
    secret_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num)) 
    
    registered_email = False
    for user in store['users']:
        if user[1] == email:
            registered_email = True
    
    if (registered_email == False):
        return {}

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "project1531.dummy.email@gmail.com"
    receiver_email = email
    password = 'Dummyemail1531'
    message = """Subject: Reset your UNSW Streams password

    Your reset code is: {secret_code}
    Please use this code to reset your password, if this wasn't you, ignore this email.
    This message was sent from UNSW Streams Python."""
    message_str = message.format(secret_code=secret_code)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_str)
        
    code_hashed = hashlib.sha256(secret_code.encode()).hexdigest()
    store['reset_code'].append([email, code_hashed])
    
    #logs user out when code is sent
    for user in store['users']:
        if (user[1] == email):
            user[6] = []
    
    data_store.set(store)
    return {}  
    
def auth_passwordreset_reset_v1(reset_code, new_password):
    '''
Takes in an active reset_code and changes the password

Arguments:
    <reset_code> (<string>) - < hashed string
    <new_password> (<string>)

Exceptions:
    - InputError - reset_code is invalid 
    - InputError - password entered is less than 6 characters

Return Value:
    Returns empty dictionary
    '''
    store = data_store.get()
    email = ''
    
    valid_code = False
    for code in store['reset_code']:
        if hashlib.sha256(reset_code.encode()).hexdigest() == code[1]:
            email = code[0]
            valid_code = True
   
    # if password is less than 6 characters long
    if (len(new_password) < 6): 
        raise InputError(
        description="Invalid Password - Needs to be more than 6 characters")
        
    # reset_code is invalid
    if (valid_code == False):
        raise InputError(description="Invalid reset_code")
        

    new_password_hashed = hashlib.sha256(new_password.encode()).hexdigest()
    for user in store['users']:
        if (user[1] == email):
            user[2] = new_password_hashed

    data_store.set(store)
    return {}
