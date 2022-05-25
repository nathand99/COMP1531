class BasicException(Exception):
    def __init__(self, title, message):
        self._title = title
        self._message = message
    
    @property
    def title(self):
        return self._title

    @property
    def message(self):
        return self._message

class NotFoundException(BasicException):
    """
        Raised when the corresponding item or unique key of the item is not registered
        Item types include Ingredient, Product, MainType, Order, staff_code (str)
    """
    pass

class NotEnoughStockException(BasicException):
    """
        Raised when the stock cannot support the change of content of the order
    """
    pass

class ExceedLimitException(BasicException):
    """
        Raised when the ordered quantity exceeds the limit
        Currently only applies to main type, in which there are limits on the number of selections for 
        Base and MajorFilling and total quantity of Base, MajorFilling, MinorFilling
    """
    pass


class IncorrectOrderStatusException(BasicException):
    """
        Raised when the order is not in the appropreiate status
    """
    pass

class MainTypeNotSelectedException(BasicException):
    """
        Raised when the action cannot be carried out without a main type
    """
    pass

class NotAllowedForMainTypeException(BasicException):
    """
        Raised when the product of type ProductForMain or StandardMain is not allowed for that kind of MainType
    """
    pass

class IncorrectTypeException(BasicException):
    """
        Raised when the variable is in incorrect
    """
    pass

class IncorrectValueException(BasicException):
    """
        Raised when the value is not correct
    """
    pass

