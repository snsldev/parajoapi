from django.db import models

# 차량 카테고리-브랜드
class CarBrand(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = "car_category_brand" # 실제 테이블명을 직접 입력할 경우 
    
    def __str__(self):
        return  self.name
# 차량 카테고리-모델
class CarModel(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # brand = models.IntegerField(default=None)
    brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT, db_column='brand')

    class Meta:
        db_table = "car_category_model" # 실제 테이블명을 직접 입력할 경우 
    
    def __str__(self):
        return  self.name
        
# 차량 카테고리-상세모델
class CarModelDetail(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default=None)
    # model = models.IntegerField(default=None)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT, db_column='model')

    class Meta:
        db_table = "car_category_model_detail" # 실제 테이블명을 직접 입력할 경우 
    
    def __str__(self):
        return  self.name

# 차량 카테고리-등급
class CarGrade(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default=None)
    modelDetail = models.ForeignKey(CarModelDetail, on_delete=models.PROTECT, db_column='modelDetail')

    class Meta:
        db_table = "car_category_model_detail_grade" # 실제 테이블명을 직접 입력할 경우 
    
    def __str__(self):
        return  self.name

# 차량 카테고리-등급-세부등급1
class CarGradeSubGroup(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default=None)
    grade = models.ForeignKey(CarGrade, on_delete=models.PROTECT, db_column='grade')

    class Meta:
        db_table = "car_category_model_detail_grade_subgroup" # 실제 테이블명을 직접 입력할 경우 
    
    def __str__(self):
        return  self.name

# 차량 카테고리-등급-세부등급2
class CarGradeSub(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default=None)
    gradeSubGroup = models.ForeignKey(CarGradeSubGroup, on_delete=models.PROTECT, db_column='gradeSubGroup')

    class Meta:
        db_table = "car_category_model_detail_grade_sub" # 실제 테이블명을 직접 입력할 경우 
    
    def __str__(self):
        return  self.name

# 자동차 정보
class CarInfo(models.Model):
    seq = models.AutoField(primary_key=True)
    catg_modeldetail_id = models.IntegerField(default=None)
    catg_grade_id = models.IntegerField(default=None)
    catg_modeldetail_name = models.CharField(max_length=50, default=None)
    catg_grade_name = models.CharField(max_length=50, default=None)
    carId = models.CharField(max_length=50, default=None)
    info = models.CharField(max_length=255, default=None)
    price = models.CharField(max_length=50, default=None)
    accident = models.CharField(max_length=50, default=None)
    site = models.CharField(max_length=20, default=None)

    class Meta:
        db_table = "web_scraped_car_info" # 실제 테이블명을 직접 입력할 경우 
    
    def __str__(self):
        return  self.info

        
