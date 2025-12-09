class DBException(Exception):
    pass


class ItemNotFoundException(DBException):
    pass


class DuplicateItemException(DBException):
    pass
