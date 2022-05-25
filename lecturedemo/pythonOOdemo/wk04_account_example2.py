from abc import ABC, abstractmethod
    
# Setting Account's super class as ABC means it is an abstract class - it cannot be instansiated
class Account(ABC):
    def compute_fee(self):
        return 5.50
    
    @abstractmethod
    def calculate_interest(self):
        pass

# SavingsAccount has Account as super/parent class - it must implement calculate_interest
class SavingsAccount(Account):
    def __init__(self,name,amount):
        self._name = name
        self._balance = amount
        self._saver_interest = 0.05
    
    def calculate_interest(self):
        return self._balance * self._saver_interest
                    
a2 = SavingsAccount("joe",1000)
print("{0}'s balance is {1} building interest at {2} and monthly fee is {3}:"
.format(a2._name,a2._balance,a2._saver_interest,a2.compute_fee()))
# a2 uses the calculate_interest method from its parent

#a3 = Account() # TypeError: Can't instantiate abstract class Account with abstract methods calculate_interest