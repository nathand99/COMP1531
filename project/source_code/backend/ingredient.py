class Ingredient():
    def __init__(self, name, unit):
        self._name = name
        self._unit = unit
    
    @property
    def name(self):
        return self._name
    
    @property
    def unit(self):
        return self._unit

    def __str__(self):
        return f"Ingredient <{self._name}, unit: {self._unit}>"
