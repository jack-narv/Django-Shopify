
import time
from django.http import JsonResponse
from django.views import View
from .models import Producto
from .models import Atributos
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.shortcuts import render
import requests

# Create your views here.

# Configuración de credenciales de Shopify
API_KEY = '2363d7a7df6a98a412cd26ffdd0230aa'
API_SECRET_KEY = '119632d9c3fb449d982d27f29b37dbd1'
ACCESS_TOKEN = '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'
SHOP_NAME = 'jack-store1708.myshopify.com'

# Endpoint base de la API de Shopify
BASE_URL = f'https://{SHOP_NAME}/admin/api/2023-07/'

#Clase producto
class ProductView(View):

    #desactivar la protección CSRF (Cross-Site Request Forgery) para la vista
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args, **kwargs)
    
    #Método GET productos BD
    def get(self, request, id=0):

        #Get por ID
        if (id>0):
            productos=list(Producto.objects.filter(id=id).values())
            if len(productos)>0:
                producto=productos[0]
                datos={'message':"Success", "product":producto}
            else:
                datos={'message':"Products not found..."}
            return JsonResponse(datos)
        else:
            #Get todos productos BD
            productos=list(Producto.objects.values())
            if len(productos)>0:
                datos={'message':"Success", 'productos':productos}
            else:
                datos={'message':"Products not found..."}
            return JsonResponse(datos)
    
    #Método Post
    def post(self, request):
        #print(request.body)
        jd=json.loads(request.body)
        atributos=list(Atributos.objects.filter(id_atributo=jd["id_atributo_id"]).values())

        atributo=atributos[0]
        #Producto a subir a Shopify      
        shopify_product_data = {
           
			"title": jd['name'],
			"body_html": jd['description'],
			"vendor": jd['categories'],
			"product_type": jd['type'],
            
			"variants": [
                {
                    "price": jd['sale_price'],
                    "sku": jd['sku'],
                    "inventory_management": "shopify",
                    "inventory_quantity": jd['stock']
                }
            ],
            "images" : [
                {
                    "src": jd['image']
                }
            ]
        }
        
        #Crear producto en BD
        Producto.objects.create(
            
			id=jd['id'],
			id_atributo_id=jd['id_atributo_id'],
			type=jd['type'],
			sku=jd['sku'],
			name=jd['name'],
			published=jd['published'],
			is_featured_field=jd['is_featured_field'],
			visibility_catalog=jd['visibility_catalog'],
			short_description=jd['short_description'],
			description=jd['description'],
			in_stock_field=jd['in_stock_field'],
			stock=jd['stock'],
			backorders_allowed=jd['backorders_allowed'],
			sold_individually=jd['sold_individually'],
			weight_lbs_field=jd['weight_lbs_field'],
			customer_reviews=jd['customer_reviews'],
			sale_price=jd['sale_price'],
			regular_price=jd['regular_price'],
			categories=jd['categories'],
			image=jd['image']

        )
        url = BASE_URL + 'products.json'
        headers = {
            'X-Shopify-Access-Token': ACCESS_TOKEN,
        }
        #Crear producto en Shopify
        response = requests.post(url, json={'product': shopify_product_data}, headers=headers)

        if response.status_code == 201:
            data = response.json()
            return JsonResponse(data['product'])
        else:
            datos={'message':"Shopify Connection not found...", "response":response}
            return JsonResponse(datos)

    #Método PUT BD
    def put(self, request, id):
        
        jd=json.loads(request.body)

        #Actualización de producto en BD
        productos=list(Producto.objects.filter(id=id).values())
        if len(productos)>0:
            producto = Producto.objects.get(id=id)
            producto.id=jd['id']
            producto.id_atributo_id=jd['id_atributo_id']
            producto.type=jd['type']
            producto.sku=jd['sku']
            producto.name=jd['name']
            producto.published=jd['published']
            producto.is_featured_field=jd['is_featured_field']
            producto.visibility_catalog=jd['visibility_catalog']
            producto.short_description=jd['short_description']
            producto.description=jd['description']
            producto.in_stock_field=jd['in_stock_field']
            producto.stock=jd['stock']
            producto.backorders_allowed=jd['backorders_allowed']
            producto.sold_individually=jd['sold_individually']
            producto.weight_lbs_field=jd['weight_lbs_field']
            producto.customer_reviews=jd['customer_reviews']
            producto.sale_price=jd['sale_price']
            producto.regular_price=jd['regular_price']
            producto.categories=jd['categories']
            producto.image=jd['image']
            print(producto)
            producto.save()
            datos={'message':"Success"}
        else:
            datos={'message':"Products not found..."}
        return JsonResponse(datos)
    
    #Delete producto BD
    def delete(self, request, id):
        productos=list(Producto.objects.filter(id=id).values())
        if len(productos)>0:
            Producto.objects.filter(id=id).delete()
            datos={'message':"Success"}
        else:
            datos={'message':"Products not found..."}
        return JsonResponse(datos)

