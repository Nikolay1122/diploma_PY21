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
user_groups_set_enter = user_groups_set
print('количество групп у проверяемого:\n', len(user_groups_set))
print('список групп у проверяемого\n', user_groups_set)


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
    friends_list_id = set(response['response']['items'])
    return (friends_list_id)


friends_list_id = set(get_user_friends(user_id))

print('количество друзей у проверяемого: \n', len(friends_list_id))
print('список друзей проверяемого: \n', friends_list_id)

print('\n--Проверяем присутствие друзей в группах --\n')
# count_group = 0
# count_friend = 0
count_error = 0
groups_friends = set()
for group in user_groups_set:
    users_groups = []
    params = {
        'access_token': token,
        'v': 5.92,
        'group_id': group,
        'filter': 'friends',
    }
    # print('params\n', params)
    url = 'https://api.vk.com/method/groups.getMembers'
    response = requests.get(url, params=params, timeout=30).json()
    # print('0', users_groups)
    if 'error' in response:
        print('error: ', response, '\n')
        count_error +=1
        continue
    else:
        users_groups.extend(response['response']['items'])
        # print('1', users_groups)
        # users_groups = set(users_groups)
        # print('2', users_groups)
        # print('\nlen', len(users_groups))
        # l = len(users_groups)
        # print(users_groups)
        # print('friends_list_id',friends_list_id)
        # print(users_groups.isdisjoint(friends_list_id))
        # fr = friends_list_id.isdisjoint(users_groups)
        # print(fr)
        # print(friends_list_id.intersection_update(users_groups))
        if len(users_groups) > 0:
            print('group', group)
            groups_friends.add(group)
            print('1', groups_friends)
    time.sleep(0.35)
user_groups_set_enter -= groups_friends
        # else:
        #     continue
print(count_error)
print('количество групп без друзей:\n', len(user_groups_set_enter))
print('список групп без друзей\n', user_groups_set_enter)
        #
    #     print(users_groups)
    #     )print(response)
    # for friend in friends_list_id:
    #     if friend in users_groups:
    #         print(users_groups)
#


