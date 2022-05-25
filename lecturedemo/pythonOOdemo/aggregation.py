class Car:
# composition - car composes engine
    def  __init__(self,make,model,engine):
    self._make = make
    self._moel = model
    self._engine = engine

class Engine:
    def  __init__(self,chassis):    
	    self._chassis = chassis

#here, the part is instantiated outside the container
#part instance can exist even after the container does not exist
#hence this is an example of aggregation

e = Engine("456xsdf")
my_car = Car("Honda","Accord",e)
another_car = Car("Honda","Civic",e)