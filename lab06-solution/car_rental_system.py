from booking import Booking
from location import Location
from errors import BookingError, check_booking_error
from datetime import datetime

class CarRentalSystem():

    def __init__(self):
        self._cars      = []
        self._customers = []
        self._bookings  = []

    '''
    Query Processing
    '''
    def car_search(self, name=None, model=None):
        # Return all cars if no keyword given
        if not name and not model:
            return self.cars

        # Convert search keywords into lowercases (if provided)
        name  = name.lower()    if name else None
        model = model.lower()   if model else None

        # Collect all matching cars into a list
        cars = []
        for car in self.cars:
            if name and (name in car.name.lower()):
                cars.append(car)

            elif model and (model in car.model.lower()):
                cars.append(car)

        return cars


    def get_customer(self, licence):
        for customer in self._customers:
            if customer.licence is licence:
                return customer
        return None


    def get_car(self, rego):
        for c in self.cars:
            if c.rego == rego:
                return c
        return None


    '''
    Booking
    '''

    def make_booking(self, customer, car, date1, date2, location1, location2):
        # we will see a better way to handle errors in the next lab
        try:
            check_booking_error(date1, date2, location1, location2)
        except BookingError as be:
            return None, be.errors 

        self._customers.append(customer)

        start_date = datetime.strptime(date1, "%Y-%m-%d")
        end_date   = datetime.strptime(date2, "%Y-%m-%d")
        period     = (end_date - start_date).days + 1
        location   = Location(location1, location2)
        
        booking = Booking(customer, car, period, location)
        self._bookings.append(booking)
        print(booking)
        return booking, {}


    def check_fee(self, customer, car, date1, date2, location1, location2):
        try:
            check_booking_error(date1, date2, location1, location2)
        except BookingError as be:
            return None, be.errors

        start_date = datetime.strptime(date1, "%Y-%m-%d")
        end_date   = datetime.strptime(date2, "%Y-%m-%d")
        period     = (end_date - start_date).days + 1

        return car.calc_fee(period), {}

        
    ''' 
        Registration
    '''
    def add_car(self, car):
        self._cars.append(car)

    def add_customer(self, customer):
        self._customers.append(customer)


    '''
    Properties
    '''
    @property
    def cars(self):
        return self._cars

    @property
    def customers(self):
        return self._customers

    @property
    def bookings(self):
        return self._bookings

