from datetime import timezone
from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import auth_register_v1, decode_jwt
from src.channels import *
import string
import re
from src import config



def channel_invite_v1(token, channel_id, u_id):
    '''
    <Invites a user with the ID u_id to a channel with the ID channel_id.
        The person is immediately added to the channel after being invited.
        All members can invite individuals in both public and private channels.>

    Arguments:
        <token> (<string>) - <string returned from auth_register and auth_login>
        <channel_id>   (<string>)    - <Channel id of the channel>
        <u_id>         (<numbers>)   - <User id of the other authorised user in the users dictionary>

    Exceptions:
        InputError  - Occurs when any of channel_id does not refer to a valid channel
                    - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user who is already a member of the channel
    
        AccessError - Occurs when channel_id is valid and the authorised user is not a member of the channel

    Return Value:
        Returns <{}> on <the fact that no exceptions are raised and valid arguments are provided.>

    '''
    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']

        
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")

    # Flags for errors
    invalid_user_flag, invalid_channel_flag, already_member_flag, not_member_flag = (False,)* 4

    #checking for a invalid u_id (InputError)
    for user in store['users']:
        if (user[0] == u_id):
            invalid_user_flag = True

    for channel in store['channels']:
        #checking for a invalid channel_id (InputError)
        if (channel[1] == channel_id):
            invalid_channel_flag = True
            
        #checking for a valid channel_id but authorised user is not a memeber of the channel (AccessError)
        if (channel[1] == channel_id) and (channel[0] == auth_user_id) :
            already_member_flag = True
        
        #checking if u_id is already a member of the channel (InputError)
        for all_mem in channel[5]:  
            if (all_mem['u_id'] == u_id):
                not_member_flag = True


    # Raises errors 
    if (invalid_user_flag == False):        
        raise InputError(description="Invalid u_id - unregistered user")

    if (invalid_channel_flag == False):        
        raise InputError(description="Channel_id does not refer to a valid channel")

    if (not_member_flag != False):        
        raise InputError(description="User is already a member of the channel")

    if (already_member_flag == False):        
        raise AccessError(description="Authorised user is not a member of the channel")

    # Add invited u_id to channel

    for user in store['users']:
        if (user[0] == u_id):
            for channel in store['channels']:
                if (channel[1] == channel_id) and (channel[0] == auth_user_id):
                    channel[5].append({'u_id': u_id, 'email': user[1],'name_first': user[3], 'name_last': user[4],'handle_str': user[5]}) 
    data_store.set(store) 


    return {
    }


def find_channel(channel_id, store):
    for channel in store['channels']:
        if channel[1] == channel_id:
            return channel


def channel_details_v1(token, channel_id):
    '''
	<return the detail of users in a specific channel>

	Arguments:
       	<token> (<string>)    - <The id of the users after they register with detail of channel>
       	<channel_id> (<int>)    - <The id of the channel which shows the detail>       

	Exceptions:
      	InputError  - Occurs when channel_id is invalid 
       	AccessError - Occurs when the authorised user is not a member of channel 

	Return Value:
	    Returns <detail of users> on <specific channels> 
    '''   
    store = data_store.get()	
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']
    channel_id = int(channel_id)
        
    #checking for invalid session_id
    session = False           
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
 
    if (session == False):
        raise AccessError(description="Invalid session_id")
    
    #checks if channel_id is valid
    if_channel = False
    for details in store['channels']:
        if details[1] == channel_id:
            if_channel = True           
    if if_channel == False:
        raise InputError(description='channel_id does not refer to a valid channel')
   
    channel = find_channel(channel_id, store)
    authorised = False
    
    #checks if user_id is a member
    for channel in store['channels']:
        for detail in channel[5] :
            if (detail['u_id'] == auth_user_id):
                authorised = True
                
    if authorised == False:
        raise AccessError(description='the authorised user is not a member of the channel')

    #return member details
    all_member = []
    owner_member = []    
    for channel in store['channels']:
        if channel[1] == channel_id:
            name = channel[2]
            if_public = channel[3]
            #for all members
            for join in channel[5]:
                all_member.append(join)
                      
            #for owner members
            for join in channel[4]:
                owner_member.append(join) 

    data_store.set(store) 
    return {
	    'name': name,
        'is_public': if_public,
        'owner_members': owner_member,
        'all_members': all_member,
    }




