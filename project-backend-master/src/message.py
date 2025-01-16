from datetime import timezone, datetime
from src.error import InputError, AccessError
from src.auth import decode_jwt
from src.data_store import data_store



def find_channel(channel_id, store):
    for channel in store['channels']:
        if channel[1] == channel_id:
            return channel

def find_dm(dm_id, store):
    for dm in store['dm']:
        if dm[1] == dm_id:
            return dm

def message_send_v1(token, channel_id, message):
    '''
    <Send a message from the authorised user to the channel specified by channel_id.>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <channel_id> (<List>)   - <A integer uesd to identify a channel>
        <message> (<string>) - <string used to send to channel>

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        InputError  - Occurs when length of message is less than 1 or over 1000 characters
        AccessError - Occurs when the authorised user is not a member of the channel

    Return Value:
        Returns <messages_id> : a dict contained message_id

    '''
    store = data_store.get()

    # InputError1: message is too long or too short
    if len(message) > 1000:
        raise InputError(description='Message is longer than 1000 characters')
    if len(message) < 1:
        raise InputError(description='Message is smaller than 1 characters')

    author = decode_jwt(token)



    # InputError3: invalid channel
    result = False
    for channel in store['channels']:
        if channel[1] == channel_id:
            result = True
    if result == False:
        raise InputError(
            description='channel_id does not refer to a valid channel')

    # AccessError1: the authorised user is not a member
    auth_user_id = author['user_id']
    channel = find_channel(channel_id, store)
    authorised = False
    # checks if user_id is a member
    for channel in store['channels']:
        for detail in channel[5]:
            if (detail['u_id'] == auth_user_id):
                authorised = True

    if authorised == False:
        raise AccessError(
            description='the authorised user is not a member of the channel')

    new_message_id = 1
    for channel in store['channels']:
        if len(channel[6]) != 0:
            new_message_id = channel[6][0]['message_id'] + 1

    # check the time
    timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    
    return_messages = {
        'message_id': new_message_id,
        'channel_id': channel_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': timestamp,
		'is_pinned': False,
        'reacts': [],
    }

    for i in store['channels']:
        if i[1] == channel_id:
            i[6].append(return_messages)

    data_store.set(store)
    return {
        'message_id': new_message_id,
    }

def message_senddm_v1(token, dm_id, message):
    '''
    <Send a message from the authorised user to the dm specified by dm_id.>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <dm_id> (<List>)   - <A integer uesd to identify a dm>
        <message> (<string>) - <string used to send to channel>

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        InputError  - Occurs when length of message is less than 1 or over 1000 characters
        AccessError - Occurs when the authorised user is not a member of the channel

    Return Value:
        Returns <messages_id> : a dict contained message_id

    '''
    store = data_store.get()
    dm_id = int(dm_id) 
    # InputError1: message is too long or too short
    if len(message) > 1000:
        raise InputError(description='Message is longer than 1000 characters')
    if len(message) < 1:
        raise InputError(description='Message is smaller than 1 characters')

    # InputError3: invalid dm
    result = False
    for dm in store['dm']:
        if dm[1] == dm_id:
            result = True
    if result == False:
        raise InputError(
            description='dm_id does not refer to a valid dm')

    # AccessError1: the authorised user is not a member
    author = decode_jwt(token)
    auth_user_id = author['user_id']
    dm = find_dm(dm_id, store)
    authorised = False
    # checks if user_id is a member
    for dm in store['dm']:
        for detail in dm[4]:
            if (detail['u_id'] == auth_user_id):
                authorised = True

    if authorised == False:
        raise AccessError(
            description='the authorised user is not a member of the dm')

    new_message_id = 1
    for dm in store['dm']:
        if len(dm[5]) != 0:
            new_message_id = dm[5][0]['message_id'] + 1

    # check the time
    timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    
    messages_return = {
        'message_id': new_message_id,
        'dm_id': dm_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': timestamp,
		'is_pinned': False,
        'reacts': [],
    }

    for i in store['dm']:
        if i[1] == dm_id:
            i[5].append(messages_return)

    data_store.set(store)
    return {
        'message_id': new_message_id,
    }

