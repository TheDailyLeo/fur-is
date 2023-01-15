from django.db import models
class Status(models.Model):
    name = models.CharField(max_length=200, null=True
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

class Supplier(models.Model):
    EMPTY = 'EY'
    SABLE = 'SB'
    FOX = 'FX'
    KARAKUL = 'KL'
    PRODUCT_RANGE_CHOICES = [
        (EMPTY, 'Empty'),
        (SABLE, 'Sable'),
        (FOX, 'Fox'),
        (KARAKUL, 'Karakul'),
    ]
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(max_length=200, null=True)
    product_range = models.CharField(max_length=2, choices=PRODUCT_RANGE_CHOICES, default=EMPTY)
    inn = models.IntegerField(max_length=200, null=True)
    kpp = models.IntegerField(max_length=200, null=True)
    bank_account = models.IntegerField(max_length=200, null=True)
    corr_acc_num = models.IntegerField(max_length=200, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

class Consignment(models.Model):
    SABLE = 'SB'
    FOX = 'FX'
    KARAKUL = 'KL'
    PRODUCT_RANGE_CHOICES = [
        (SABLE, 'Sable'),
        (FOX, 'Fox'),
        (KARAKUL, 'Karakul'),
    ]
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
    type_material = models.CharField(max_length=2, choices=PRODUCT_RANGE_CHOICES)
    waybill_num = models.IntegerField(max_length=200, null=True)
    date_income = models.DateTimeField(auto_now_add=True, null=True)
    amount_material = models.IntegerField(max_length=200, null=True)
    price_material = models.FloatField(max_length=200, null=True)

    def __str__(self):
        return str(self.waybill_num)

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

class Material(models.Model):
    consignment = models.ForeignKey(Consignment, null=True, on_delete=models.SET_NULL)
    material_pic = models.ImageField(upload_to='images', null=True, blank=True)
    location_warehouse = models.IntegerField(max_length=3, null=True)
    warehouse_cell = models.IntegerField(max_length=3, null=True)
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)
    edited = models.BooleanField(default=False)
    edit_date = models.DateTimeField(auto_now_add=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Material, self).__init__(*args, **kwargs)
        self._published = self.edited

    def save(self, *args, **kwargs):
        if self.edited and self.edit_date is None:
            self.edit_date = datetime.now()
        elif not self.edited and self.edit_date is not None:
            self.edit_date = None
        super(Material, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + " " + str(self.consignment)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

class Characteristics(models.Model):
    material = models.ForeignKey(Material, null=True, on_delete=models.SET_NULL)
    hex_code_1 = models.CharField(max_length=7, null=True)
    hex_code_2 = models.CharField(max_length=7, null=True)
    hex_code_3 = models.CharField(max_length=7, null=True)
    height = models.IntegerField(max_length=3, null=True)
    width_up = models.IntegerField(max_length=3, null=True)
    width_down = models.IntegerField(max_length=3, null=True)

    def __str__(self):
        return str(self.material)

    class Meta:
        verbose_name = 'Список характеристик'
        verbose_name_plural = 'Характеристики'


