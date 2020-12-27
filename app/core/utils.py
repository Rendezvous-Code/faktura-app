# account roles settings

ACCOUNT_PERMISSION_GROUPS = [
    {'name': 'account-admin', 'str': 'Admin'},
    {'name': 'account-user', 'str': 'User'}
]

ACCOUNT_PERMISSION_GROUP_NAMES = list(group['name']
                                      for group in ACCOUNT_PERMISSION_GROUPS)
ACCOUNT_ROLE_CHOICES = list((x['name'], x['str'])
                            for x in reversed(ACCOUNT_PERMISSION_GROUPS))
