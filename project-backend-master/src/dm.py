
from datetime import timezone
from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import auth_register_v1, decode_jwt
from src.channels import *

import string
import jwt
import re
import requests
import json
from src import config
from src.other import clear_v1
from src import config

def find_dm(dm_id, store):
    for dm in store['dm']:
        if dm[1] == dm_id:
            return dm

def dm_create_v1(token, u_ids):
    '''
    <Creates a new DM with auto DM name and can be directed to many u_ids. 
    The person who created the dm is the owner. 
    If the token or u_ids is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) - < jwt encoded string>
    	<u_ids> (<List>)   - <u_ids contains the user(s) that this DM is directed>

    
    Exceptions:
    	InputError  - Occurs when any u_id in u_ids does not refer to a valid user.
    	AccessError - Occurs when user_id and session_id are not valid.
    
    Return Value:
    	Returns <'dm_id': dm_num>  when valid <token and u_ids> have been inputted.
    
    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    dm_num = (len(store['dm']) + 1)
    token_flag2 = False
    session = False
    owner_members = []
    all_members = []    
    messages = []
    name = []
    
    #checking for an invalid session_id
    
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
    
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    for user in store['users']:
        if (user[0] == decoded_object['user_id']):
            #concatenate handle
            handle_str = (user[3] + user[4])
            #removing character not alphanumeric
            unwanted_characters = string.punctuation + ' ' + '-'
            for i in unwanted_characters:
                handle_str = handle_str.replace(i, '')
            name.append(handle_str)
            generic_handle = "generic"        
            for image in store['images']:
                if image['user_id'] == user[0]:
                    if image["file_address"] == 'static/' + user[5] + '.jpg':
                        generic_handle = user[5]                           
            profile_img_url = config.url + 'static/' + generic_handle +'.jpg'
            owner_members.append({'u_id': decoded_object['user_id'],
             'email':user[1] ,
             'name_first':user[3], 'name_last': user[4], 
             'handle_str': user[5]})
            all_members.append({'u_id': decoded_object['user_id'], 
            'email':user[1] ,
             'name_first':user[3], 'name_last': user[4], 
             'handle_str': user[5], 'profile_img_url': profile_img_url})
             
    for users in u_ids:
        for user in store['users']:
            if (users == user[0]):
                token_flag2 = True
                #concatenate handle
                handle_str = (user[3] + user[4])
                #removing character not alphanumeric
                unwanted_characters = string.punctuation + ' ' + '-'
                for i in unwanted_characters:
                    handle_str = handle_str.replace(i, '')
                name.append(handle_str)
                generic_handle = "generic"        
                for image in store['images']:
                    if image['user_id'] == user[0]:
                        if image["file_address"] == 'static/' + user[5] + '.jpg':
                            generic_handle = user[5]
                profile_img_url = config.url + 'static/' + generic_handle +'.jpg'
                all_members.append({'u_id': users, 'email':user[1] ,
                 'name_first':user[3], 'name_last': user[4], 
                 'handle_str': user[5], 'profile_img_url': profile_img_url})
        if(token_flag2 == False):
            raise InputError(description="u_ids does not refer to valid user")
    name.sort()
    store['name'].append([dm_num, name])
    store['dm'].append([decoded_object['user_id'], dm_num, name, owner_members, all_members, messages])
    '''
    for users in store['dm']:
        messages.append({'message_id':users[2]})
    '''
    data_store.set(store)
    
    return {
        'dm_id': dm_num
    
    }
    
def dm_list_v1(token):
    '''
    <Creates a new DM with auto DM name and can be directed to many u_ids. 
    The person who created the dm is the owner. 
    If the token or u_ids is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) - < jwt encoded string>
    	<u_ids> (<List>)   - <u_ids contains the user(s) that this DM is directed>

    
    Exceptions:
    	InputError  - Occurs when any u_id in u_ids does not refer to a valid user.
    	AccessError - Occurs when user_id and session_id are not valid.
    
    Return Value:
    	Returns <'dm_id': dm_num>  when valid <token and u_ids> have been inputted.
    
    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    dm_list = []
    session = False
    authorised = False
    joined_name = ""
    
    #checking for an invalid session_id
    
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
    if (session == False):
        raise AccessError(description="Invalid session_id")

    for dms in store['dm']:
        for detail in dms[4] :
            if (detail['u_id'] == decoded_object['user_id']):
                authorised = True
                for names in store['name']:
                    if names[0] == dms[1]:
                        joined_name = ", ".join(names[1])
                dm_list.append({'dm_id':dms[1] , 'name': joined_name})
        if (authorised == False):
            raise AccessError('the authorised user is not a member of any DMs')
    
    data_store.set(store)
    
    return {
        'dms': dm_list
    
    }
     
