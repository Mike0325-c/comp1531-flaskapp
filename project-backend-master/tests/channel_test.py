'''
import pytest

from src.channel import channel_invite_v1, channel_details_v1,channel_messages_v1, channel_join_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1

#1. Tests for channel_details_v1: InputError raises when channel_id is invalid
def test_channel_details_v1_invaild_channel():
    clear_v1()
    register = auth_register_v1('JiaJun@yahoo.com', 'password', 'Andy','MingHao')
    channels_create_v1(register['auth_user_id'], 'detail_channel', False)
	
    with pytest.raises(InputError):
	    channel_details_v1(register['auth_user_id'], 'IncorrectId')
	    channel_details_v1(register['auth_user_id'], 123456)

#2. Tests for channel_details_v1: AccessError raises when the authorised user is not a member of the channel
def test_channel_details_v1_is_not_member():
    clear_v1()
    register = auth_register_v1('Mingtao@yahoo.com', 'password', 'LiuAn','TiNa')
    register2 = auth_register_v1('LiuChao@yahoo.com', 'passwords', 'Chao','Theshy')
    channel2 = channels_create_v1(register2['auth_user_id'], 'detail_channel2', True)
	
    with pytest.raises(AccessError):
	    channel_details_v1(register['auth_user_id'], channel2['channel_id'])

#3. Tests for invalid channel_id which doesn't match one returned when creating channel
def test_channel_invite_invaild_channel_id():
    clear_v1()
    login1 = auth_register_v1('Goodemail@yahoo.com', 'passwordone', 'Shaggy','Wilson')
    channels_create_v1(login1['auth_user_id'], 'channels', True)
    login2 = auth_register_v1('bademail@yahoo.com', 'passworone', 'Scooby','doo')
    
    with pytest.raises(InputError):
	    channel_invite_v1(login1['auth_user_id'], 3025, login2['auth_user_id'])
	    channel_invite_v1(login1['auth_user_id'], 5, login2['auth_user_id'])

#4. Tests for invalid u_id being passed into channel_invite 
def test_channel_invite_invaild_u_id():
    clear_v1()
    login1 = auth_register_v1('Crystal@gmail.com', 'laptop', 'Crystal', 'Smith')
    channel = channels_create_v1(login1['auth_user_id'], 'channelid', False)	
	
    with pytest.raises(InputError):
	    channel_invite_v1(login1['auth_user_id'],  channel['channel_id'], 6900)
	    channel_invite_v1(login1['auth_user_id'],  channel['channel_id'], 77)
	    channel_invite_v1(login1['auth_user_id'],  channel['channel_id'], 'jjy')

#5. Tests for inviting a member which is already a member of the channel
def test_channel_invite_already_member():
    clear_v1()
    login1 = auth_register_v1('YaoJian@gmail.com', 'computer', 'Jane', 'Smith')
    channel = channels_create_v1(login1['auth_user_id'], 'channelmember', True)	
	
    with pytest.raises(InputError):
	    channel_invite_v1(login1['auth_user_id'], channel['channel_id'], login1['auth_user_id'])

#6. Tests for when a non_member tries to invite a user to the channel		
def test_channel_invite_is_not_member():
    clear_v1()
    login1 = auth_register_v1('Jiayang@yahoo.com', 'password', 'LiuTao','mike')
    other_login1 = auth_register_v1('other_jiayang@yahoo.com', 'passwordtwo', 'Rai','David')
    login2 = auth_register_v1('Crystal@gmail.com', 'laptop', 'Crystal', 'Smith')
    channel = channels_create_v1(login1['auth_user_id'], 'channel_not', False)	
    with pytest.raises(AccessError):
	    channel_invite_v1(other_login1['auth_user_id'], channel['channel_id'], login2['auth_user_id'])

#7. Tests for when invalid channel is passed into channel_join
def test_channel_join_v1_invaild_channel():	
    clear_v1()
    register1 = auth_register_v1('JiangMin@yahoo.com', 'passwordone', 'Luxi','Faker')
    register2 = auth_register_v1('JianZhou@yahoo.com', 'passwordtwo', 'Alice','Alex')
    register3 =	auth_register_v1('Hayden@yahoo.com', 'passwordthree', 'TangSan','YunChe')
    channels_create_v1(register1['auth_user_id'], 'detail_channel4', True)
    channels_create_v1(register2['auth_user_id'], 'detail_channel5', False)
    channels_create_v1(register3['auth_user_id'], 'detail_channel6', True)
	
    with pytest.raises(InputError):
	    channel_join_v1(register1['auth_user_id'], 555)
	    channel_join_v1(register2['auth_user_id'], 54)
	    channel_join_v1(register3['auth_user_id'], 5555)

#8. Tests for when a user that is already part of the channel tries to join it again
def test_channel_join_v1_already_member():	
    clear_v1()
    register1 = auth_register_v1('JiangMin@yahoo.com', 'passwordone', 'Luxi','Faker')
    register2 = auth_register_v1('JianZhou@yahoo.com', 'passwordtwo', 'Alice','Alex')
    register3 =	auth_register_v1('Hayden@yahoo.com', 'passwordthree', 'TangSan','YunChe')
    channel1 = channels_create_v1(register1['auth_user_id'], 'detail_channel4', True)
    channel2 = channels_create_v1(register2['auth_user_id'], 'detail_channel5', False)
    channel3 = channels_create_v1(register3['auth_user_id'], 'detail_channel6', True)
	
    with pytest.raises(InputError):
	    channel_join_v1(register1['auth_user_id'], channel1['channel_id'])
	    channel_join_v1(register2['auth_user_id'], channel2['channel_id'])
	    channel_join_v1(register3['auth_user_id'], channel3['channel_id'])

#9. Tests for when a non-member tries to join a private channel
def test_channel_join_v1_is_not_member():	
    clear_v1()
    auth_register_v1('JiangMin@yahoo.com', 'passwordone', 'Luxi','Faker')
    register2 = auth_register_v1('JianZhou@yahoo.com', 'passwordtwo', 'Alice','Alex')
    register3 =	auth_register_v1('Hayden@yahoo.com', 'passwordthree', 'TangSan','YunChe')	
    register4 =	auth_register_v1('MingtKao@yahoo.com', 'passwordX', 'Anly','Apple')
    channel_is_private = channels_create_v1(register4['auth_user_id'], 'detail_channel0', False)
	
    with pytest.raises(AccessError):
	    channel_join_v1(register2['auth_user_id'], channel_is_private['channel_id'])
	    channel_join_v1(register3['auth_user_id'], channel_is_private['channel_id'])

#10. Tests for when a global owner tries to join a channel		    
def test_channel_join_v1_is_global_owner():	
	clear_v1()
	register1 = auth_register_v1('JiangMin@yahoo.com', 'passwordone', 'Luxi','Faker')
	register4 =	auth_register_v1('MingtKao@yahoo.com', 'passwordX', 'Anly','Apple')
	channel_is_private = channels_create_v1(register4['auth_user_id'], 'detail_channel0', False)

	assert(channel_join_v1(register1['auth_user_id'], channel_is_private['channel_id']) == {})

#11. Tests for channel_messages_v1: InputError raises when channel_id is invalid
def test_channel_messages_v1_invalid_channel():
	clear_v1()
	register1 = auth_register_v1('JiangMin@yahoo.com', 'passwordone', 'Luxi', 'Faker')
	register2 = auth_register_v1('JianZhou@yahoo.com', 'passwordtwo', 'Alice', 'Alex')
	
	with pytest.raises(InputError):
		channel_messages_v1(register1['auth_user_id'], 4354, 0)
		channel_messages_v1(register2['auth_user_id'], 674, 0)

#12. Tests for channel_messages_v1: InputError raises when start is greater than the number of the messages	
def test_channel_messages_v1_too_greater():
	clear_v1()
	register1 = auth_register_v1('MingChen@yahoo.com', 'password_chen', 'Orange', 'Blue')	
	channel_true = channels_create_v1(register1['auth_user_id'], 'detail_channels', True)	
	
	with pytest.raises(InputError):
		channel_messages_v1(register1['auth_user_id'], channel_true['channel_id'], 10000)

#13. Tests for channel_messages_v1: AccessError raises when the authorised user is not a member of the channel			
def test_channel_messages_v1_is_not_member():
	clear_v1()
	register1 = auth_register_v1('JiangMin@yahoo.com', 'passwordone', 'Luxi', 'Faker')
	register2 = auth_register_v1('JianZhou@yahoo.com', 'passwordtwo', 'Alice', 'Alex')
	auth_register_v1('Hayden@yahoo.com', 'passwordthree', 'TangSan', 'YunChe')	
	register4 =	auth_register_v1('MingtKao@yahoo.com', 'passwordX', 'Anly', 'Apple')
	channel_other= channels_create_v1(register4['auth_user_id'], 'message_chan', False)	
	
	with pytest.raises(AccessError):
		channel_messages_v1(register1['auth_user_id'], channel_other['channel_id'], 0)
		channel_messages_v1(register2['auth_user_id'], channel_other['channel_id'], 0)
		channel_messages_v1(register2['auth_user_id'], channel_other['channel_id'], 0)

#14. Tests for channel_invite_v1: Test if the global member is invited
def test_inviting_global_member():
    clear_v1()
    user_woody = auth_register_v1('sheriff.woody@andysroom.com', 'qazwsx!!', 'sheriff',\
     'woody')
    user_zerg = auth_register_v1('zerg.thedestroyer@zergworld.com', '!!qazwsx', 'lord',\
     'zerg')
    channel_data = channels_create_v1(user_woody['auth_user_id'], 'woodys toybox', True)
    channel_invite_v1(user_woody['auth_user_id'], channel_data['channel_id'], user_zerg['auth_user_id'])
    ch_deets = channel_details_v1(user_zerg['auth_user_id'], channel_data['channel_id'])
    
    assert user_zerg['auth_user_id'] in [k['u_id'] for k in ch_deets['all_members']]
    
#15. Tests for channel_messages_v1: Empty list is returned when start is 0	
def test_channel_messages_v1_start_zero():
	clear_v1()
	register1 = auth_register_v1('MingChen@yahoo.com', 'password_chen', 'Orange', 'Blue')	
	channel_true = channels_create_v1(register1['auth_user_id'], 'detail_channels', True)
	ch_msgs = channel_messages_v1(register1['auth_user_id'], channel_true['channel_id'], 0)
	assert ch_msgs['start'] == 0
	assert ch_msgs['end'] == -1
	assert ch_msgs['messages'] == []
'''
