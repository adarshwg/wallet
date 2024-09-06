class UserNotFoundException(Exception):
    pass


class WalletEmptyException(Exception):
    pass


class InvalidPasswordException(Exception):
    pass


class NotAuthorizedException(Exception):
    pass


class SelfTransferException(Exception):
    pass


class LowBalanceException(Exception):
    pass
