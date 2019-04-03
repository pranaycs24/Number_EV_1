class CarConfiguration:
    def __init__(self, speed, charging_rate, car_capacity):

        self.speed = speed
        self.charging_rate = charging_rate
        self.car_capacity = car_capacity

    @property
    def speed(self):
        return self.speed

    @property
    def charging_rate(self):
        return  self.charging_rate

    @property
    def car_capacity(self):
        return self.car_capacity
