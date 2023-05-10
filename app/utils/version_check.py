from django.utils.version import get_version_tuple

def check_if_version_valid(latest_app_version, current_user_version):
    """ returns whether the user version is less than latest version :param latest_app_version: string :param current_user_version: string :return Bool: """
    user_version = get_version_tuple(current_user_version)
    latest_version = get_version_tuple(latest_app_version)
    if latest_version[0] > user_version[0]:
        return True 
    if latest_version[0] == user_version[0] and latest_version[1] > user_version[1]:
        return True
    elif latest_version[0] == user_version[0] and latest_version[1] == user_version[1] and latest_version[2] >= user_version[2]:
        return True
    return False

def check_version_update(latest_app_version, current_user_version):
    """ returns whether the user version needs update or not :param latest_app_version: string :param current_user_version: string :return is_mandatory: Bool: :return has_update: Bool: """
    user_version = get_version_tuple(current_user_version)
    latest_version = get_version_tuple(latest_app_version)
    if latest_version[0] > user_version[0]:
        has_update = True
    elif latest_version[0] < user_version[0]:
        has_update = False
    elif latest_version[1] > user_version[1]:
        has_update = True
    elif latest_version[1] < user_version[1]:
        has_update = False
    elif latest_version[2] > user_version[2]:
        has_update = True
    else:
        has_update = False
    return has_update