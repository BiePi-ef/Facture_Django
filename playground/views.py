from django import urls
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q, F, Sum
from playground.models import Product, Facture, Facture_Product
from .cart import Cart


# Create your views here.

def say_hello(response):
  # queryset = Product.objects.filter(expiration_date__month=3)
  # queryset_facture = Facture.objects.all()
  # queryset_facture_product_P = Product.objects.filter()
  # queryset_facture_product_F = Facture.objects.prefetch_related('products').order_by('id').all()
  querytry = Facture.objects.all().annotate(price_total=Sum('products__price'))

  return render(response, 'hello.html', 
                {'name' : 'Mosh', 
                #  'products':list(queryset), 
                #  'factures':list(queryset_facture), 
                #  'facture_product_F' : list(queryset_facture_product_F)
                  'test' : querytry
                })

def accueil(response):
  return render(response, 'index.html')

def products(response, query='None'):
  all_products = Product.objects.all()
  query = response.GET.get('q', '')

  if query:
      all_products = Product.objects.filter(
          Q(name__icontains=query) | Q(id__icontains=query) | Q(expiration_date__icontains=query)
      )
  else:
      all_products = Product.objects.all()

  return render(response, 'products.html', 
                  {
                     'products': all_products
                  })

def cart_add(response, product_id):
    cart = Cart(response)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect(urls.reverse('products'))

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_remove_one(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_one(product)
    return redirect('cart_detail')

def cart_detail(response):
    cart = Cart(response)
    products_ids = []

    for i in cart:
      # print(i['product'].id)
      for n in range(i['quantity']):
        products_ids.append(i['product'].id)

    # make list readable for url
    str_products_ids = '_'.join([str(x) for x in products_ids])

    # make str_product_ids null if cart empty
    if cart.is_empty():
      return render(response, 'cart.html', {'cart': cart})
    else:
      return render(response, 'cart.html', {'cart': cart, 'str_products_ids': str_products_ids})

def get_facture_by_id(response, facture_id):
   facture = get_object_or_404(Facture, id=facture_id)
   return render(response, 'facture.html', {'facture': facture})


# Used logig for filter in checkout : code en doublon, moche
def factures(response):
  query = response.GET.get('q', '')
  all_factures = Facture.objects.all()
  all_products = Product.objects.all()
  
  # if query:
  #   all_factures = Facture.objects.filter(
  #     Q(id__icontains=query) | Q(date__icontains=query)
  #   )

  all_factures_products = Facture_Product.objects.all()

  lines_id_facture_id_product_quantity = []
  all_factures_w_products = []

  for line in all_factures_products:
    # facture = all_factures.get(id=line.facture_id)
    # product = all_products.get(id=line.product_id)
    facture = None
    product = None

    # populate lines_id_facture_id_product_quantity with objects
    # for i in all_factures:
    #   if line.facture_id == i.id:
    #       facture = i

    # for i in all_products:
    #   if line.product_id == i.id:
    #       product = i

    # lines_id_facture_id_product_quantity.append({
    #   "facture_id" : line.facture_id,
    #   "Product_id" : line.product_id,
    #   "quantity" : line.quantity
    # })
          

  return render(response, 
                'all_factures.html',
                {
                  'all_factures': all_factures,
                  'all_products' : all_products,
                  'all_factures_products' : all_factures_products,
                  # 'all_factures_products_treated' : lines_id_facture_id_product_quantity,
                })

def checkout(response, str_products_ids = None):
    
    if bool(str_products_ids) == True:
      # un-stringify the ids
      list_products_ids = [int(x) for x in str_products_ids.split('_')]
    
      facture = Facture.objects.create()
      # Add products to the facture (many-to-many)
      for pid in list_products_ids:
        product = get_object_or_404(Product, id=pid)
        if product in facture.products.all():
          pproduct = facture.facture_product_set.get(product_id=product.id)
          pproduct.quantity += 1
          print(pproduct)
          print(pproduct.quantity)
          # print(facture.products.all())
          # product_temp['facture_products__quantity'] += 1
        else:
          facture.products.add(product)
      
      facture.save()
      
    return factures(response)

# def get_products_facture_by_id(response, id):
#    products_id = Product.objects.filter(facture_id=id)
#    return render