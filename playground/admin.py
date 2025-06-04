from django.contrib import admin
from django.db.models import Count
from datetime import date, timedelta
from . import models


# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['pk', 'name', 'price', 'expiration_date', 'expiration_status']
  list_editable = ['name', 'price', 'expiration_date']
  list_per_page = 30

  def expiration_status(self, product):
    time_until_expired = product.expiration_date - date.today()
    if time_until_expired < timedelta(0):
      return 'expired'
    elif time_until_expired < timedelta(5):
      return 'expiring soon'
    else:
      return 'ok'

@admin.register(models.Facture)
class FactureAdmin(admin.ModelAdmin):
  list_display = ['pk', 'date', 'products_count']
  list_per_page = 30

  @admin.display(ordering='products_count')
  def products_count(self, facture):
    return facture.products_count
 
  def get_queryset(self, request):
    return super().get_queryset(request).annotate(
      products_count = Count('facture_product')
    )

@admin.register(models.Facture_Product)
class Facture_ProductAdmin(admin.ModelAdmin):
  list_display = ['pk', 'quantity', 'facture_id', 'product']
  list_per_page = 30