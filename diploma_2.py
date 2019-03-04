#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import json

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

user = input('Введите id пользователя или его user_name:')
# print('user\n', user)

try:
    params = {
        'access_token': token,
        'v': 5.92,
        'q': user
    }
    # print('params\n', params)
    url = 'https://api.vk.com/method/users.search'
    response = requests.get(url, params=params, timeout=30).json()
    # print('response\n', response)
    user_id = response['response']['items'][0]['id']
    # print('user_id1\n', user_id)
except:
    user_id = user
    # print('проверяем\n', user_id)

# print('проверяем:\n', user_id)


print('\n--Записываем группы объекта во множество user_groups_set--\n')


def get_user_groups(user_id):
    params = {
        'access_token': token,
        'v': 5.92,
        'user_id': user_id
    }
    # print('params\n', params)
    url = 'https://api.vk.com/method/groups.get'
    response = requests.get(url, params=params, timeout=30).json()
    # print('response\n', response)
    user_groups_set = set(response['response']['items'])
    return (user_groups_set)


user_groups_set = get_user_groups(user_id)
print('количество групп у проверяемого:\n', len(user_groups_set))
# print('список групп у проверяемого\n', user_groups_set)


print('\n--Записваем друзей в список friends_list--\n')


def get_user_friends(user_id):
    params = {
        'access_token': token,
        'v': 5.92,
        'user_id': user_id
    }
    url = 'https://api.vk.com/method/friends.get'
    response = requests.get(url, params=params, timeout=30).json()
    # print('response\n', response)
    friends_list_id = response['response']['items']
    return (friends_list_id)


friends_list_id = get_user_friends(user_id)

print('количество друзей у проверяемого: \n', len(friends_list_id))
print('список друзей проверяемого: \n', friends_list_id)