def message_edit_v1(token, message_id, message):
    '''
    <Given a message, update its text with new text. If the new message is an empty string, the message is deleted.>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <message_id> (<integer>)   - <a unique ID a message have>
        <message> (<string>) - <string used to send to channel>

    Exceptions:
        InputError  - Occurs when any oflength of message too large
        InputError  - Occurs when message_id does not refer to a valid message
        AccessError - Occurs when the message was sent by the authorised user
        AccessError - Occurs when the authorised user has owner permissions in the channel/DM
    Return Value:
        Returns <{}>

    '''
    store = data_store.get()

    # InputError1: message is too long
    if len(message) > 1000:
        raise InputError(description='Message is longer than 1000 characters')

    # InputError2: message_id does not refer to a valid message
    boolean = False
    for channel in store['channels']:
        for i in channel[6]:
            if i['message_id'] == message_id:
                boolean = True
    if boolean == False:
        raise InputError(
            description='message_id does not refer to a valid message ')
        # AccessError
    author = decode_jwt(token)
    u_id = author['user_id']

    channel_id = 0
    # gets channel_id from message_id
    for channel in store['channels']:
        if channel[6][0]['message_id'] == int(message_id):
            channel_id = channel[1]

    author = False
    get_channel = find_channel(channel_id, store)
    for j in get_channel[4]:
        if j['u_id'] == u_id:
            author = True
    for i in channel[6]:
        if author is False and i['u_id'] != u_id:
            raise AccessError(
                description='the message was sent by the authorised user making this request')

    for nmsg in store['channels']:
        for messages in nmsg[6]:
            if messages.get("message_id") is message_id:
                if not message:
                    messages['message'] = " "
                    break
                # replace the current message with the message we want
                else:
                    messages["message"] = message

    data_store.set(store)

    return {}


def message_remove_v1(token, message_id):
    '''
    <Given a message_id for a message, this message is removed from the channel/DM>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <message_id> (<integer>)   - <a unique ID a message have>

    Exceptions:
        InputError  - Occurs when message_id does not refer to a valid message
        InputError  - Occurs when length of message is less than 1 or over 1000 characters
        AccessError - Occurs when the message was sent by the authorised user
        AccessError - Occurs when the authorised user has owner permissions in the channel/DM

   Return Value:
        Returns <{}>

    '''
    author = decode_jwt(token)
    store = data_store.get()
    # InputError1: invalid token
    u_id = author.get('u_id')


    # InputError2: message_id does not refer to a valid message
    bool = False
    for channel in store['channels']:
        for i in channel[6]:
            if i['message_id'] == message_id:
                bool = True
    if bool == False:
        raise InputError(
            description='message_id does not refer to a valid message ')

    # AccessError
    author = decode_jwt(token)
    u_id = author.get('u_id')

    channel_id = 0
    # gets channel_id from message_id
    for channel in store['channels']:
        if channel[6][0]['message_id'] == int(message_id):
            channel_id = channel[1]

    author = False
    get_channel = find_channel(channel_id, store)

    for j in get_channel[4]:
        if j['u_id'] == u_id:
            author = True
    for i in channel[6]:
        if author is False and i['u_id'] == u_id:
            raise AccessError(
                description='the message was not sent by the authorised user making this request')
    data_store.set(store)

    for msg in store['channels']:
        if msg[1] == channel_id:
            for msg1 in msg[6]:
               if msg1['message_id'] == message_id:
                   msg1['message'] = ""

    data_store.set(store)

    return {}

def message_react_v1(token, message_id, react_id):
    '''
    <add a "react" to that particular message>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <message_id> (<integer>)   - <a unique ID a message have>
        <react_id> (<integer>)   - <a ID a message which is reacted>
    
    Exceptions:
        InputError  - Occurs when message_id is not a valid message
        InputError  - Occurs when react_id is not a valid react ID
        InputError - Occurs when the message already contains a react with ID react_id 
        
   Return Value:
        Returns <{}>
    '''      
    store = data_store.get()
    #decoded_object = decode_jwt(token)

   
    #invalid message_id
    msg_check = False   
    for channel in store["channels"]:
        for message in channel[6]:
            if message["message_id"] == message_id:
                msg_check = True
    if msg_check == False:
        raise InputError(description='Message id is not a valid')
    
    #invalid react_id
    if react_id != 1:
        raise InputError(description="react_id is not a valid react ID ")   
   
    
    data_store.set(store) 
   
    return{}


def message_unreact_v1(token, message_id, react_id):
    '''
    <remove a "react" to that particular message>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <message_id> (<integer>)   - <a unique ID a message have>
        <react_id> (<integer>)   - <a ID a message which is reacted>
    
    Exceptions:
        InputError  - Occurs when message_id is not a valid message
        InputError  - Occurs when react_id is not a valid react ID
        InputError - Occurs when the message does not contain a react with ID react_id
        
   Return Value:
        Returns <{}>
    '''    
    store = data_store.get()
    decoded_object = decode_jwt(token)
    auth_user_id = decoded_object['user_id']   
    
    #invalid message_id
    msg_check = False   
    for channel in store["channels"]:
        for message in channel[6]:
            if message["message_id"] == message_id:
                msg_check = True
    if msg_check == False:
        raise InputError(description='Message id is not a valid')
    
    #invalid react_id
    if react_id != 1:
        raise InputError(description="react_id is not a valid react ID ")    
    
    #the message does not contain a react with ID react_id from the authorised user
    for channel in store['channels']:
        for message in channel[6]:
            if auth_user_id not in message["u_id"]:
                raise InputError(description='the message does not contain a react with ID react_id from the authorised user')
      
    data_store.set(store)
   
    return{}