#Clase Shopify
class ShopifyView(View):

    #desactivar la protección CSRF (Cross-Site Request Forgery) para la vista
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args, **kwargs)
    
    #Método Get para productos en Shopify
    def get(self, request, id=0):
        headers = {
            'X-Shopify-Access-Token': ACCESS_TOKEN,
            }
        #Get producto por Id Shopify
        if (id>0):
            url = BASE_URL + f'products/{id}.json'
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return JsonResponse({'data':data['product']}) 
            elif response.status_code == 404:
                datos={'message':"Producto no encontrado Shopify..."}
                return JsonResponse(datos)
            else:
               datos={'message':"Products not found Shopify..."}
               return JsonResponse(datos)
        
        else:
            #Get todos los productos de Shopify
            url = BASE_URL + 'products.json'
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return JsonResponse({'data-productos':data['products']})
            else:
                datos={'message':"Products not found Shopify..."}
                return JsonResponse(datos)
            
    #Método delete Shopify
    def delete(self, request, id):
        url = BASE_URL + f'products/{id}.json'
        headers = {
            'X-Shopify-Access-Token': ACCESS_TOKEN,
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            datos={'message':"Producto eliminado de Shopify..."}
            return JsonResponse(datos)
        elif response.status_code == 404:
            datos={'message':"No se encontró el producto en Shopify..."}
            return JsonResponse(datos)
        else:
            datos={'message':"Error al eliminar el producto de Shopify..."}
            return JsonResponse(datos)
    
    #Método update Shopify
    def put(self, request, id):
        url = BASE_URL + f'products/{id}.json'
        headers = {
            'X-Shopify-Access-Token': ACCESS_TOKEN,
        }
        jd=json.loads(request.body)

        #Actualización de producto
        shopify_product_data = {
                "id": jd['id'],
                "title": jd['title'],
                "body_html": jd['body_html'],
                "vendor": jd['vendor'],
                "product_type": jd['product_type'],
                "created_at": jd['created_at'],
                "handle": jd['handle'],
                "updated_at": jd['updated_at'],
                "published_at": jd['published_at'],
                "template_suffix": jd['template_suffix'],
                "status": jd['status'],
                "published_scope": jd['published_scope'],
                "tags": jd['tags'],
                "admin_graphql_api_id": jd['admin_graphql_api_id'],
                "variants": jd['variants'],
                "options": jd['options'],
                "images": jd['images'],
                "image": jd['image']
            }
        
        #Método put con producto actualizado en Shopify
        response = requests.put(url, json={'product': shopify_product_data}, headers=headers)

        if response.status_code == 200:
            data = response.json()

            #CREACIÓN DE WEBHOOKS PARA ACTUALIZACIÓN DE PRODUCTO EN SHOPIFY
            urlW = BASE_URL + 'webhooks.json'
            webhook = {
                    "topic": 'products/update',

                     #ADDRESS CREADO CON SERVIDOR LOCAL XAMPP Y TUNEL NGROK
                    "address": 'https://cf53-191-99-151-224.ngrok.io/urls.py',
                    "format": "json"

            }

            #POST Webhook creado
            responseW = requests.post(urlW, json={'webhook':webhook}, headers=headers)
            if responseW.ok:
                try:
                    dataW = responseW.json()

                    #DEVOLVEMOS MENSAJE DE SUCCESS, EL PRODUCTO ACTUALIZADO Y EL WEBHOOK CREADO
                    datos={'message':"Success","product":data['product'], "webhook":dataW['webhook']}
                    return JsonResponse(datos)
                except requests.exceptions.JSONDecodeError:
                    datos = {'message': "Success", "product": data['product'], "webhook": None}
                    return JsonResponse(datos)
            else:
                # Manejar errores aquí, por ejemplo, imprimir el contenido de la respuesta
                print(responseW.text)
                return JsonResponse({'No se pudo crear webhook':responseW.text})
            
        elif response.status_code == 404:
            datos={'message':"Producto no encontrado Shopify..."}
            return JsonResponse(datos)
        else:
            datos={'message':"Error al actualizar el producto en Shopify..."}
            return JsonResponse(datos)
            

class importarProductos(View):  
    #desactivar la protección CSRF (Cross-Site Request Forgery) para la vista
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args, **kwargs)

    #MÉTODO POST PARA MIGRAR TODOS LOS PRODUCTOS DE BASE DE DATOS A SHOPIFY        
    def post(self, request):

        productos=list(Producto.objects.values())

        if len(productos)>0:
         conteo = 0

         #POST PRODUCTO POR PRODUCTO
         for producto in productos:
                shopify_product_data = {
                
                    "title": producto['name'],
                    "body_html": producto['description'],
                    "vendor": producto['categories'],
                    "product_type": producto['type'],
                    
                    "variants": [
                        {
                            "price": producto['sale_price'],
                            "sku": producto['sku'],
                            "inventory_management": "shopify",
                            "inventory_quantity": producto['stock']
                        }
                    ],
                    "images": [
                        {
                            "src": producto['image']
                        }
                    ]
                }
                url = BASE_URL + 'products.json'
                headers = {
                    'X-Shopify-Access-Token': ACCESS_TOKEN,
                }

                response = requests.post(url, json={'product': shopify_product_data}, headers=headers, timeout=1200)

                if response.status_code == 201:
                        conteo+=1
                else:
                        datos = {
                                'message': "Shopify Connection not found...",
                                'status_code': response.status_code,
                                'response_content': response.text
                            }
                        return JsonResponse(datos)
                # Pausa de 1 segundo entre solicitudes para evitar sobrecargar el servidor
                time.sleep(1)
         return JsonResponse({'message':"Sehan subido los productos a Shopify...", "conteo":conteo})
        else:
            datos={'message':"Products not found..."}
            return JsonResponse(datos)
    
    
     

