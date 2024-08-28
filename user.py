from authentication import Authentication


class User :
    def __init__(self,username,password):
        Authentication.login(username,password)