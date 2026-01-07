def get_user_info(user_payload):
    return {
        'user_id': user_payload.get('user_id'),
        'username': user_payload.get('username')
    }

