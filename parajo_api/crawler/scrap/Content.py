# 자동차 가격정보
class Content:

    def __init__(self, carId, site, info, price, accident):
        self.carId = carId
        self.site = site
        self.info = info
        self.price = price
        self.accident = accident
# 등급
class CarGrade:

    def __init__(self, name):
        self.name = name
# 세부등급1
class CarGradeSubGroup:

    def __init__(self, name):
        self.name = name
# 세부등급2
class CarGradeSub:

    def __init__(self, name):
        self.name = name