def channel_messages_v1(token, channel_id, start):   
    '''
    <collect and return up to 50 messages from users in a specified channel>
    	
    Arguments:
    		token -  <The id of the users after they register with detail of channel> 
    		channel_id (int) -  <The id of the channel which shows the detail>
    		start(int) -  <The index of the message which the users want to start>
    	
    Exceptions:
    		InputError - Occurs when channel_id is invalid or start is greater than total number of messages in channel
    		AccessError - Occurs when the authorised user is not a member of channel 
    	
    Return Value:
    		Return the detail of up to 50 messages with start and end 
    '''
    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']   
    channel_id = int(channel_id) 
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
   
    #checks if channel_id is valid
    current = False
    for detail in store['channels']:
        if detail[1] == channel_id:
            current = True           
    if current == False:
        raise InputError(description='channel_id does not refer to a valid channel')  
   
    channel_list = find_channel(channel_id, store)
    authorised = False
    total_messages = len(channel_list[6])
    #checks if user_id is a member
    for channel in store['channels']:
        for detail in channel[5]:
            if (detail['u_id'] == auth_user_id):
                authorised = True                
    if authorised == False:
        raise AccessError(description='the authorised user is not a member of the channel')
    
	#check if the start is greater than the total number of messages
    if start > total_messages:
        raise InputError(description='start is greater than the total number of messages in the channel')
    
    if total_messages > (start + 50):
        messages = channel_list[6][start: start + 51]
        end = start + 50
    else:
        messages =  channel_list[6][start:]
         
    data_store.set(store)
    return {
        'messages': messages,
        'start': start,
        'end': end,
    }


