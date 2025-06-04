from django.db import models

# Create your models here.
# ! types relates to form inputs

class Product(models.Model):
  slug = models.SlugField(null=True)
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  expiration_date = models.DateField()
  # m to m relationship creates a product_set list

  def __str__(self) -> str:
    return self.name
  
  class Meta:
    ordering = ['name']
  

class Facture(models.Model):
  slug = models.SlugField(null=True)
  date = models.DateTimeField(auto_now_add=True)
  products = models.ManyToManyField(Product, through="Facture_Product", unique=False)

  def __str__(self) -> str:
    return f"{self.date}_{self.pk}"

  class Meta:
    ordering = ['date']


class Facture_Product(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.facture} - {self.product}"
    
    # class Meta:
    #   ordering = ['facture_id']

## TEST : learning
# class Order(models.Model):
#   PAYEMENT_PENDING = 'P'
#   PAYEMENT_COMPLETE = 'C'
#   PAYEMENT_FAILED = 'F'
#   PAYEMENT_STATUS = [
#     (PAYEMENT_PENDING, 'Pending'),
#     (PAYEMENT_COMPLETE, 'Complete'),
#     (PAYEMENT_FAILED, 'Failed')
#   ]

#   placed_at = models.DateTimeField(auto_now_add=True),
#   payement_status = models.CharField(max_length=1, choices=PAYEMENT_STATUS, default=PAYEMENT_PENDING)