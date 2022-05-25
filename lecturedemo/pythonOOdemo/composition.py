class  Car:  
# composition - car composes engine
# part instiated inside the constructor of the container

    def  __init__(self,make,model, chassis):
        self._make = make
        self._moel = model
        self._engine = Engine(chassis)

class  Engine:
    def  __init__(self,chassis):
        self._chassis = chassis

my_car = Car("Honda","Accord","456sxd")s