def channel_join_v1(token, channel_id):
    '''
    <Given a channel_id of a channel that the authorised user can join, adds them to that channel.
     Global owner should be able to use channel_join to add themselves to any channel (Public / Private).>

    Arguments:
        <token> (<string>) - <string returned from auth_register and auth_login>
        <channel_id>   (<string>)    - <Channel id of the channel>

    Exceptions:
        InputError  - Occurs when any of channel_id does not refer to a valid channel
                    - Occurs when the authorised user is already a member of the channel
        AccessError - Occurs when channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner.
    
    Return Value:
        Returns <{}> on <the fact that no exceptions are raised and valid arguments are provided.>

    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']

    # Flags for errors
    invalid_user_flag, invalid_channel_flag, already_member_flag, private_channel_flag, session = (False,) * 5

    #checking for a invalid user_id and session_id
    for user in store['users']:
        if (user[0] == auth_user_id) and (decoded_object['session_id'] in user[6]):
            session = True
            invalid_user_flag = True

    if (session == False):
        raise AccessError(description="Invalid session_id")

    for channel in store['channels']:    
        #checking for a invalid channel_id
        if (channel[1] == channel_id):
            invalid_channel_flag = True

        #checking if the authorised user is already a member of the channel
        if (channel[1] == channel_id) and (channel[0] == auth_user_id) :
            already_member_flag = True

        #checking if the Private channel and the authorised user is not already a channel member and is not a global owner
        if (channel[1] == channel_id) and (channel[3] == False) and (channel[0] != auth_user_id) :
            if(store['users'][0][0] == auth_user_id):
                private_channel_flag = False
            else:
                for member in channel[5]:
                    if (member['u_id'] != auth_user_id):
                        private_channel_flag = True

    # Raises errors
    if (invalid_channel_flag == False):        
        raise InputError(description="Channel_id does not refer to a valid channel")
    if (already_member_flag != False):        
        raise InputError(description="Authorised user is already a member of the channel")

    if (invalid_user_flag == False):        
        raise AccessError(description="Invalid user_id - unregistered user")

    if (private_channel_flag != False):        
        raise AccessError(description="Private channel and the authorised user is not already a channel member and is not a global owner")

    # Dictionary of memebers and their channels 

    for user in store['users']:
        if (user[0] == auth_user_id):
            for channel in store['channels']:
                generic_handle = "generic"        
                for image in store['images']:
                    if image['user_id'] == user[0]:
                        if image["file_address"] == 'static/' + user[5] + '.jpg':
                            generic_handle = user[5]      
                profile_img = config.url + 'static/' + generic_handle +'.jpg'
                if (channel[1] == channel_id):
                    channel[5].append({'u_id': auth_user_id, 'email': user[1], 
                    'name_first': user[3], 'name_last': user[4], 
                    'handle_str': user[5], 'profile_img_url': profile_img}) 

    data_store.set(store) 

    return {
    }

def channel_leave_v1(token, channel_id):
    '''
    <Given a channel_id of a channel that the authorised user is a member of, removes them from the channel>

    Arguments:
        <token> (<string>) - <string returned from auth_register and 
        auth_login>
        <channel_id>   (<string>)    - <Channel id of the channel>

    Exceptions:
        InputError - Occurs when any of channel_id does not refer to a valid channel
        AccessError - Occurs when there's a valid channel_id but the user is not a member of the channel. Also when the token session is invalid
    
    Return Value:
        Returns <{}> 

    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']
    channel_id = int(channel_id)

    # Flags for errors
    invalid_user_flag, invalid_channel_flag, user_not_member_flag, session = (False,) * 4

    #checking for a invalid user_id and session_id
    for user in store['users']:
        if (user[0] == auth_user_id) and (decoded_object['session_id'] in user[6]):
            session = True
            invalid_user_flag = True

    if (session == False):
        raise AccessError(description="Invalid session_id")

    for channel in store['channels']:    
        #checking for a invalid channel_id
        if (channel[1] == channel_id):
            invalid_channel_flag = True
        for member in channel[5]:
            if (member['u_id'] == auth_user_id):
                user_not_member_flag = True
            

    # Raises errors
    if (invalid_channel_flag == False):        
        raise InputError(description="Channel_id does not refer to a valid channel")

    if (user_not_member_flag == False):
        raise AccessError(description="user not member of channel given")

    if (invalid_user_flag == False):        
        raise AccessError(description="Invalid user_id - unregistered user")

    # Removing member from channel 
    for channel in store['channels']:
        if (channel[1] == channel_id):
            channel[5] = [i for i in channel[5] if not (i['u_id'] == auth_user_id)]
            channel[4] = [i for i in channel[4] if not (i['u_id'] == auth_user_id)]
                 
    
    data_store.set(store) 

    return {}
    
