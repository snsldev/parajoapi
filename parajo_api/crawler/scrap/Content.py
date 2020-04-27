class Content:

    def __init__(self, carId, site, info, price, accident):
        self.carId = carId
        self.site = site
        self.info = info
        self.price = price
        self.accident = accident

class CarGrade:

    def __init__(self, name):
        self.name = name