def message_pin_v1(token, message_id):        
   '''
    <Given a message within a channel or DM, mark it as "pinned">

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <message_id> (<integer>)   - <a unique ID a message have>

    Exceptions:
        InputError  - Occurs when when message_id does not refer to a valid message
        InputError  - Occurs when the message is already pinned
        AccessError - Occurs when the authorised user does not have owner permissions in the channel/DM
        
   Return Value:
        Returns <{}>
    '''      
   
   store = data_store.get()
   decoded_object = decode_jwt(token)
   auth_user_id = decoded_object['user_id']
   message_id = int(message_id)
   
   #invalid message_id
   msg_check = False   
   for channel in store["channels"]:
       for message in channel[6]:
           if message["message_id"] == message_id:
               msg_check = True
   if msg_check == False:
       raise InputError(description='Message id is not a valid')
         
   #the message is already pinned
   for channel in store['channels']:
       for message in channel[6]:  
           if message["message_id"] == message_id: 
               if message["is_pinned"] == True: 
                   raise InputError(description= "This message is already pinned")
 
   for channel in store['channels']:
       for channel_msg in channel[6]:
           if channel_msg['message_id'] == message_id:
               members = False
               for member in channel[5]:
                   if member['u_id'] == auth_user_id:
                       members = True
               owners = False
               for owner in channel[4]:
                   if owner['u_id'] == auth_user_id:
                       owners = True
               if members is False or owners is False:
                   raise AccessError(
                       description="the authorised user does not have owner permissions in the channel")
                                                     
       for channel_msg in channel[6]:
           if channel_msg['message_id'] == message_id:
               members = False
               for member in channel[5]:
                   if member['u_id'] == auth_user_id:
                       members = True
               owners = False
               for owner in channel[4]:
                   if owner['u_id'] == auth_user_id:
                       owners = True
               if members is False or owners is False:
                   raise AccessError(
                       description="the authorised user does not have owner permissions in the channel")
                              
	#mark it as "pinned"
   for channel in store["channels"]: 
       for message in channel[6]: 
           if message.get("message_id") == message_id: 
               message["is_pinned"] = True
    
   data_store.set(store) 
   
   return{}
                   
def message_unpin_v1(token, message_id):   
   '''
    <Given a message within a channel or DM, remove its mark as pinned>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <message_id> (<integer>)   - <a unique ID a message have>

    Exceptions:
        InputError  - Occurs when when message_id does not refer to a valid message
        InputError  - Occurs when the message is not already pinned
        AccessError - Occurs when the authorised user does not have owner permissions in the channel/DM
        
   Return Value:
        Returns <{}>
    '''      
   
   store = data_store.get()
   decoded_object = decode_jwt(token)
   auth_user_id = decoded_object['user_id']
   message_id = int(message_id)
   
   #invalid message_id
   msg_check = False   
   for channel in store["channels"]:
       for message in channel[6]:
           if message["message_id"] == message_id:
               msg_check = True
   if msg_check == False:
       raise InputError(description='Message id is not a valid')
         
   #the message is not pinned
   for channel in store['channels']:
       for message in channel[6]:  
           if message["message_id"] == message_id: 
               if message["is_pinned"] == False: 
                   raise InputError(description= "This message is not pinned")
 
   for channel in store['channels']:
       for channel_msg in channel[6]:
           if channel_msg['message_id'] == message_id:
               members = False
               for member in channel[5]:
                   if member['u_id'] == auth_user_id:
                       members = True
               owners = False
               for owner in channel[4]:
                   if owner['u_id'] == auth_user_id:
                       owners = True
               if members is False or owners is False:
                   raise AccessError(
                       description="the authorised user does not have owner permissions in the channel")
                              
	#mark it as "unpinned"
   for channel in store["channels"]: 
       for message in channel[6]: 
           if message.get("message_id") == message_id: 
               message["is_pinned"] = False
    
   data_store.set(store) 
   
   return{}

