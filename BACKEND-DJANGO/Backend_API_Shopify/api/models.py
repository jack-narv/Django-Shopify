# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Atributos(models.Model):
    id_atributo = models.IntegerField(db_column='ID_ATRIBUTO', primary_key=True)  # Field name made lowercase.
    parent = models.TextField(db_column='PARENT', blank=True, null=True)  # Field name made lowercase.
    atribute_1_name = models.TextField(db_column='ATRIBUTE_1_NAME', blank=True, null=True)  # Field name made lowercase.
    atribute_1_value = models.TextField(db_column='ATRIBUTE_1_VALUE', blank=True, null=True)  # Field name made lowercase.
    atribute_2_name = models.TextField(db_column='ATRIBUTE_2_NAME', blank=True, null=True)  # Field name made lowercase.
    atribute_2_value = models.TextField(db_column='ATRIBUTE_2_VALUE', blank=True, null=True)  # Field name made lowercase.
    atribute_3_name = models.TextField(db_column='ATRIBUTE_3_NAME', blank=True, null=True)  # Field name made lowercase.
    atribute_3_value = models.TextField(db_column='ATRIBUTE_3_VALUE', blank=True, null=True)  # Field name made lowercase.
    atribute_4_name = models.TextField(db_column='ATRIBUTE_4_NAME', blank=True, null=True)  # Field name made lowercase.
    atribute_4_value = models.TextField(db_column='ATRIBUTE_4_VALUE', blank=True, null=True)  # Field name made lowercase.
    atribute_5_name = models.TextField(db_column='ATRIBUTE_5_NAME', blank=True, null=True)  # Field name made lowercase.
    atribute_5_value = models.TextField(db_column='ATRIBUTE_5_VALUE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'atributos'



class Producto(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase. The composite primary key (ID, ID_ATRIBUTO) found, that is not supported. The first column is selected.
    id_atributo = models.ForeignKey(Atributos, models.DO_NOTHING, db_column='ID_ATRIBUTO')  # Field name made lowercase.
    type = models.TextField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    sku = models.TextField(db_column='SKU', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='NAME', blank=True, null=True)  # Field name made lowercase.
    published = models.TextField(db_column='PUBLISHED', blank=True, null=True)  # Field name made lowercase.
    is_featured_field = models.TextField(db_column='IS_FEATURED?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    visibility_catalog = models.TextField(db_column='VISIBILITY_CATALOG', blank=True, null=True)  # Field name made lowercase.
    short_description = models.TextField(db_column='SHORT_DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    in_stock_field = models.TextField(db_column='IN_STOCK?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    stock = models.TextField(db_column='STOCK', blank=True, null=True)  # Field name made lowercase.
    backorders_allowed = models.TextField(db_column='BACKORDERS_ALLOWED', blank=True, null=True)  # Field name made lowercase.
    sold_individually = models.TextField(db_column='SOLD_INDIVIDUALLY', blank=True, null=True)  # Field name made lowercase.
    weight_lbs_field = models.TextField(db_column='WEIGHT (LBS)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    customer_reviews = models.TextField(db_column='CUSTOMER_REVIEWS', blank=True, null=True)  # Field name made lowercase.
    sale_price = models.TextField(db_column='SALE_PRICE', blank=True, null=True)  # Field name made lowercase.
    regular_price = models.TextField(db_column='REGULAR_PRICE', blank=True, null=True)  # Field name made lowercase.
    categories = models.TextField(db_column='CATEGORIES', blank=True, null=True)  # Field name made lowercase.
    image = models.TextField(db_column='IMAGE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'producto'
        unique_together = (('id', 'id_atributo'),)
