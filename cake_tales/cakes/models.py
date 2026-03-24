from django.db import models

import uuid

# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta :

        abstract = True

    
# class CategoryChoices(models.TextChoices):

#     WEDDING_CAKES = 'Wedding cakes','Wedding cakes'

#     BIRTHDAY_CAKES = 'Birthday cakes','Birthday cakes'

#     PLUM_CAKES = 'Plum cakes','Plum cakes'

#     CUP_CAKES = 'Cup cakes','Cup cakes'

class Category(BaseClass):

    name = models.CharField(max_length=30)

    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name = 'categories'

        verbose_name_plural = 'categories'



# class FlavourChoices(models.TextChoices):

#     VANILLA = 'Vanilla','Vanilla'

#     CHOCOLATE = 'Chocolate','Chocolate'
    
#     BUTTERSCOTCH = 'Butterscotch','Butterscotch'
    
#     STRAWBERRY = 'Strawberry','Strawberry'
    
#     RED_VELVET = 'Red Velvet','Red Velvet'
    
#     BLACK_FOREST = 'Black Forest','Black Forest'
    
#     WHITE_FOREST = 'White Forest','White Forest'
    
#     PINEAPPLE = 'Pineapple','Pineapple'
    
#     BLUEBERRY = 'Blueberry','Blueberry'
    
#     MANGO = 'Mango','Mango'
    
#     OREO = 'Oreo','Oreo'

class Flavour(BaseClass):

    name = models.CharField(max_length=30)

    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name = 'flavours'

        verbose_name_plural = 'flavours'

# class ShapeChoices(models.TextChoices):

#     ROUND = 'Round','Round'

#     SQUARE = 'Square','Square'

#     RECTANGLE = 'Rectangle','Rectangle'

#     HEART = 'Heart','Heart'

#     OVAL = 'Oval','Oval'

class Shape(BaseClass):

    name = models.CharField(max_length=30)

    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name = 'shapes'

        verbose_name_plural = 'shapes'

# class WeightChoices(models.TextChoices):

#     HALF_KG = '1/2 kg','1/2 kg'

#     ONE_KG = '1 kg','1 kg'

#     TWO_KG = '2 kg','2 kg'

#     THREE_KG = '3 kg','3 kg'

class Weight(BaseClass):

    name = models.CharField(max_length=30)

    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name = 'weight'

        verbose_name_plural = 'weight'

class Cake(BaseClass):

    name = models.CharField(max_length=50)

    description = models.TextField()

    photo = models.ImageField(upload_to='cake-images')

    category = models.ForeignKey('Category',on_delete=models.CASCADE)

    flavour = models.ForeignKey('Flavour',on_delete=models.CASCADE)

    shape = models.ForeignKey('Shape',on_delete=models.CASCADE)

    weight = models.ForeignKey('weight',on_delete=models.CASCADE)

    egg_added = models.BooleanField(default=True)

    is_available = models.BooleanField(default=True)

    price = models.FloatField()

    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name = 'Cakes'

        verbose_name_plural = 'Cakes'
