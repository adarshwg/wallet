class UserNotFoundException(Exception):
    pass

class InvalidMudraPinException(Exception):
    pass

class UserAlreadyExistsException(Exception):
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


class InvalidAmountException(Exception):
    pass


class InvalidDateException(Exception):
    pass


class NoRecordsException(Exception):
    pass


class DatabaseException(Exception):
    pass
