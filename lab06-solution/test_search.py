from car_rental_system import CarRentalSystem
from car import SmallCar, MediumCar, LargeCar, PremiumCar
from customer import Customer
from location import Location
from errors import BookingError
from datetime import datetime
from client import IdGenerator
import pytest


@pytest.fixture
def sys():
    system = CarRentalSystem()
    rego_generator = IdGenerator()

    for name in ["Mazda", "Ford"]:
        for model in ["Falcon", "Commodore"]:
            system.add_car(SmallCar(name, model, rego_generator.next()))
            system.add_car(MediumCar(name, model, rego_generator.next()))
            system.add_car(LargeCar(name, model, rego_generator.next()))

    for name in ["Tesla", "Audi"]:
        for model in ["model x", "A4"]:
            system.add_car(PremiumCar(name, model, rego_generator.next()))
    return system


class TestSearchAll():

    def test_successful_search_all(self, sys):
        cars = sys.car_search(None, None)
        assert cars is not None
        assert len(sys.cars) == len(cars)
        assert set(sys.cars) == set(cars)

    def test_no_car_available(self, sys):
        cars = sys.car_search('Non-existent Make', 'Non-existent Model')
        assert cars == []



class TestSearchByKeyword():

    def test_successful_search_by_exact_match_make(self, sys):
        self._test_search_by_make(sys, 'Mazda')

    def test_successful_search_by_different_cases_match_make(self, sys):
        self._test_search_by_make(sys, 'mAzDa')

    def test_successful_search_by_substring_match_make(self, sys):
        self._test_search_by_make(sys, 'az')

    def test_search_with_no_matched_make(self, sys):
        self._test_search_by_make(sys, 'potato')

    def test_successful_search_by_exact_match_model(self, sys):
        self._test_search_by_model(sys, 'Falcon')

    def test_successful_search_by_different_cases_match_model(self, sys):
        self._test_search_by_model(sys, 'fAlCoN')

    def test_successful_search_by_substring_match_model(self, sys):
        self._test_search_by_model(sys, 'alc')

    def test_search_with_no_matched_model(self, sys):
        self._test_search_by_model(sys, 'potato')


    def test_successful_search_by_make_and_model(self, sys):
        self._test_search_by_make_and_model(sys, 'maz', 'alc')

    def test_search_by_matched_make_and_no_matched_model(self, sys):
        self._test_search_by_make_and_model(sys, 'maz', 'potato')

    def test_search_by_no_matched_make_and_matched_model(self, sys):
        self._test_search_by_make_and_model(sys, 'potato', 'alc')

    def test_search_by_no_matched_keywords(self, sys):
        self._test_search_by_make_and_model(sys, 'potato', 'tomato')

    def _test_search_by_make(self, sys, make):
        result = sys.car_search(make, None)

        for car in sys.cars:
            if car in result:
                assert make.lower() in car.name.lower()
            else:
                assert make.lower() not in car.name.lower()

    def _test_search_by_model(self, sys, model):
        result = sys.car_search(None, model)

        for car in sys.cars:
            if car in result:
                assert model.lower() in car.model.lower()
            else:
                assert model.lower() not in car.model.lower()

    def _test_search_by_make_and_model(self, sys, make, model):
        result = sys.car_search(make, model)

        make = make.lower()
        model = model.lower()

        for car in sys.cars:
            if car in result:    
                assert (make in car.name.lower()) or (model in car.model.lower())
            else:
                assert (make not in car.name.lower()) and (model not in car.model.lower())