def message_sendlater_v1(token, channel_id, message, time_sent):
   '''
    <Send a message from the authorised user to the channel at a specified time in the future>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <channel_id> (<integer>)   - <a unique ID a channel have>
		<message> (<string>) - < the unique message>
        <time_sent> (<integer>)   - <the time messages will send>

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        InputError  - Occurs when length of message is over 1000 characters
        InputError  - Occurs when time_sent is a time in the past
        AccessError - Occurs when authorised user is not a member of the channel they are trying to post to
        
   Return Value:
        Returns <{message_id}>
    '''   
   store = data_store.get()
   decoded_object = decode_jwt(token)
   auth_user_id = decoded_object['user_id']
   
   #invalid_channel   
   result = False
   for channel in store['channels']:
       if channel[1] == channel_id:
           result = True
   if result == False:
       raise InputError(
           description='channel_id does not refer to a valid channel')
   #message is too long
   if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")
   
   #time is in the past
   timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
   if time_sent < timestamp: 
        raise InputError(description= "time_sent is a time in the past")

   channel = find_channel(channel_id, store)
   authorised = False
    
   #checks if user_id is a member
   for channel in store['channels']:
       for detail in channel[5] :
           if (detail['u_id'] == auth_user_id):
               authorised = True
   if authorised == False:
       raise AccessError(description='the authorised user is not a member of the channel')
   
   
   message_id = message_send_v1(token, channel_id, message)["message_id"]
    
   data_store.set(store) 
   
   return {"message_id" : message_id}
   
def message_sendlaterdm_v1(token, dm_id, message, time_sent):
   '''
    <Send a message from the authorised user to the dm at a specified time in the future>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <dm_id> (<integer>)   - <a unique ID a dm have>
		<message> (<string>) - < the unique message>
        <time_sent> (<integer>)   - <the time messages will send>

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        InputError  - Occurs when length of message is over 1000 characters
        InputError  - Occurs when time_sent is a time in the past
        AccessError - Occurs when authorised user is not a member of the channel they are trying to post to
        
   Return Value:
        Returns <{message_id}>
    '''   
   store = data_store.get()
   decoded_object = decode_jwt(token)
   auth_user_id = decoded_object['user_id']
   dm_id = int(dm_id) 
   #invalid_channel   
   result = False
   for dm in store['dm']:
       if dm[1] == dm_id:
           result = True
   if result == False:
       raise InputError(
           description='dm_id does not refer to a valid DM')
   #message is too long
   if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")
   
   #time is in the past
   timestamp = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
   if time_sent < timestamp: 
        raise InputError(description= "time_sent is a time in the past")

   dm = find_dm(dm_id, store)
   authorised = False
    
   #checks if user_id is a member
   for dm in store['dm']:
       for detail in dm[4] :
           if (detail['u_id'] == auth_user_id):
               authorised = True
   if authorised == False:
       raise AccessError(description='the authorised user is not a member of the dm')
   
   
   message_id = message_senddm_v1(token, dm_id, message)["message_id"]
    
   data_store.set(store) 
   
   return {"message_id" : message_id}
    
def search_v1(token, query_str):
    '''
    <Send a message from the authorised user to the dm at a specified time in the future>

    Arguments:
        <token> (<string>) - < jwt encoded string>
        <query_str> (<integer>)   - <a unique ID a dm have>


    Exceptions:
        InputError  - Occurs when length of query_str is less than 1 or over 1000 characters
        
   Return Value:
        Returns <{messages}>
    '''
    store = data_store.get()
    decoded_object = decode_jwt(token)
    list_channels = []
    list_dm = []
    list_message = []
    auth_user_id = decoded_object['user_id']
    
    #checking for an invalid session_id
    session = False
    for user in store['users']:
        if (decoded_object['session_id'] in user[6]):
            session = True
    
    if (session == False):
        raise AccessError(description="Invalid session_id")
        
    # InputError1: query_str is too long or too short
    if len(query_str) > 1000:
        raise InputError(description='Message is longer than 1000 characters')
    if len(query_str) < 1:
        raise InputError(description='Message is smaller than 1 characters')
    
    for channel in store['channels']:
        for mem in channel[5]:
            if (mem['u_id'] == auth_user_id):
               list_channels.append(channel[1])
    
    for dm in store['dm']:
        for mems in dm[4]:
            if (mems['u_id'] == auth_user_id):
               list_dm.append(dm[1])
    
    query_str = query_str.lower()
    query_str = "".join(query_str.split())
    
    for ch in store['channels']:
        for chan in ch[6]:
            if chan['channel_id'] in list_channels:
                check = "".join(chan['message'].upper().split())
                if query_str in check:
                    found_message_ch = {
                        "message_id" : chan['message_id'],
                        "u_id" : chan['u_id'],
                        "message" : chan['message'],
                        "time_created" : chan['time_created'],
                        'reacts': chan['reacts'],
                        'is_pinned': chan['is_pinned'],
                    }
                    list_message.append(found_message_ch)
                
    for dm in store['dm']:
        for dms in dm[5]:
            if dms['dm_id'] in list_dm:
                check2 = "".join(dms['message'].upper().split())
                if query_str in check2:
                    found_message_dm = {
                        "message_id" : dms['message_id'],
                        "u_id" : dms['u_id'],
                        "message" : dms['message'],
                        "time_created" : dms['time_created'],
                        'reacts': dms['reacts'],
                        'is_pinned': dms['is_pinned']
                    }
                    list_message.append(found_message_dm)
    return {
        'messages': list_message
    }
