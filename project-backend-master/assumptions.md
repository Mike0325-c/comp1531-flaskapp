**Project** 

***iteration 1***

**auth**

auth_login_v1

1. The password is of an appropriate max length as was not accounted for

auth_register_v1

1. The password is no longer than 50 characters
2. The first and last name don't include any mathematical symbols etc, 
as I tested for punctuation and extra spaces and dashes but not symbols like '%, @' 

**channels**

channels_create_v1

1. Channels can have same names but different channel_id.
2. An exception (Access error) is raised if channel is created by an unregistered user.

channels_list_v1

1. Given the auth_user_id, the user can list all channels they are an owner of 
or a member of. I have assumed here that the user does not have to be an owner to 
list the channels.  

channels_listall_v1
1. I assumed that the user_id given was valid, if not that than I raised an InputError

**channel**

channel_invite_v1

1. I assume that it is not important to be the owner to invite new registered users.

channel_join_v1

1. I assume that the registered user can only join a public channel if they have its channel_id. 
2. Only the global owner is allowed to join both public and private channels but the other registered user needs to be invited to a private channel.

channel_details_v1
1. I assume that the auth_user_id should be the member of the channel_id it does not have to be the owner. 

channel_leave_v1
1. Assumed that if the member is an owner, they are removed but the channel still exists. Spec is not explicit on this, where it says that "If the only channel owner leaves, the channel will remain", and in channel_removeowner, the only owner remains.
2. If the user is an owner as well as a member they leave both

**user**

users_all_v1
1. token is active


**other**

1. add some lists or objects

**data_store**

1. add some lists or objects

**dm**

dm_create_v1
 • I assume that the Access error is raised if the token is invalid.
 • I assume that u_ids are auth_user_id not tokens.
 • I assume that the name handle does not need to be converted to lowercase and neither does it have to handle duplicate handles.
 • I assume that if the u_ids is empty the function will still create a DM with just itself in it

dm_details_v1
 • I assume that return type name should be a string not list.
 • I assume that return type members contains data of users and can be portrayed in any order.

dm_list_v1
 • I assume that the return for this function is a list of dictionary where name key contains string value not list

dm_remove_v1
 • I assume that the global owner cannot remove the DM

dm_leave_v1
 • I assume that  when the creator of the DM leaves the DM cannot be removed

** message**

message_send_v1
 1. iuputerror occurs when channel_id is invalid and message is too long or too short
 2. each message should return a unique message_id
 3. access error occurs when user is not a member of channel
 4. should return a dict with unique message_id 

message_edit_v1
1. update its text with new text,when message is empty, should remove it
2. inputerror occur when token and message_id are invalid

message_remove_v1
1. remove the message with a special message_id















