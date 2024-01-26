from django.urls import path
from . import views

urlpatterns = [

    path('', views.create_invoice, name='home'),

    path('create_product/', views.create_product, name='create_product'),
    path('view_product/', views.view_product, name='view_product'),
    path('edit_product/<int:pk>', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('upload_product_excel', views.upload_product_from_excel,
         name='upload_product_excel'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('view_customer/', views.view_customer, name='view_customer'),
    path('edit_customer/<int:pk>', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),

    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('delete_all_invoice/', views.delete_all_invoice,
         name='delete_all_invoice'),
    path('download_all_invoice/', views.download_all,
         name='download_all_invoice'),
    path('view_invoice_detail/<int:pk>/',
         views.view_invoice_detail, name='view_invoice_detail'),
    path('create_producto/', views.create_producto, name='create_producto'),
    path('view_producto/', views.view_producto, name='view_producto'),
    path('edit_producto/<int:pk>', views.edit_producto, name='edit_producto'),
    path('delete_producto/<int:pk>/', views.delete_producto, name='delete_producto'),
#     path('upload_product_excel', views.upload_product_from_excel,
#          name='upload_product_excel'),
    path('create_proveedor/', views.create_proveedor, name='create_proveedor'),
    path('view_proveedor/', views.view_proveedor, name='view_proveedor'),
    path('edit_proveedor/<int:pk>', views.edit_proveedor, name='edit_proveedor'),
    path('delete_proveedor/<int:pk>/', views.delete_proveedor, name='delete_proveedor'),

    path('create_compra/', views.create_compra, name='create_compra'),
    path('view_compra/', views.view_compra, name='view_compra'),
    path('delete_compra/<int:pk>/', views.delete_compra, name='delete_compra'),
    path('delete_all_invoice/', views.delete_all_invoice,name='delete_all_invoice'),
    path('download_all_compra/', views.download_all,name='download_all_compra'),
    path('view_compra_detail/<int:pk>/',views.view_compra_detail, name='view_compra_detail'),
]