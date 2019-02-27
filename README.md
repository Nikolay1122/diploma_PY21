# diploma_PY21

import requests
import time
import json

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

user = input('Введите id пользователя или его user_name:')
print('user', user)

try:
    params = {
        'access_token': token,
        'v': 5.92,
        'q': user
    }
    print('params', params)
    url = 'https://api.vk.com/method/users.search'
    response = requests.get(url, params=params, timeout=30).json()
    print('response', response)
    user_id = response['response']['items'][0]['id']
    print('user_id1', user_id)
except:
    user_id = user
    print('user_id2', user_id)

print('user_id', user_id)


# Записываем группы объекта во множество user_groups_set

def get_user_groups(user_id):
    params = {
        'access_token': token,
        'v': 5.92,
        'user_id': user_id
    }
    print('params', params)
    url = 'https://api.vk.com/method/groups.get'
    response = requests.get(url, params=params, timeout=30).json()
    print('response', response)
    user_groups_set = set(response['response']['items'])
    return (user_groups_set)

user_groups_set = get_user_groups(user_id)
print('user_groups_set', user_groups_set)
