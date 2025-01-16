'''
import pytest

from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1

#1. Tests if the channels_create_v1 successfully creates a channel 
def test_channel_create_successful():
    clear_v1()
    name = 'andys room'
    user_zerg = auth_register_v1('zerg.thedestroyer@zergworld.com', '!!qazwsx', 'lord',\
     'zerg')
    channel_data = channels_create_v1(user_zerg['auth_user_id'], 'andys room', False)
    deets = channel_details_v1(user_zerg['auth_user_id'], channel_data['channel_id'])
    assert deets['name'] == name
    assert user_zerg['auth_user_id'] in [memb['u_id'] for memb in deets['owner_members']]
    assert(channel_data['channel_id'] == 1)


#2. Tests when the valid arguments are provided it creates the channel id.
def test_channel_create_valid():
    clear_v1()
    dev_data = auth_register_v1('dev.bhimsaria@gmail.com', 'dev123#', 'dev',\
     'bhimsaria')
    channel_data = channels_create_v1(dev_data['auth_user_id'], 'Channel', True)
    assert(channel_data['channel_id'] == 1)

#3. Tests if it raises InputError when provided an empty channel name.
def test_channel_create_empty_name():
    clear_v1()
    dev_data = auth_register_v1('dev.bhimsaria@gmail.com', 'dev123#', 'dev',\
     'bhimsaria')
    with pytest.raises(InputError):
    	channels_create_v1(dev_data['auth_user_id'], '', True)

#4. Tests if it raises InputError when provided a long channel name.
def test_channel_create_too_long_name():
    clear_v1()
    dev_data = auth_register_v1('dev.bhimsaria@gmail.com', 'dev123#', 'dev',
     'bhimsaria')
    with pytest.raises(InputError):
    	channels_create_v1(dev_data['auth_user_id'],
    	 'jdfkjfkjksjfksjsfkjksfskfskfskjfskf', False)
 
#5. Tests for when a user is registered, yet has not created a channel but is invited into one, therefore should have a channel listed. 
def test_channel_list_member():
    clear_v1()
    woody_data = auth_register_v1('sheriff.hugh@gmail.com', 'woody123#',
     'sheriff', 'woody')
    zerg_data = auth_register_v1('zerg.hugh@gmail.com', 'zerg123#', 'lord',
     'zerg')
    ch = channels_create_v1(woody_data['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(woody_data['auth_user_id'], ch, 
    zerg_data['auth_user_id'])
    assert(channels_list_v1(zerg_data['auth_user_id']) == {'channels':
     [{'channel_id': 1, 'name': 'Channel1'}]})
     
#6. Tests when invalid user_id is passed in to channels_create, channels_list and channels_listall    	
def test_channel_invalid_user_id():
    clear_v1()
    user_id = 3
    with pytest.raises(AccessError):
    	channels_create_v1(user_id, 'OscarChannel', \
    	 True)
    with pytest.raises(AccessError):
        channels_list_v1(user_id)
    with pytest.raises(AccessError):
        channels_listall_v1(user_id)

#7. Tests for when two channels are created with one user's id, they should be listed as followed  	
def test_channel_list_two_channels():
    clear_v1()
    ray_data = auth_register_v1('ray.hugh@gmail.com', 'ray123#', 'ray', 'hugh')
    channels_create_v1(ray_data['auth_user_id'], 'Channel1', True)
    channels_create_v1(ray_data['auth_user_id'], 'Channel2', False)
    assert(channels_list_v1(ray_data['auth_user_id']) == {'channels':
     [{'channel_id': 1, 'name': 'Channel1'}, {'channel_id': 2, 'name':
      'Channel2'}]})

#8. Tests for when one user creates three channels of which are all listed      
def test_channel_list_private_three_channels():
    clear_v1()
    fish_data = auth_register_v1('fish_meat@yahoo.com', 'fishrule', 'Lucas',
     'Dane')
    channels_create_v1(fish_data['auth_user_id'], 'Fish Channel 1',
     False)
    channels_create_v1(fish_data['auth_user_id'], 'Fish Channel 2',
     False)
    channels_create_v1(fish_data['auth_user_id'], 'Fish Channel 3',
     False)
    assert(channels_listall_v1(fish_data['auth_user_id']) == {'channels':
     [{'channel_id': 1, 'name': 'Fish Channel 1'}, {'channel_id': 2, 'name': 
     'Fish Channel 2'},{'channel_id': 3, 'name': 'Fish Channel 3'}]})

#9. Tests for when two users create a channel each of which channel_list only lists user 1's channel     
def test_channel_list_one_channel():
    clear_v1()
    ray_data = auth_register_v1('ray.hugh@gmail.com', 'ray123#', 'ray', 'hugh')
    mes_data = auth_register_v1('mes.hugh@gmail.com', 'mes123#', 'mes', 'hugh')
    channels_create_v1(ray_data['auth_user_id'], 'Channel1', True)
    channels_create_v1(mes_data['auth_user_id'], 'Channel2', True)
    assert(channels_list_v1(ray_data['auth_user_id']) == {'channels':
     [{'channel_id': 1, 'name': 'Channel1'}]})

#10. Tests for when two users create seperate channels and another user wants to list all channels
def test_channel_list_all_three_channels():
    clear_v1()
    ray_data = auth_register_v1('ray.hugh@gmail.com', 'ray123#', 'ray', 'hugh')
    mes_data = auth_register_v1('mes.hugh@gmail.com', 'mes123#', 'mes', 'hugh')
    fish_data = auth_register_v1('fish_meat@yahoo.com', 'fishrule', 'Lucas',
     'Dane')
    channels_create_v1(ray_data['auth_user_id'], 'Rays Channel',
     True)
    channels_create_v1(mes_data['auth_user_id'], 'Mes Channel',
     False)
    assert(channels_listall_v1(fish_data['auth_user_id']) == {'channels':
     [{'channel_id': 1, 'name': 'Rays Channel'}, {'channel_id': 2, 'name': 
     'Mes Channel'}]})

#11. Tests for when a registered user tries to list channels that haven't been created
def test_when_no_channels():
    clear_v1()
    ray_data = auth_register_v1('ray.hugh@gmail.com', 'ray123#', 'ray', 'hugh')
    assert(channels_listall_v1(ray_data['auth_user_id']) == {'channels':
     []})
    assert(channels_list_v1(ray_data['auth_user_id']) == {'channels':
     []})
'''
