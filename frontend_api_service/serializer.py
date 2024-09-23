class Serialzer():
    def __init__(self) -> None:
        pass

    def serialize_user(self, user):
        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': str(user.created_at)
        }   