def dm_details_v1(token, dm_id):
    '''
    <Provides basic details about the DM the member is part of. 
    It will provide name and the members of DM.  
    If the token or dm_id is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) - < jwt encoded string>
    	<dm_id> (<number>)   - <contains the dm id of a DM>

    
    Exceptions:
    	InputError  - Occurs when dm_id does not refer to a valid DM
    	AccessError - Occurs when user_id and session_id are not valid.
    				- Occurs when dm_id is valid and the authorised user is not the member of the DM.
    
    Return Value:
    	Returns <{name, member}>  when valid <token and dm_id> have been inputted.
    '''
    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    dm_flag = False
    authorised = False
    all_member = []
    dm_id = int(dm_id)
    session = False
    #checking for an invalid token and invalid session_id
    
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True

    if (session == False):
        raise AccessError(description="Invalid session_id")
    


    #checks if memeber is in a valid dm_id.
    for dms in store['dm']:
        if (dms[1] == dm_id):
            dm_flag = True
            for detail in dms[4] :
                if (detail['u_id'] == decoded_object['user_id']):
                    authorised = True
    
    if (dm_flag == False):
        raise InputError(description="Invalid DM")
    
    if (authorised == False):
        raise AccessError('the authorised user is not a member of the channel')
    
    
    for DMs in store['dm']:
        if DMs[1] == dm_id:
    		#for all members
            for join in DMs[4]:
                if(join['u_id'] != False):
                    alls = {'u_id': join['u_id'], 'email': join['email'],'name_first': join['name_first'], 'name_last': join['name_last'], 'handle_str': join['handle_str'], 'profile_img_url': join['profile_img_url']}
                    all_member.append(alls)
    joined_name = ""
    for names in store['name']:
        if names[0] == dm_id:
                joined_name = ", ".join(names[1])

    data_store.set(store)
    return {'name': joined_name,'members': all_member}
    
    
def dm_remove_v1(token, dm_id):
    '''
    <Deletes a DM with the given dm_id. This can be only done by the creator of the DM only. 
    If the token or dm_id is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) - < jwt encoded string>
    	<dm_id> (<number>)   - <contains the dm id of a DM>

    
    Exceptions:
    	InputError  - Occurs when dm_id does not refer to a valid DM
    	AccessError - Occurs when user_id and session_id are not valid.
    				- Occurs when dm_id is valid and the authorised user is not the original DM creator
    
    Return Value:
    	Returns <{}>  when valid <token and dm_id> have been inputted.
    '''
    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    dm_flag = False
    dm_id = int(dm_id)
    authorised = False
    session = False
    #checking for an invalid session_id
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True

    if (session == False):
        raise AccessError(description="Invalid session_id")
        
    #checking if dm_id refer to a valid DM
    for i in store['dm']:
        if (i[1] == dm_id):
            dm_flag = True
            for detail in i[4] :
                if (detail['u_id'] == decoded_object['user_id']):
                    authorised = True
                    
    if (dm_flag == False):
        raise InputError(description="Invalid DM")
    
    if (authorised == False):
            raise AccessError('the authorised user is not a member of the channel')
        
    
                
    
        
    store['dm'] = [i for i in store['dm'] if not (i[1] == dm_id)]
    data_store.set(store)
    return {}
    
def dm_leave_v1(token, dm_id):
    '''
    <Removes the memeber from the DM. Anyone can leave the DM and the creator may leave too. 
    If the token or dm_id is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) - < jwt encoded string>
    	<dm_id> (<number>)   - <contains the dm id of a DM>

    
    Exceptions:
    	InputError  - Occurs when dm_id does not refer to a valid DM
    	AccessError - Occurs when user_id and session_id are not valid.
    				- Occurs when dm_id is valid and the authorised user is not the original DM creator
    
    Return Value:
    	Returns <{}>  when valid <token and dm_id> have been inputted.
    '''
    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    dm_flag = False
    dm_id = int(dm_id)
    session = False
    authorised = False

    #checking for an invalid session_id
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True

    if (session == False):
        raise AccessError(description="Invalid session_id")

    
    #checking if dm_id refer to a valid DM
    for i in store['dm']:
        if (i[1] == dm_id):
            dm_flag = True
            for detail in i[4] :
                if (detail['u_id'] == decoded_object['user_id']):
                    authorised = True
                    detail['u_id'] = False
        
    if (dm_flag == False):
        raise InputError(description="Invalid DM")
    if (authorised == False):
            raise AccessError('the authorised user is not a member of the channel')

    data_store.set(store)
    return {}

def find_channel(dm_id, store):
    for channel in store['dm']:
        if channel[1] == dm_id:
            return channel

def dm_messages_v1(token, dm_id, start):   
    '''
    <collect and return up to 50 messages from users in a specified channel>
    	
    Arguments:
    		token -  <The id of the users after they register with detail of DM> 
    		dm_id (int) -  <The id of the DM which shows the detail>
    		start(int) -  <The index of the message which the users want to start>
    	
    Exceptions:
    		InputError - Occurs when dm_id is invalid or start is greater than total number of messages in DM
    		AccessError - Occurs when the authorised user is not a member of DM 
    	
    Return Value:
    		Return the detail of up to 50 messages with start and end 
    '''
    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']   
    dm_id = int(dm_id) 
    start = int(start)
    end = -1
    messages = []
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
   
    #checks if dm_id is valid
    current = False
    for detail in store['dm']:
        if detail[1] == dm_id:
            current = True           
    if current == False:
        raise InputError(description='dm_id does not refer to a valid dm')  
   
    dm_list = find_dm(dm_id, store)
    authorised = False
    total_messages = len(dm_list[5])
    #checks if user_id is a member
    for dm in store['dm']:
        for detail in dm[4]:
            if (detail['u_id'] == auth_user_id):
                authorised = True                
    if authorised == False:
        raise AccessError(description='the authorised user is not a member of the dm')
    
	#check if the start is greater than the total number of messages
    if start > total_messages:
        raise InputError(description='start is greater than the total number of messages in the dm')
    
    if total_messages > (start + 50):
        messages = dm_list[5][start: start + 51]
        end = start + 50
    else:
        messages =  dm_list[5][start:]
         
    data_store.set(store)
    return {
        'messages': messages,
        'start': start,
        'end': end,
    }
