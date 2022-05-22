

class FallbackException(Exception):
    def __init__(self):
        msg = 'Fallback Function is Not Defined'
        super().__init__(msg)


class UserException(Exception):
    def __init__(self):
        msg = 'User ID Not Found'
        super().__init__(msg)

