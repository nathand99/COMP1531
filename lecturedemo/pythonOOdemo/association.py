class  Pet:
    def __init__(self, species, age, owner=None):
        self._species = species
        self._age = age
        self._owner = owner
    def  set_owner(self, p):
	    self._owner = p

class  Car:
    def  __init__(self,make,model):
        self._make = make
        self._model = model

class  Person:
    def  __init__(self,name):
        self._name = name
    def  drive(self, car):
	    pass

  
andrew = Person("andrew")
some_car = Car("Honda","Euro")

#example of association between Car and Person through method collaboration
andrew.drive(some_car)

#example of association between Pet and Person through setting the owner. Here,
#pet instance can be associated with any Person instance
terry = Pet("labrador",1)
terry.set_owner(andrew)