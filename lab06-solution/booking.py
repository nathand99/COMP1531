class Booking:

    def __init__(self, customer, car, period, location):
        self._customer  = customer
        self._car       = car
        self._period    = period
        self._location  = location

    @property
    def fee(self):
        return self._car.calc_fee(self._period)

    @property
    def location(self):
        return self._location

    def __str__(self):
        output = ''
        output += f'Made by {self._customer}\n'
        output += f'Reserve {self._car} for {self._period} days\n'
        output += f'Locations: {self._location}\n'
        output += f'Total fee: ${self.fee:.2f}'
        return output

