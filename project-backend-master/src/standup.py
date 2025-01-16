from datetime import datetime, timezone
from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import auth_register_v1, decode_jwt
from src.channels import *
from src.dm import *
from src.message import *

import threading
import time
import string
import jwt
import re
import requests
import json
from src import config
from src.other import clear_v1

def message_send(token, channel_id):
    store = data_store.get()
    channel_id = int(channel_id)
    standup_dict = None
    for channel in store['channels']:
        if channel[1] == channel_id:
            standup_dict = channel
            break
    
    message = standup_dict[7]['standup_packaged_message']
    message_send_v1(token, channel_id, message)

def error_checker(token, channel_id):
    store = data_store.get()
    channel_id = int(channel_id)
    decoded_object = decode_jwt(token)
    session, invalid_channel_flag, already_member_flag = (False,)* 3

    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
    
    if (session == False):
        raise AccessError(description="Invalid session_id")
        
    for channel in store['channels']:
        #checking for a invalid channel_id (InputError)
        if (channel[1] == channel_id):
            invalid_channel_flag = True

        #checking for a valid channel_id but authorised user is not a memeber of the channel (AccessError)
        if (channel[1] == channel_id) and (channel[0] == decoded_object['user_id']):
            already_member_flag = True
            
    if (invalid_channel_flag == False):
        raise InputError(description="Channel_id does not refer to a valid channel")

    if (already_member_flag == False):
        raise AccessError(description="Authorised user is not a member of the channel")
    data_store.set(store)
    return 0




def standup_start_v1(token, channel_id, length):
    '''
    <For a given channel, start the standup period whereby for the next "length" seconds 
    if someone calls "standup/send" with a message, it is buffered during the X second window 
    then at the end of the X second window a message will be added to the message queue in the channel 
    from the user who started the standup. "length" is an integer that denotes the number of seconds that the standup occurs for.
    If the token, channel_id or length is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) 		- <jwt encoded string>
    	<channel_id> (<integer>)- <Channel id of the channel>
    	<length> (<integer>)	- <Denotes the number of seconds that the standup occurs for>
    
    Exceptions:
    	InputError  - Occurs when channel_id does not refer to a valid channel.
    				- Occurs when length is a negative integer.
    				- Occurs when an active standup is currently running in the channel.
    				
    	AccessError - Occurs when channel_id is valid and the authorised user is not a member of the channel.
    
    Return Value:
    	Returns <time_finish>  when valid <token, channel_id and length> have been inputted.
    
    '''
    
    store = data_store.get()
    #decoded_object = decode_jwt(token)
    length = int(length)
    channel_id = int(channel_id)
    if error_checker(token, channel_id) == 0:
        if(length < 0):
            raise InputError(description="Length is a negative integer")

        timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        time_finish = timestamp + length

        if standup_active_v1(token, channel_id).get('is_active') == True:
            raise InputError(description='An active standup is currently running in this channel')

        #Empty the standup_packaged_message.
        for m in store['channels']:
            if m[0] == channel_id:
                m[7]['standup_packaged_message'] = ''
                m[7]['time_finish'] = time_finish

        #send the message at the end of the standup
        threading.Timer(length, message_send,(token, channel_id,)).start()
        data_store.set(store)
        return {
            'time_finish': time_finish
        }
     


def standup_active_v1(token, channel_id):
    '''
    <For a given channel, return whether a standup is active in it, and what time the standup finishes.
    If no standup is active, then time_finish returns None.
    If the token or channel_id is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) 		- <jwt encoded string>
    	<channel_id> (<integer>)- <Channel id of the channel>
    
    Exceptions:
    	InputError  - Occurs when channel_id does not refer to a valid channel.

    	AccessError - Occurs when channel_id is valid and the authorised user is not a member of the channel.
    
    Return Value:
    	Returns <{is_active, time_finish }>  when valid <token and channel_id> have been inputted.
    
    '''
    
    store = data_store.get()
    #decoded_object = decode_jwt(token)
    channel_id = int(channel_id)
    if error_checker(token, channel_id) == 0:

    	current_timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    	
    	time_check = 0
    	
    	for finshed_time in store['channels']:
    	    if finshed_time[0] == channel_id:
    	        finish_time = finshed_time[7]['time_finish']
    	        time_check = (finshed_time[7]['time_finish'] - current_timestamp)
    	        break

    	if time_check > 0:
    	    is_active = True
    	    time_finish = finish_time
    	else :
    	    is_active = False
    	    time_finish = None
    	data_store.set(store)
    	return {
    	    'is_active': is_active,
    	    'time_finish': time_finish
    	}
    
    
def standup_send_v1(token, channel_id, message):
    '''
    <Sending a message to get buffered in the standup queue, assuming a standup is currently active.
    Note: We do not expect @ tags to be parsed as proper tags when sending to standup/send
    If the token, channel_id or message is incorrect, InputError or AccessError are raised.>

    Arguments:
    	<token> (<string>) 				- <jwt encoded string>
    	<channel_id> (<integer>)		- <Channel id of the channel>
    	<message> (<List of Dictionary>)- <List of dictionaries, where each dictionary contains types 
    									   { message_id, u_id, message, time_created, reacts, is_pinned>
    
    Exceptions:
    	InputError  - Occurs when channel_id does not refer to a valid channel.
    				- Occurs when length of message is over 1000 characters.
    				- Occurs when an active standup is not currently running in the channel.
    				
    	AccessError - Occurs when channel_id is valid and the authorised user is not a member of the channel.
    
    Return Value:
    	Returns <{}>  when valid <token, channel_id and message> have been inputted.
    
    '''
    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    channel_id = int(channel_id)
    error_checker(token, channel_id)
    

    if(len(message) > 1000):
        raise InputError(description="Length of message is over 1000 characters")
    
    if standup_active_v1(token, channel_id).get('is_active') == False:
        raise InputError(description="Standup is not Active")
        
    handle_str = ''
    
    for name in store['users']:
        if (name[0] == decoded_object['user_id']):
            handle_str = name[5]
            break
    
    mess_send = handle_str + ': ' + message + '\n'       
    
    for package in store['channels']:
        if package[1] == channel_id:
            package[7]['standup_packaged_message'] += mess_send
    data_store.set(store)
    return {}