class AtributosView(View):
        #desactivar la protección CSRF (Cross-Site Request Forgery) para la vista
        @method_decorator(csrf_exempt)
        def dispatch(self, request, *args, **kwargs):
            return super().dispatch(request,*args, **kwargs)
        
        #MÉTODO GET PARA ATRIBUTOS EN BD
        def get(self, request, id=0):
            #GET POR ID EN BD
            if (id>0):
                atributos=list(Atributos.objects.filter(id_atributo=id).values())
                if len(atributos)>0:
                    atributo=atributos[0]
                    datos={'message':"Success", "atributo":atributo}
                else:
                    datos={'message':"Atributos not found..."}
                return JsonResponse(datos)
            else:
                #GET TODOS LOS ATRIBUTOS DE BD
                atributos=list(Atributos.objects.values())
                if len(atributos)>0:
                    datos={'message':"Success", 'atributos':atributos}
                else:
                    datos={'message':"Products not found..."}
                return JsonResponse(datos)
            
class WebhooksView(View):

    #desactivar la protección CSRF (Cross-Site Request Forgery) para la vista
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args, **kwargs)
    
    #Devuelve todos los webhooks creados
    def get(self, request, id=0):
        url = BASE_URL + 'webhooks.json'
        headers = {
            "X-Shopify-Access-Token": ACCESS_TOKEN
        }
        response = requests.get(url, headers=headers)
        
        if response.ok:
            return JsonResponse(response.json())
        else:
            # Manejar errores aquí, por ejemplo, imprimir el contenido de la respuesta
            print(response.text)
            return None