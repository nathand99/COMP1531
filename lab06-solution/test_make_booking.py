from car_rental_system import CarRentalSystem
from car import SmallCar, MediumCar, LargeCar, PremiumCar
from customer import Customer
from location import Location
from errors import BookingError
from datetime import datetime
import pytest

@pytest.fixture
def sys():
    return CarRentalSystem()

@pytest.fixture
def george(sys):
    c = Customer('george', 111)
    sys.add_customer(c)
    return c

def date_str(year, month, day):
    return f'{year}-{month}-{day}'

class TestMakeBooking():

    # Alternative to pytest fixtures
    # def setup_method(self):
    #     self.system = CarRentalSystem()
    #     self.george = Customer('george', 111)
    #     self.system.add_customer(self.george)


    def test_successful_make_small_car_booking(self, sys, george):        
        loc1 = 'Sydney'
        loc2 = 'Melbourne'
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 23)

        # (Name, Model, Rego)
        car = SmallCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert len(sys.bookings) == 1
        assert len(errors) == 0
        assert booking is not None
        assert sys.bookings[0] is booking
        assert booking.fee              == 200
        assert booking.location.pickup  == loc1
        assert booking.location.dropoff == loc2


    def test_successful_make_medium_car_booking(self, sys, george):
        loc1 = 'Sydney'
        loc2 = 'Melbourne'
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 23)

        # (Name, Model, Rego)
        car = MediumCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert len(sys.bookings) == 1
        assert len(errors) == 0
        assert booking is not None
        assert sys.bookings[0] is booking
        assert booking.fee              == 300
        assert booking.location.pickup  == loc1
        assert booking.location.dropoff == loc2


    def test_successful_make_large_car_booking_below_7_days(self, sys, george):
        loc1 = 'Sydney'
        loc2 = 'Melbourne'
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 23)

        # (Name, Model, Rego)
        car = LargeCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert len(sys.bookings) == 1
        assert len(errors) == 0
        assert booking is not None
        assert sys.bookings[0] is booking
        assert booking.fee              == 400
        assert booking.location.pickup  == loc1
        assert booking.location.dropoff == loc2


    def test_successful_make_large_car_booking_over_7_days(self, sys, george):
        loc1 = 'Sydney'
        loc2 = 'Melbourne'
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 28)

        # (Name, Model, Rego)
        car = LargeCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert len(sys.bookings) == 1
        assert len(errors) == 0
        assert booking is not None
        assert sys.bookings[0] is booking
        assert booking.fee              == 855
        assert booking.location.pickup  == loc1
        assert booking.location.dropoff == loc2


    def test_successful_make_premium_car_booking(self, sys, george):
        loc1 = 'Sydney'
        loc2 = 'Melbourne'
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 23)

        # (Name, Model, Rego)
        car = PremiumCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert len(sys.bookings) == 1
        assert len(errors) == 0
        assert booking is not None
        assert sys.bookings[0] is booking
        assert booking.fee              == 690
        assert booking.location.pickup  == loc1
        assert booking.location.dropoff == loc2


    def test_make_booking_with_invalid_period(self, sys, george):
        loc1 = 'Sydney'
        loc2 = 'Melbourne'
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 19)

        # (Name, Model, Rego)
        car = PremiumCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert 'period' in errors
        assert errors['period'] == 'Specify a valid booking period'
        assert booking is None
        assert len(sys.bookings) == 0


    def test_make_booking_with_empty_start_location(self, sys, george):
        loc1 = ''
        loc2 = 'Melbourne'
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 23)

        # (Name, Model, Rego)
        car = PremiumCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert 'start_location' in errors
        assert errors['start_location'] == 'Specify a valid start location'
        assert booking is None
        assert len(sys.bookings) == 0


    def test_make_booking_with_empty_end_location(self, sys, george):
        loc1 = 'Sydney'
        loc2 = ''
        date1 = date_str(2018, 5, 20)
        date2 = date_str(2018, 5, 23)

        # (Name, Model, Rego)
        car = PremiumCar('Mazda', 'Falcon', 100)
        sys.add_car(car)
        booking, errors = sys.make_booking(george, car, date1, date2, loc1, loc2)

        assert 'end_location' in errors
        assert errors['end_location'] == 'Specify a valid end location'
        assert booking is None
        assert len(sys.bookings) == 0


'''
Similarly, test for invalid dates in the almost exact same format as above
'''