def channel_addowner_v1(token, channel_id, u_id):
    '''
    <Given a channel_id of a channel that the authorised user is an owner of, adds the u_id as another owner>

    Arguments:
        <token> (<string>) - <string returned from auth_register and 
        auth_login>
        <channel_id>   (<string>)    - <Channel id of the channel>
        <u_id>  (<string>) - converted to an integer, user_id of member

    Exceptions:
        InputError - Occurs when any of channel_id does not refer to a valid channel, u_id is invalid, u_id refers to someone who is not a member, or if u_id is a user who is already an owner
        AccessError - Occurs when there's a valid channel_id but the authorised user is not an owner of the channel. Also when the token session is invalid
    
    Return Value:
        Returns <{}> 

    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']
    channel_id = int(channel_id)
    u_id = int(u_id)

    # Flags for errors
    invalid_user_flag, invalid_channel_flag, user_not_member_flag, u_id_owner_flag, auth_user_owner_permissions, session = (False,) * 6

    #checking for a invalid u_id and session_id
    for user in store['users']:
        if (user[0] == u_id):
            invalid_user_flag = True 
        
        if (decoded_object['session_id'] in user[6]):
            session = True

    if (session == False):
        raise AccessError(description="Invalid session_id")

    for channel in store['channels']:    
        #checking for a invalid channel_id
        if (channel[1] == channel_id):
            invalid_channel_flag = True
        for member in channel[5]:
            if (member['u_id'] == u_id):
                user_not_member_flag = True
        for owner in channel[4]:
            if (owner['u_id'] == u_id):
                u_id_owner_flag = True
            if (owner['u_id'] == auth_user_id):
                auth_user_owner_permissions = True      
            

    # Raises errors
    if (u_id_owner_flag == True):
        raise InputError(description="user with u_id is already an owner")
    
    if (invalid_channel_flag == False):        
        raise InputError(description="Channel_id does not refer to a valid channel")

    if (invalid_user_flag == False):        
        raise InputError(description="Invalid user_id - unregistered user")
        
    if (user_not_member_flag == False):
        raise InputError(description="user not member of channel given")
    
    if (auth_user_owner_permissions == False):
        raise AccessError(description="user of the token inputted is not an owner")
    
    # Adding member as an owner from channel 
    new_owner = {}
    for channel in store['channels']:
        if (channel[1] == channel_id):
            for member in channel[5]:
                if member['u_id'] == u_id:
                    new_owner = member
            channel[4].append(new_owner)
            break
                 
    
    data_store.set(store) 

    return {
        
    }
    
def channel_removeowner_v1(token, channel_id, u_id):
    '''
    <Given a channel_id of a channel that the authorised user is an owner of, removes the u_id as an owner>

    Arguments:
        <token> (<string>) - <string returned from auth_register and 
        auth_login>
        <channel_id> (<string>) - <Channel id of the channel>
        <u_id>  (<string>) - converted to an integer, user_id of owner

    Exceptions:
        InputError - Occurs when any of channel_id does not refer to a valid channel, u_id is invalid, u_id refers to someone who is not an owner, or if u_id is a user who is the only owner
        AccessError - Occurs when there's a valid channel_id but the authorised user is not an owner of the channel. Also when the token session is invalid
    
    Return Value:
        Returns <{}> 

    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']
    channel_id = int(channel_id)
    u_id = int(u_id)

    # Flags for errors
    invalid_user_flag, invalid_channel_flag, u_id_owner_flag, auth_user_owner_permissions, session = (False,) * 5

    #checking for a invalid u_id and session_id
    for user in store['users']:
        if (user[0] == u_id):
            invalid_user_flag = True 
        
        if (decoded_object['session_id'] in user[6]):
            session = True

    if (session == False):
        raise AccessError(description="Invalid session_id")

    for channel in store['channels']:    
        #checking for a invalid channel_id
        if (channel[1] == channel_id):
            invalid_channel_flag = True
        for owner in channel[4]:
            if (owner['u_id'] == u_id):
                u_id_owner_flag = True
            if (owner['u_id'] == auth_user_id):
                auth_user_owner_permissions = True      
            

    # Raises errors
    if (u_id_owner_flag == False):
        raise InputError(description="user with u_id is not an owner")
    
    for channel in store['channels']:
        if (len(channel[4]) == 1) and (u_id_owner_flag == True):
            raise InputError(description="u_id is the only owner of the channel")       
    
    if (invalid_channel_flag == False):        
        raise InputError(description="Channel_id does not refer to a valid channel")
    
    if (invalid_user_flag == False):        
        raise InputError(description="Invalid user_id - unregistered user")
    
    if (auth_user_owner_permissions == False):
        raise AccessError(description="user of the token inputted is not an owner")
    
    # Removing member from channel 
    for channel in store['channels']:
        if (channel[1] == channel_id):
            channel[4] = [i for i in channel[4] if not (i['u_id'] == u_id)]
                 
    
    data_store.set(store) 

    return {}
