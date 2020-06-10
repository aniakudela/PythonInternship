class IllegalCarError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Car:
    def __init__(self, pax_count, car_mass, gear_count):
        if not self._pax_countValid(pax_count):
            raise IllegalCarError('pax_count cannot be greater than 5, or less than 1')
        if not self._car_massValid(car_mass):
            raise IllegalCarError('car_mass (excluding the passengers) cannot be greater than 2000 kg')
        if not self._gear_countValid(gear_count):
            raise IllegalCarError('gear_count cannot be less than 0 and it must be an integer number')

        self.pax_count = pax_count
        self.car_mass = car_mass
        self.gear_count = gear_count

    def _pax_countValid(self, pax_count):
        return type(pax_count) == int and 1 < pax_count < 5

    def _car_massValid(self, car_mass):
        return (type(car_mass) == float or type(car_mass) == int) and 0 < car_mass < 2000

    def _gear_countValid(self, gear_count):
        return type(gear_count) == int and gear_count > 0

    def total_mass(self):
        """Retrieves the total mass estimate of a car instance, assuming that an average person weight is 70 kg."""
        return str(self.car_mass + self.pax_count * 70)


if __name__ == '__main__':
    c = Car(3, 1600, 5)
    print(c.total_mass())
    # wrong_car_1 = Car(3, 2001, 5)
