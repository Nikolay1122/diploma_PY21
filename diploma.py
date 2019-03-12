# diploma_PY21

import requests
import time
import json

token = '6601d3306601d3306601d330986668ea98666016601d3303a86a0d27143595f139c0143'

user = input('Введите id пользователя или его user_name:')
print('user\n', user)

try:
    params = {
        'access_token': token,
        'v': 5.92,
        'q': user
    }
    print('params\n', params)
    url = 'https://api.vk.com/method/users.search'
    response = requests.get(url, params=params, timeout=30).json()
    print('response\n', response)
    user_id = response['response']['items'][0]['id']
    print('user_id1\n', user_id)
except:
    user_id = user
    print('user_id2\n', user_id)
finally:
    print('user_id2\n', user_id)

print('user_id3\n', user_id)


# Записываем группы объекта во множество user_groups_set

def get_user_groups(user_id):
    params = {
        'access_token': token,
        'v': 5.92,
        'user_id': user_id
    }
    print('params\n', params)
    url = 'https://api.vk.com/method/groups.get'
    response = requests.get(url, params=params, timeout=30).json()
    print('response\n', response)
    user_groups_set = set(response['response']['items'])
    return (user_groups_set)

user_groups_set = get_user_groups(user_id)
print('user_groups_set\n', user_groups_set)

#Записваем друзей в список friends_list
def get_user_friends(user_id):
    params = {
        'access_token': token,
        'v': 5.92,
        'user_ids': user_id
    }
    url = 'https://api.vk.com/method/friends.get'
    response = requests.get(url, params=params, timeout=30).json()
    print('response\n', response)
    friends_list_id = response['response']['items']
    return (friends_list_id)


friends_list_id = get_user_friends(user_id)

print('friends_list_id: \n', friends_list_id)

#Записываем все группы друзей  во множество friends_group_set


friends_group = []
count = 1
for friend in friends_list_id:
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'access_token': token,
        'v': 5.92,
        'user_id': friend
    }
    response = requests.get(url, params=params, timeout=30).json()
    if 'error' in response:
        print('error\n', response)
        continue
    else:
        friends_group.extend(response['response']['items'])
    print('Проверены группы друга № {}'.format(count))
    time.sleep(3)
    count += 1

friends_group_set = set(friends_group)
print('friends_group_set: ', friends_group_set)

#Находим группы из первого множества, которых нет во втором

only_user_groups = user_groups_set.difference(friends_group_set)

print('only_user_groups:', only_user_groups)

group_list = []
count = 1
for group in only_user_groups:
    group_info_dict = {}
    params = {
        'access_token': token,
        'v': 5.92,
        'group_id': group,
        'fields': 'members_count',

    }
    url = 'https://api.vk.com/method/groups.getById'
    response = requests.get(url, params=params, timeout=30).json()
    if 'error' in response:
        print('error\n', response)
        continue
    else:
        group_info_dict['name'] = (response['response'][0]['name'])
        group_info_dict['gid'] = (response['response'][0]['id'])

        group_info_dict['members_count'] = (response['response'][0]['members_count'])
        group_list.append(group_info_dict)
        print(count)
        count += 1
        time.sleep(3)

print('group_list:\n', group_list)

with open('groups.json', 'w') as f:
    f.write(json.dumps(group_list))