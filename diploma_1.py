# diploma_PY21


import requests
import time
import json

token = 'e62bff8a57e7662edee756efac3726bbf1349a3b7c19dcdcce08f4858b62fa3c5370c7479d7ff7a9d7f79'

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

print('проверяем:\n', user_id)


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
# print('список друзей проверяемого: \n', friends_list_id)

print('\n--Записываем все группы друзей  во множество friends_group_set--\n')

friends_group = []
count = 0
for friend in friends_list_id:
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'access_token': token,
        'v': 5.92,
        'user_id': friend
    }
    response = requests.get(url, params=params, timeout=30).json()
    if 'error' in response:
        print('обращение к другу выдало: номер ошибки', response['error']['error_code'], '- ',response['error']['error_msg'])
        count += 1
        continue
    else:
        friends_group.extend(response['response']['items'])
        count += 1
    print('проверены группы друга № {}'.format(count))
    time.sleep(0.35)

friends_group_set = set(friends_group)
print('количество групп у друзей проверяемого: ', len(friends_group_set))
# print('список групп друзей проверяемого: ', friends_group_set)

print('\n--Находим группы из первого множества, которых нет во втором--\n')

only_user_groups = user_groups_set.difference(friends_group_set)

print('количество групп проверяемого без его друзей:', len(only_user_groups))
print('список групп проверяемого без его друзей:', only_user_groups)

group_list = []
count = 1
for group in only_user_groups:
    group_info_dict = {}
    try:

        params = {

            'access_token': token,
            'v': 5.92,
            'group_id': group,
            'fields': 'members_count',

        }
        # print('params\n', params)
        url = 'https://api.vk.com/method/groups.getById'
        response = requests.get(url, params=params, timeout=30).json()
        # print('response\n', response)
        if 'error' in response:
            print('error: ', response, '\n')
            continue
        else:

            group_info_dict['name'] = (response['response'][0]['name'])
            # print('group_info_dict[name]\n', group_info_dict['name'])
            group_info_dict['gid'] = (response['response'][0]['id'])

            # print('group_info_dict[gid]\n', group_info_dict['gid'])

            group_info_dict['members_count'] = (response['response'][0]['members_count'])
            # print('group_info_dict[members_count]\n', group_info_dict['members_count'])
            if 'error' in response:
                print('обращение к группе выдало:\n', response['response'])
                count += 1
                continue
            group_list.append(group_info_dict)
            print('записываем группу № ', count)
            count += 1
            time.sleep(0.35)

    except:
        # count += 1
        print('обращение к группе выдало: error\n', response['response'][0]['deactivated'])



print('len_group_list:\n', len(group_list))
# print('создан словарь из списка:\n', group_list)

with open('groups.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(group_list, ensure_ascii=False, indent=2, default=str))