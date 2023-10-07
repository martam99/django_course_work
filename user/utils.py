from user.models import User

user = User()


def is_manager(user):
    return user.groups.filter(name='Managers').exists()
