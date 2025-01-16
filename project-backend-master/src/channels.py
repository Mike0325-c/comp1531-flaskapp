from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import auth_register_v1, decode_jwt
import string
import re
import jwt
from src import config

def channels_list_v1(token):
    '''
    <Given a valid token, lists all the channels the user is part of>

    Arguments:
    	<token> (<string>) - <string returned from auth_register and auth_login>

    Exceptions:
    	AccessError - Occurs when invalid user_id is passed into the function, invalid token is passed in or session id isn't valid

    Return Value:
    	Returns <channels_list> list which contains channel_id and name on <the fact that a valid user_id is given>
    '''
    store = data_store.get()
    #created a list of dictionaries to return
    channels_list = []
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']
    
    #checking for a invalid user_id and invalid session_id
    counter = 0
    session = False
    
    for user in store['users']:
        if (user[0] == auth_user_id):
            counter += 1
            
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
   
    for channel in store['channels']:        
        for ch in channel[5]:
            if (ch['u_id'] == auth_user_id) and session == True:
                counter += 1
        
    
    if (counter == 0):        
        raise AccessError(description="Invalid user_id - unregistered user")
        
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    #checking all the channels the user is part of a storing it in the list
    for channel in store['channels']:
        if (channel[0] == auth_user_id):
            channels_list.append({'channel_id': channel[1], 
            'name': channel[2]})
        else:
            for ch in channel[5]:
                if(ch['u_id'] == auth_user_id):
                    channels_list.append({'channel_id': channel[1], 
                    'name': channel[2]}) 
    
    data_store.set(store) 
    
    return {
        'channels' : channels_list
    }

	
def channels_listall_v1(token):
    '''
    <Given a valid token, will list all the channels created by users>

    Arguments:
    	<token> (<string>) - <string returned from auth_register and auth_login>

    Exceptions:
    	AccessError -  Occurs when invalid user_id is passed into the function, invalid token is passed in or session id isn't valid

    Return Value:
    	Returns <channels_list_all> list which contains channel_id and name on <the fact that a valid user_id is given>
    '''
    store = data_store.get() 
    #created a list of dictionaries to return
    channels_list_all = []
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']
     
    #checking for a invalid user_id and session_id
    counter = 0
    session = False
    for user in store['users']:
        if (user[0] == auth_user_id) and (decoded_object['session_id'] in user[6]):
            session = True
            counter += 1
    
    if (counter == 0):        
        raise AccessError(description="Invalid user_id - unregistered user")
        
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    #storing all channel id and names in channel_list_all to be returned 
    for channel in store['channels']:
        channels_list_all.append({'channel_id': channel[1], 
        'name': channel[2]})
    
    data_store.set(store)

    return {
        'channels': channels_list_all
    }

def channels_create_v1(token, name, is_public):
    '''
    <Creates a new channel with the given name that might be public or private.
    The person who established the channel immediately joins it. 
    If the user or channel name is incorrect, InputError and AccessError are raised.>

    Arguments:
    	<token> (<string>) - < jwt encoded string>
    	<name> 		   (<string>)    - <Name of the new channel being created>
    	<is_public>    (<boolean>)   - <Store whether the channel is public or private; Public = true, Private = false>
    	
    
    Exceptions:
    	InputError  - Occurs when name is invalid (not between 1 to 20 characters).
    	AccessError - Occurs when user has not been registered.
    
    Return Value:
    	Returns <'channel_id': channels_num>  when valid <token, name, and is_public> have been inputted
    
    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    channels_num = len(store['channels']) + 1
    token_flag = False
		
    #checking if token exists
    
    for user in store['users']:
        if (user[0] == decoded_object['user_id']):
            token_flag = True
    
    if (token_flag == False):        
        raise AccessError(description="User has not been registered")
	
    #checking for an invalid token and invalid session_id
    session = False
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
            
    if (session == False):
        raise AccessError(description="Invalid session_id")

	#if the name is not between 1 to 20 characters   
    if((len(name) > 20) or (len(name) < 1)):
        raise InputError(description="Invalid Name - Needs to be between 1 and 20 characters")
    
    #Store the new channel information and user details into channels dictionary.
    owner_members = []
    all_members = []    
    messages = []
    standup =  {'time_finish': -1, 'standup_packaged_message':'',}
    profile_img = ''
    
    for user in store['users']:
        if (user[0] == decoded_object['user_id']):
            generic_handle = "generic"        
            for image in store['images']:
                if image['user_id'] == user[0]:
                    if image["file_address"] == 'static/' + user[5] + '.jpg':
                        generic_handle = user[5]      
            profile_img = config.url + 'static/' + generic_handle +'.jpg'
        
            owner_members.append({'u_id': decoded_object['user_id'],
             'email':user[1], 'name_first':user[3], 'name_last': user[4], 
             'handle_str': user[5], 'profile_img_url': profile_img})
             
            all_members.append({'u_id': decoded_object['user_id'], 
            'email':user[1], 'name_first':user[3], 'name_last': user[4], 
             'handle_str': user[5], 'profile_img_url': profile_img})
    '''
    for users in store['channels']:
        messages.append({'message_id':users[2]})
    '''
    store['channels'].append([decoded_object['user_id'], channels_num, name, is_public, owner_members, all_members, messages, standup])
    '''
    tester = []
    for channel in store['channels']:
        if channel[1] == 1:
			#for all members
	        for join in channel[5]:
	            alls = {
	                'handle_str': join['handle_str'],
	                'profile_img_url': join['profile_img_url']
	            } 
	            tester.append(alls)
    '''
    data_store.set(store) 
	
    return {
        'channel_id': channels_num
	}
