
from django.db import models

class Car(models.Model):
      
   
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    chassis_number = models.CharField(max_length=100, unique=True)

    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    sale_date = models.DateField(null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=[('unsold', 'غير مباعة'), ('sold', 'مباعة')],
        default='unsold'
      )
    
    CLEARANCE_CHOICES = models.CharField(
       max_length=10,
       choices=[('buy', 'شراء'),('ad', 'اعلان')],
        default='buy'
       )
    partial_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
  


    def __str__(self):
        return self.name
    
   

    # 🔹 الربح الكلي (حسابي فقط)
    def total_profit(self):
        if self.sale_price:
            return self.sale_price - self.purchase_price
            return 0

    def save(self, *args, **kwargs):
        if self.sale_date:
            self.status = 'sold'
        super().save(*args, **kwargs)

    def _str_(self):
        return self.car_type
    

class Expense (models.Model):
    
    description = models.CharField(max_length=200,default="none")
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    expense_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
