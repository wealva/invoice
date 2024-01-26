from django import forms
from django.forms import formset_factory
from django.forms import inlineformset_factory
from .models import *


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'product_name',
#             'product_price',
#             'product_unit',
#         ]
#         widgets = {
#             'product_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'product_name',
#                 'placeholder': 'Ingresa el nombre del producto',
#             }),
#             'product_price': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'id': 'product_price',
#                 'placeholder': 'Ingresa el precio del producto',
#                 'type': 'number',
#             }),
#             'product_unit': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'product_unit',
#                 'placeholder': 'Ingresa la cantidad del producto',
#             }),
#         }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_price',
            'product_unit',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'product_name',
                'placeholder': 'Enter name of the product',
            }),
            'product_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'product_price',
                'placeholder': 'Enter price of the product',
                'type': 'number',
            }),
            'product_unit': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'product_unit',
                'placeholder': 'Enter unit of the product',
            }),
        }



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_name',
            'customer_gender',
            'customer_dob',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'customer_name',
                'placeholder': 'Ingresa el nombre del cliente',
            }),
            'customer_gender': forms.Select(attrs={
                'class': 'form-control',
                'id': 'Selecciona género',
            }),
            'customer_dob': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'customer_dob',
                'placeholder': '2000-01-01',
                'type': 'date',
            }),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer',
            'comments',
            'contact',
            'email',
        ]
        widgets = {
            'customer': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_customer',
                'placeholder': 'Ingresa el nombre del cliente',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_contact',
                'placeholder': 'Ingresa el contacto del cliente',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'invoice_email',
                'placeholder': 'Ingresa el email del cliente',
            }),
            'comments': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_comments',
                'placeholder': 'Ingresa comentario',
            }),

        }


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = [
            'product',
            'amount',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_product',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_amount',
                'placeholder': '0',
                'type': 'number',
            })
        }


class excelUploadForm(forms.Form):
    file = forms.FileField()


InvoiceDetailFormSet = formset_factory(InvoiceDetailForm, extra=1)


# 
# 
# 

# class CategoriaForm(forms.ModelForm):
#     class Meta:
#         model = Categoria
#         fields = [
#             'categoria',
#             # Añade aquí los demás campos si es necesario
#         ]
#         widgets={
#             'categoria': forms.TextInput(attrs={
#                 'class': 'form-control'
#                 'placeholder': 'Ingrese el nombre del proveedor',
#             }),
#         }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'stock',
            # 'usuario_creacion',
            # 'usuario_modificacion',
            'categoria',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del producto',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el precio del producto',
                'type': 'number',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el stock del producto',
                'type': 'number',
            }),
            # 'usuario_creacion': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Ingrese el usuario de creación',
            # }),
            # 'usuario_modificacion': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Ingrese el usuario de modificación',
            # }),
            'categoria': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre',
            'contacto',
            'telefono',
            'direccion',
            # 'usuario_creacion',
            # 'usuario_modificacion',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del proveedor',
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el contacto del proveedor',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono del proveedor',
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección del proveedor',
            }),
            # 'usuario_creacion': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Ingrese el usuario de creación',
            # }),
            # 'usuario_modificacion': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Ingrese el usuario de modificación',
            # }),
        }





class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = Detallecompra
        fields = [
            'producto',
            'cantidad',
            # Añade aquí los demás campos si es necesario
        ]
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un producto',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad',
                'type': 'number',
            }),
           
        }
class excelSubirForm(forms.Form):
    file = forms.FileField()


# InvoiceDetailFormSet = formset_factory(InvoiceDetailForm, extra=1)

DetalleCompraFormSet = inlineformset_factory(Compra, Detallecompra, form=DetalleCompraForm, extra=1)

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = [
            'date',
            'proveedor',
            'cod_factura',
            'contacto',
            
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la fecha de compra',
                'type': 'date',
            }),
            'proveedor': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un proveedor',
            }),
            'cod_factura': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'cod_factura',
                'placeholder': 'Ingrese el codigo',
                'type': 'number',
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_contact',
                'placeholder': 'Ingresa el contacto',
            }),
           
        }


        



           