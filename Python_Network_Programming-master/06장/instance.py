class Car():
    # to represent a car
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_car_name(self):
        long_name = str(self.year) + ' ' + self.make + ' ' + self.model
        return long_name.title()

class ElectricCar(Car):
    def __init__(self, make, model, year):
        # Initialize attributes of the parent class.
        super().__init__(make, model, year)
        self.battery = Battery()

class Battery():
    #  to model a battery for an electric car.
    def __init__(self, battery_size=70):
        # Initialize the battery's attributes.
        self.battery_size = battery_size
    def describe_battery(self):
        # a statement describing the battery size.
        print("This car has a " + str(self.battery_size) + "-kWh battery.")

my_tesla = ElectricCar('tesla', 'model s', 2016)
print(my_tesla.get_car_name())
my_tesla.battery.describe_battery()
